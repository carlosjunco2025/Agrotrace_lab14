"""Semana 14 · Ejercicio 8: controlador transaccional de pedidos.

El precio se lee de la base de datos dentro de ``transaction.atomic``; el
navegador sólo envía identificadores y cantidades. El descuento de stock usa
F('stock') para que la base de datos haga la resta atómicamente.
"""

from decimal import Decimal
import uuid

from django.db import transaction
from django.db.models import F
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from catalogo.models import Producto

from .models import Cliente, DetallePedido, Pago, Pedido
from .serializers import (
    ClienteSerializer,
    CrearPedidoSerializer,
    PagoSerializer,
    PedidoSerializer,
)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'documento']


class PagoViewSet(viewsets.ReadOnlyModelViewSet):
    """Los pagos se consultan, pero no se inventan desde la API."""

    queryset = Pago.objects.select_related('pedido')
    serializer_class = PagoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente', 'pago').prefetch_related(
        'detalles__producto',
    )
    serializer_class = PedidoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente__nombre', 'estado']

    @action(detail=False, methods=['post'], url_path='crear')
    def crear_pedido(self, request):
        """Registra pedido + detalle + pago y descuenta stock en una sola transacción."""
        serializer = CrearPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cliente = serializer.validated_data['cliente']
        items = serializer.validated_data['items']
        ids = [item['producto'].pk for item in items]

        with transaction.atomic():
            # select_for_update bloquea las filas; en SQLite el bloqueo lo
            # garantiza la transacción. El orden evita interbloqueos.
            productos = {
                producto.pk: producto
                for producto in Producto.objects.select_for_update()
                .filter(pk__in=ids)
                .order_by('pk')
            }

            # 1) Validar disponibilidad usando los valores leídos de la BD.
            for item in items:
                producto = productos.get(item['producto'].pk)
                if producto is None:
                    raise ValidationError(
                        {'items': f'El producto {item["producto"].pk} no existe.'}
                    )
                if not producto.activo:
                    raise ValidationError(
                        {'items': f'{producto.nombre} no está activo.'}
                    )
                if producto.stock < item['cantidad']:
                    raise ValidationError(
                        {
                            'items': (
                                f'Stock insuficiente para {producto.nombre}: '
                                f'se solicitan {item["cantidad"]} y hay {producto.stock}.'
                            )
                        }
                    )

            # 2) Calcular el total en el servidor con los precios de la BD.
            total = sum(
                (
                    productos[item['producto'].pk].precio * item['cantidad']
                    for item in items
                ),
                Decimal('0.00'),
            )

            # 3) Persistir cabecera, detalle, pago simulado y descontar stock.
            pedido = Pedido.objects.create(
                cliente=cliente,
                estado=Pedido.ESTADO_PENDIENTE,
                total=total,
            )
            for item in items:
                producto = productos[item['producto'].pk]
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=producto.precio,
                )
                Producto.objects.filter(pk=producto.pk).update(
                    stock=F('stock') - item['cantidad'],
                )

            Pago.objects.create(
                pedido=pedido,
                monto=total,
                estado=Pago.ESTADO_PAGADO,
                referencia=f'SIM-{uuid.uuid4().hex[:12].upper()}',
            )
            pedido.estado = Pedido.ESTADO_PAGADO
            pedido.save(update_fields=['estado'])

        return Response(
            PedidoSerializer(pedido).data,
            status=status.HTTP_201_CREATED,
        )
