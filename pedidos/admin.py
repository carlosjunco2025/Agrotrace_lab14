from django.contrib import admin

from .models import Cliente, DetallePedido, Pago, Pedido


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'documento', 'email')
    search_fields = ('nombre', 'documento')


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('precio_unitario',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado',)
    inlines = (DetallePedidoInline,)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'pedido', 'monto', 'estado')
    list_filter = ('estado',)
