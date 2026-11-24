"""Semana 14 · Ejercicio 4: pedidos, detalle y pago simulado de la cafetería.

Un Pedido es la cabecera; DetallePedido es la tabla de línea. La regla de
integridad es: borrar el pedido borra sus detalles (CASCADE), pero borrar un
producto vendido está prohibido (PROTECT) para no alterar el histórico.
"""

from django.db import models

from catalogo.models import Producto


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    documento = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_PAGADO = 'PAGADO'
    ESTADO_ENTREGADO = 'ENTREGADO'
    ESTADO_CANCELADO = 'CANCELADO'
    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_ENTREGADO, 'Entregado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos',
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    # Columna SQL: DECIMAL(12, 2). Se calcula en Django, jamás en el navegador.
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion', '-id']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.cliente.nombre} ({self.estado})'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_pedido',
    )
    cantidad = models.PositiveIntegerField()
    # Precio "congelado" al momento de la venta; cambiar el catálogo no reescribe la venta.
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad


class Pago(models.Model):
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_PAGADO = 'PAGADO'
    ESTADO_FALLIDO = 'FALLIDO'
    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_FALLIDO, 'Fallido'),
    ]

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pago',
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    referencia = models.CharField(max_length=40, unique=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pago {self.referencia} - {self.estado}'
