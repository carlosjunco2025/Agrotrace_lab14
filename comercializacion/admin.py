from django.contrib import admin

from .models import (
    ClienteAgro,
    DetalleOrdenDespacho,
    OrdenDespacho,
    PagoDespacho,
    ProductoAgro,
    ProductorAgro,
)


@admin.register(ProductorAgro)
class ProductorAgroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ruc', 'region', 'activo')


@admin.register(ClienteAgro)
class ClienteAgroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'documento', 'email')


@admin.register(ProductoAgro)
class ProductoAgroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'stock_kg', 'precio_kg', 'productor', 'activo')
    list_filter = ('activo', 'productor')
    search_fields = ('codigo', 'nombre')


class DetalleDespachoInline(admin.TabularInline):
    model = DetalleOrdenDespacho
    extra = 0


@admin.register(OrdenDespacho)
class OrdenDespachoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado',)
    inlines = (DetalleDespachoInline,)


@admin.register(PagoDespacho)
class PagoDespachoAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'orden', 'monto', 'estado')
