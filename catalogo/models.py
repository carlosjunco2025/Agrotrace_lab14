"""Semana 14 · Ejercicio 2: catálogo de la cafetería.

Categoria es el padre de Producto. Se usa ``PROTECT`` para que la tabla de
categorías no pueda eliminarse mientras siga referencing productos: el
histórico comercial no debe quedar huérfano por un borrado accidental.
"""

from django.db import models


class Categoria(models.Model):
    """Grupo de productos de la cafetería (Bebidas, Repostería, ...)."""

    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto vendible. El dinero se guarda como Decimal, nunca como float."""

    nombre = models.CharField(max_length=120)
    # Columna SQL: DECIMAL(10, 2) -> precio con dos decimales exactos.
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Columna SQL: INTEGER con restricción >= 0 (PositiveIntegerField).
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return f'{self.nombre} (S/ {self.precio})'
