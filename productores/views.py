from django.http import JsonResponse


def modulo(request):
    """Respuesta de estructura: confirma que la app está creada y registrada."""
    return JsonResponse(
        {
            "modulo": "Productores AgroTrace",
            "estado": "estructura_inicial",
            "planificacion": "Estructura en S13 · modelos y API en S14",
            "rutas_previstas": ['/api/productores/', '/api/productores/{id}/'],
            "nota": "Los modelos de negocio se programan en la Semana 14.",
        }
    )
