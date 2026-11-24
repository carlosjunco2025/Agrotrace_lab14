"""Verificación en shell de los Ejercicios 3 y 4 (y su equivalente AgroTrace).

Uso: python manage.py verificar_semana14
"""

from django.core.management.base import BaseCommand
from django.db.models import ProtectedError

from catalogo.models import Categoria, Producto
from comercializacion.models import ProductoAgro


class Command(BaseCommand):
    help = 'Lista datos sembrados y demuestra ProtectedError al borrar una categoría.'

    def handle(self, *args, **options):
        self.stdout.write('== Categorías (Ejercicio 3) ==')
        for categoria in Categoria.objects.all():
            self.stdout.write(f'  {categoria.id}: {categoria.nombre}')

        self.stdout.write('== Producto.objects.all() ==')
        self.stdout.write(f'  SQL equivalente: {Producto.objects.all().query}')
        for producto in Producto.objects.all():
            self.stdout.write(
                f'  {producto.id}: {producto.nombre} | S/ {producto.precio} | '
                f'stock {producto.stock} | {producto.categoria.nombre}'
            )

        self.stdout.write('== ProductoAgro (equivalente AgroTrace) ==')
        for producto in ProductoAgro.objects.all():
            self.stdout.write(
                f'  {producto.codigo}: {producto.nombre} | '
                f'{producto.stock_kg} kg | S/ {producto.precio_kg}/kg'
            )

        categoria = Categoria.objects.filter(productos__isnull=False).first()
        if categoria is None:
            self.stdout.write('No hay categorías con productos para probar PROTECT.')
            return

        self.stdout.write('== Prueba de on_delete=PROTECT (Ejercicio 4) ==')
        try:
            categoria.delete()
        except ProtectedError as error:
            self.stdout.write(
                self.style.ERROR(
                    'ProtectedError: no se puede borrar la categoría '
                    f'"{categoria.nombre}" porque tiene productos asociados.'
                )
            )
            self.stdout.write(f'  Detalle: {error.args[0][:180]}')
        else:
            self.stdout.write(self.style.ERROR('ERROR: la categoría se borró (no debe).'))
