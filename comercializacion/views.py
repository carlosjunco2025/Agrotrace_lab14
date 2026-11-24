from django.http import JsonResponse


def modulo(request):
    """Respuesta de estructura: confirma que la app está creada y registrada."""
    return JsonResponse(
        {
            "modulo": "Comercialización AgroTrace",
            "estado": "estructura_inicial",
            "planificacion": "Estructura en S13 · pedidos y pagos en S15",
            "rutas_previstas": ['/api/pedidos-agrotrace/', '/api/precios/'],
            "nota": "Los modelos de negocio se programan en la Semana 14.",
        }
    )
