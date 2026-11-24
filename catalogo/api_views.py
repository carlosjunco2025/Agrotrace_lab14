"""Semana 14 · Ejercicio 5: ViewSets REST del catálogo."""

from rest_framework import filters, viewsets

from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']


class ProductoViewSet(viewsets.ModelViewSet):
    """CRUD + búsqueda por nombre, publicado en /api/productos/."""

    queryset = Producto.objects.select_related('categoria')
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
