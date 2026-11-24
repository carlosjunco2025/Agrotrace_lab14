from django.http import JsonResponse


def modulo(request):
    """Respuesta de estructura: confirma que la app está creada y registrada."""
    return JsonResponse(
        {
            "modulo": "Trazabilidad AgroTrace",
            "estado": "estructura_inicial",
            "planificacion": "Estructura en S13 · histórico y trazas en S16",
            "rutas_previstas": ['/api/trazabilidad/', '/api/trazabilidad/{codigo_lote}/'],
            "nota": "Los modelos de negocio se programan en la Semana 14.",
        }
    )
