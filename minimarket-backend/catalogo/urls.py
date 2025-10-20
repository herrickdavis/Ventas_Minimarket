from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, MarcaViewSet, ClaseImpuestoViewSet, UnidadViewSet, 
    ConversionUnidadViewSet, ProductoViewSet, VarianteProductoViewSet, 
    ComboProductoViewSet, ListaPreciosViewSet, ReglaListaPreciosViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'clases-impuestos', ClaseImpuestoViewSet, basename='claseimpuesto')
router.register(r'unidades', UnidadViewSet, basename='unidad')
router.register(r'conversiones-unidades', ConversionUnidadViewSet, basename='conversionunidad')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'variantes', VarianteProductoViewSet, basename='variante')
router.register(r'combos', ComboProductoViewSet, basename='combo')
router.register(r'listas-precios', ListaPreciosViewSet, basename='listaprecios')
router.register(r'reglas-precios', ReglaListaPreciosViewSet, basename='reglaprecios')

urlpatterns = [
    path('', include(router.urls)),
]