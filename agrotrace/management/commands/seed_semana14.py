"""Datos reales de prueba para los ejercicios de la Semana 14.

Uso:
    python manage.py seed_semana14

El comando es idempotente: si se ejecuta dos veces no duplica registros.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand

from catalogo.models import Categoria, Producto
from comercializacion.models import (
    ClienteAgro,
    ProductoAgro,
    ProductorAgro,
)
from pedidos.models import Cliente

CATEGORIAS = ['Bebidas', 'Repostería']

PRODUCTOS = [
    ('Café de origen', '18.50', 40, 'Bebidas'),
    ('Capuchino', '14.00', 25, 'Bebidas'),
    ('Jugo de naranja', '10.50', 15, 'Bebidas'),
    ('Croissant de almendra', '8.50', 30, 'Repostería'),
    ('Pan de yuca', '6.00', 20, 'Repostería'),
]

CLIENTES_CAFETERIA = [
    ('Compañía Andes SAC', 'cliente-andes@tecsup.edu.pe', '20500123456'),
    ('Distribuidora Costa Verde', 'costa-verde@tecsup.edu.pe', '20500987654'),
]

PRODUCTORES_AGRO = [
    ('Asociación Valle Norte', '20601111111', 'Cajamarca'),
    ('Fundo Los Olivos', '20602222222', 'La Libertad'),
]

CLIENTES_AGRO = [
    ('Exportadora del Sur SAC', '20603333333', 'exportaciones@tecsup.edu.pe'),
    ('Molinos Unión', '20604444444', 'molinos@tecsup.edu.pe'),
]

PRODUCTOS_AGRO = [
    ('AG-001', 'Café arábica lavado', '1200.00', '18.50', 'Asociación Valle Norte'),
    ('AG-002', 'Café natural de altura', '800.00', '15.75', 'Asociación Valle Norte'),
    ('AG-003', 'Cacao fermentado', '500.00', '22.40', 'Fundo Los Olivos'),
    ('AG-004', 'Banano orgánico', '2000.00', '3.20', 'Fundo Los Olivos'),
    ('AG-005', 'Miel de abeja pura', '300.00', '28.00', 'Fundo Los Olivos'),
]


class Command(BaseCommand):
    help = 'Siembra categorías, productos, clientes y productores de la Semana 14.'

    def handle(self, *args, **options):
        categorias = {}
        for nombre in CATEGORIAS:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre)
            categorias[nombre] = categoria

        for nombre, precio, stock, categoria in PRODUCTOS:
            _, creado = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'precio': Decimal(precio),
                    'stock': stock,
                    'activo': True,
                    'categoria': categorias[categoria],
                },
            )
            if creado:
                self.stdout.write(f'Producto creado: {nombre}')

        for nombre, email, documento in CLIENTES_CAFETERIA:
            _, creado = Cliente.objects.get_or_create(
                documento=documento,
                defaults={'nombre': nombre, 'email': email},
            )
            if creado:
                self.stdout.write(f'Cliente de cafetería creado: {nombre}')

        productores = {}
        for nombre, ruc, region in PRODUCTORES_AGRO:
            productor, _ = ProductorAgro.objects.get_or_create(
                ruc=ruc,
                defaults={'nombre': nombre, 'region': region, 'activo': True},
            )
            productores[nombre] = productor

        for nombre, documento, email in CLIENTES_AGRO:
            _, creado = ClienteAgro.objects.get_or_create(
                documento=documento,
                defaults={'nombre': nombre, 'email': email},
            )
            if creado:
                self.stdout.write(f'Cliente AgroTrace creado: {nombre}')

        for codigo, nombre, stock, precio, productor in PRODUCTOS_AGRO:
            _, creado = ProductoAgro.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'stock_kg': Decimal(stock),
                    'precio_kg': Decimal(precio),
                    'activo': True,
                    'productor': productores[productor],
                },
            )
            if creado:
                self.stdout.write(f'Producto AgroTrace creado: {codigo} - {nombre}')

        self.stdout.write(
            self.style.SUCCESS(
                'Semilla S14 lista: '
                f'{Categoria.objects.count()} categorías, '
                f'{Producto.objects.count()} productos de cafetería, '
                f'{ProductoAgro.objects.count()} productos AgroTrace.'
            )
        )
