from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework import routers
from vendor.views import BrandSlugsSet, BrandViewSet, CategorySlugsSet, CategoryViewSet, PageSlugsSet, PageViewSet, ProductViewSet, SubcategorySlugsSet, SubcategoryViewSet, ReviewViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'pages', PageViewSet)
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

router.register(r'page-slugs', PageSlugsSet)
router.register(r'brand-slugs', BrandSlugsSet)
router.register(r'category-slugs', CategorySlugsSet)
router.register(r'subcategory-slugs', SubcategorySlugsSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('advanced_filters/', include('advanced_filters.urls'))
]
