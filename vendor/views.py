from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from vendor.pagination import StandardResultsSetPagination
from vendor.serializers import BrandListSerializer, BrandRetrieveSerializer, BrandSlugSerializer, CategoryListSerializer, CategoryRetrieveSerializer, CategorySlugSerializer, PageListSerializer, PageRetrieveSerializer, PageSlugSerializer, ProductListSerializer, ProductRetrieveSerializer, SubcategoryListSerializer, SubcategoryRetrieveSerializer, SubcategorySlugSerializer, ReviewListSerializer, ReviewRetrieveSerializer
from vendor.models import Brand, Category, Page, Product, Subcategory, Review
from django.db.models import Count


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def list(self, request):
        categories = Category.objects.all().annotate(
            page_num=Count('page')).order_by('-page_num')

        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        categories = Category.objects.all()
        category = get_object_or_404(categories, slug=pk)
        serializer = CategoryRetrieveSerializer(
            instance=category, context={'request': request})
        return Response(serializer.data)


class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer

    def list(self, request):
        brands = Brand.objects.all().annotate(
            page_num=Count('page')).order_by('-page_num')

        page = self.paginate_queryset(brands)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(brands, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        brands = Brand.objects.all()
        brand = get_object_or_404(brands, slug=pk)
        serializer = BrandRetrieveSerializer(
            instance=brand, context={'request': request})
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ModelViewSet):

    queryset = Subcategory.objects.all()
    serializer_class = SubcategoryListSerializer

    def list(self, request):
        subcategories = Subcategory.objects.all()

        page = self.paginate_queryset(subcategories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        subcategories = Subcategory.objects.all()
        subcategory = get_object_or_404(subcategories, slug=pk)
        serializer = SubcategoryRetrieveSerializer(
            instance=subcategory, context={'request': request})
        return Response(serializer.data)


class PageViewSet(viewsets.ModelViewSet):

    queryset = Page.objects.all()
    serializer_class = PageListSerializer

    def list(self, request):
        pages = Page.objects.all().annotate(
            product_num=Count('product')).order_by('-product_num')

        brand = self.request.query_params.get('brand')
        if brand is not None:
            pages = pages.filter(brand=brand)

        category = self.request.query_params.get('category')
        if category is not None:
            pages = pages.filter(category=category)

        page = self.paginate_queryset(pages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(pages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pages = Page.objects.all()
        page = get_object_or_404(pages, slug=pk)
        serializer = PageRetrieveSerializer(
            instance=page, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def list(self, request):
        products = Product.objects.all()

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        products = Product.objects.all()
        product = get_object_or_404(products, sku=pk)
        serializer = ProductRetrieveSerializer(
            instance=product, context={'request': request})
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def list(self, request):
        reviews = Review.objects.all()

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        reviews = Review.objects.all()
        review = get_object_or_404(reviews, slug=pk)
        serializer = ReviewRetrieveSerializer(
            instance=review, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


##### Sitemap #####
class PageSlugsSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSlugSerializer

    def list(self, request):
        pages = Page.objects.all().annotate(
            product_num=Count('product')).order_by('-product_num')

        page = self.paginate_queryset(pages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(pages, many=True)
        return Response(serializer.data)


class BrandSlugsSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSlugSerializer

    def list(self, request):
        brands = Brand.objects.all().annotate(
            page_num=Count('page')).order_by('-page_num')

        page = self.paginate_queryset(brands)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(brands, many=True)
        return Response(serializer.data)


class CategorySlugsSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySlugSerializer

    def list(self, request):
        categories = Category.objects.all().annotate(
            page_num=Count('page')).order_by('-page_num')

        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class SubcategorySlugsSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySlugSerializer

    def list(self, request):
        subcategories = Subcategory.objects.all()

        page = self.paginate_queryset(subcategories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)
