"""Semana 14 · Ejercicio 5: serializers del catálogo de la cafetería."""

from rest_framework import serializers

from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre')


class ProductoSerializer(serializers.ModelSerializer):
    """Convierte Producto <-> JSON y aplica la regla de precio positivo."""

    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True,
    )

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'precio',
            'stock',
            'activo',
            'categoria',
            'categoria_nombre',
        )

    def validate_precio(self, value):
        """Regla de negocio: un producto no puede costar cero ni ser negativo."""
        if value <= 0:
            raise serializers.ValidationError(
                'El precio debe ser mayor que cero.'
            )
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value
