"""Semana 14 · Ejercicio 11: ViewSets de AgroTrace y orden transaccional."""

from decimal import Decimal
import uuid

from django.db import transaction
from django.db.models import F
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import (
    ClienteAgro,
    DetalleOrdenDespacho,
    OrdenDespacho,
    PagoDespacho,
    ProductoAgro,
    ProductorAgro,
)
from .serializers import (
    ClienteAgroSerializer,
    CrearOrdenDespachoSerializer,
    OrdenDespachoSerializer,
    PagoDespachoSerializer,
    ProductoAgroSerializer,
    ProductorAgroSerializer,
)


class ProductorAgroViewSet(viewsets.ModelViewSet):
    queryset = ProductorAgro.objects.all()
    serializer_class = ProductorAgroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'ruc']


class ClienteAgroViewSet(viewsets.ModelViewSet):
    queryset = ClienteAgro.objects.all()
    serializer_class = ClienteAgroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'documento']


class ProductoAgroViewSet(viewsets.ModelViewSet):
    """Entidad principal: CRUD y búsqueda en /api/productos-agro/."""

    queryset = ProductoAgro.objects.select_related('productor')
    serializer_class = ProductoAgroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'codigo']


class PagoDespachoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PagoDespacho.objects.select_related('orden')
    serializer_class = PagoDespachoSerializer


class OrdenDespachoViewSet(viewsets.ModelViewSet):
    queryset = OrdenDespacho.objects.select_related('cliente', 'pago').prefetch_related(
        'detalles__producto',
    )
    serializer_class = OrdenDespachoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente__nombre', 'estado']

    @action(detail=False, methods=['post'], url_path='crear')
    def crear_orden(self, request):
        """Versión AgroTrace de crear_pedido: mismo patrón, mismo atomic."""
        serializer = CrearOrdenDespachoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cliente = serializer.validated_data['cliente']
        items = serializer.validated_data['items']
        ids = [item['producto'].pk for item in items]

        with transaction.atomic():
            productos = {
                producto.pk: producto
                for producto in ProductoAgro.objects.select_for_update()
                .filter(pk__in=ids)
                .order_by('pk')
            }

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
                if producto.stock_kg < item['cantidad_kg']:
                    raise ValidationError(
                        {
                            'items': (
                                f'Stock insuficiente para {producto.nombre}: '
                                f'se solicitan {item["cantidad_kg"]} kg y hay '
                                f'{producto.stock_kg} kg.'
                            )
                        }
                    )

            total = sum(
                (
                    productos[item['producto'].pk].precio_kg * item['cantidad_kg']
                    for item in items
                ),
                Decimal('0.00'),
            )

            orden = OrdenDespacho.objects.create(
                cliente=cliente,
                estado=OrdenDespacho.ESTADO_PENDIENTE,
                total=total,
            )
            for item in items:
                producto = productos[item['producto'].pk]
                DetalleOrdenDespacho.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad_kg=item['cantidad_kg'],
                    precio_unitario_kg=producto.precio_kg,
                )
                ProductoAgro.objects.filter(pk=producto.pk).update(
                    stock_kg=F('stock_kg') - item['cantidad_kg'],
                )

            PagoDespacho.objects.create(
                orden=orden,
                monto=total,
                estado=PagoDespacho.ESTADO_PAGADO,
                referencia=f'AGRO-{uuid.uuid4().hex[:12].upper()}',
            )
            orden.estado = OrdenDespacho.ESTADO_PAGADO
            orden.save(update_fields=['estado'])

        return Response(
            OrdenDespachoSerializer(orden).data,
            status=status.HTTP_201_CREATED,
        )
