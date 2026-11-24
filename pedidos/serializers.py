"""Semana 14 · Ejercicios 5 y 8: serializers de pedidos y pago."""

from rest_framework import serializers

from catalogo.models import Producto

from .models import Cliente, DetallePedido, Pago, Pedido


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nombre', 'email', 'documento')


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = DetallePedido
        fields = (
            'id', 'producto', 'producto_nombre', 'cantidad',
            'precio_unitario', 'subtotal',
        )


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ('id', 'monto', 'estado', 'referencia', 'fecha_pago')
        read_only_fields = fields


class PedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Pedido
        fields = (
            'id', 'cliente', 'cliente_nombre', 'estado', 'total',
            'fecha_creacion', 'detalles', 'pago',
        )
        read_only_fields = ('total', 'fecha_creacion', 'estado')


class ItemPedidoSerializer(serializers.Serializer):
    """Un ítem del carrito enviado por React: sólo id y cantidad."""

    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    cantidad = serializers.IntegerField(min_value=1)

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor que cero.')
        return value


class CrearPedidoSerializer(serializers.Serializer):
    """Valida la entrada del endpoint transaccional antes de abrir la transacción."""

    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    items = serializers.ListField(child=ItemPedidoSerializer(), allow_empty=False)

    def validate_items(self, items):
        productos = [item['producto'].pk for item in items]
        if len(productos) != len(set(productos)):
            raise serializers.ValidationError(
                'No se puede repetir un producto en el mismo pedido.'
            )
        return items
