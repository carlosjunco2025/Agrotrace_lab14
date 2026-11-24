from django.http import JsonResponse


def modulo(request):
    """Respuesta de estructura: confirma que la app está creada y registrada."""
    return JsonResponse(
        {
            "modulo": "Pedidos (práctica cafetería)",
            "estado": "estructura_inicial",
            "planificacion": "Estructura en S13 · carrito y pedidos en S14-S15",
            "rutas_previstas": ['/api/pedidos/', '/api/pedidos/{id}/'],
            "nota": "Los modelos de negocio se programan en la Semana 14.",
        }
    )
