from django.http import JsonResponse


def modulo(request):
    """Respuesta de estructura: confirma que la app está creada y registrada."""
    return JsonResponse(
        {
            "modulo": "Inventario y lotes AgroTrace",
            "estado": "estructura_inicial",
            "planificacion": "Estructura en S13 · modelos y API en S14",
            "rutas_previstas": ['/api/lotes/', '/api/lotes-detallados/'],
            "nota": "Los modelos de negocio se programan en la Semana 14.",
        }
    )
