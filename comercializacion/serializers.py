"""Semana 14 · Ejercicio 11: serializers del dominio AgroTrace."""

from decimal import Decimal

from rest_framework import serializers

from .models import (
    ClienteAgro,
    DetalleOrdenDespacho,
    OrdenDespacho,
    PagoDespacho,
    ProductoAgro,
    ProductorAgro,
)


class ProductorAgroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductorAgro
        fields = ('id', 'nombre', 'ruc', 'region', 'activo')


class ClienteAgroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteAgro
        fields = ('id', 'nombre', 'documento', 'email')


class ProductoAgroSerializer(serializers.ModelSerializer):
    """Regla de negocio equivalente a validate_precio de la cafetería."""

    productor_nombre = serializers.CharField(source='productor.nombre', read_only=True)

    class Meta:
        model = ProductoAgro
        fields = (
            'id', 'codigo', 'nombre', 'stock_kg', 'precio_kg', 'activo',
            'productor', 'productor_nombre',
        )

    def validate_precio_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio por kg debe ser mayor que cero.')
        return value

    def validate_stock_kg(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value


class DetalleOrdenDespachoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = DetalleOrdenDespacho
        fields = (
            'id', 'producto', 'producto_nombre', 'cantidad_kg',
            'precio_unitario_kg', 'subtotal',
        )


class PagoDespachoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoDespacho
        fields = ('id', 'monto', 'estado', 'referencia', 'fecha_pago')
        read_only_fields = fields


class OrdenDespachoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    detalles = DetalleOrdenDespachoSerializer(many=True, read_only=True)
    pago = PagoDespachoSerializer(read_only=True)

    class Meta:
        model = OrdenDespacho
        fields = (
            'id', 'cliente', 'cliente_nombre', 'estado', 'total',
            'fecha_creacion', 'detalles', 'pago',
        )
        read_only_fields = ('estado', 'total', 'fecha_creacion')


class ItemDespachoSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=ProductoAgro.objects.all())
    cantidad_kg = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
    )

    def validate_cantidad_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad en kg debe ser mayor que cero.')
        return value


class CrearOrdenDespachoSerializer(serializers.Serializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=ClienteAgro.objects.all())
    items = serializers.ListField(child=ItemDespachoSerializer(), allow_empty=False)

    def validate_items(self, items):
        productos = [item['producto'].pk for item in items]
        if len(productos) != len(set(productos)):
            raise serializers.ValidationError(
                'No se puede repetir un producto en la misma orden.'
            )
        return items
