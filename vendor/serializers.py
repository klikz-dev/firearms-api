from vendor.models import Brand, Category, Page, PriceHistory, Product, Subcategory
from rest_framework import serializers


#######################################################
###################### Product ########################
#######################################################
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['sku', 'slug', 'name', 'sale_price',
                  'retailer', 'thumb_url', 'image_url']


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['date', 'new_retail', 'new_auction',
                  'used_retail', 'used_auction']


class ProductRetrieveSerializer(serializers.ModelSerializer):
    pricehistory = ProductPriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['sku', 'retailer', 'manufacturer_id', 'name', 'slug', 'long_description', 'short_description',
                  'thumb_url', 'image_url', 'medium_image_url', 'buy_link', 'alternative_buy_link', 'keywords',
                  'reviews', 'retail_price', 'sale_price', 'color', 'size', 'pattern', 'material', 'weight',
                  'age_group', 'gender', 'upc', 'gtin', 'guid', 'sale_price_effective_date', 'availability',
                  'visibility', 'quantity', 'condition', 'shipping_status', 'tracking', 'product_group', 'parent_group',
                  'model_number', 'content_widget', 'alternative_product_id', 'alternative_image_id', 'google_categorization',
                  'commission', 'created_at', 'updated_at', 'pricehistory', 'page']


#######################################################
####################### Page ##########################
#######################################################
class PageListSerializer(serializers.ModelSerializer):
    product_num = serializers.SerializerMethodField(read_only=True)
    sale_price = serializers.SerializerMethodField(read_only=True)
    thumb_url = serializers.SerializerMethodField(read_only=True)
    subcategory = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)

    def get_product_num(self, page):
        return page.product.count()

    def get_sale_price(self, page):
        products = Product.objects.filter(page=page).order_by('-sale_price')
        return products[0].sale_price

    def get_thumb_url(self, page):
        products = Product.objects.filter(page=page).order_by('-sale_price')
        return products[0].thumb_url
    
    def get_subcategory(self, page):
        products = Product.objects.filter(page=page).order_by('-sale_price')
        try:
            subcategory = Subcategory.objects.get(slug=products[0].subcategory)
            return subcategory.name
        except Subcategory.DoesNotExist:
            return ''
        
    def get_description(self, page):
        products = Product.objects.filter(page=page).order_by('-sale_price')
        description = page.description
        if products[0].short_description:
            description = products[0].short_description
        if products[0].long_description:
            description = products[0].long_description
        return description

    class Meta:
        model = Page
        fields = ['url', 'slug', 'title', 'brand', 'category', 'pre_category_rank',
                  'pre_brand_rank', 'product_num', 'subcategory', 'sale_price', 'thumb_url', 'description', 'updated_at']


class PageProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'sale_price']


class PageBrandRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['slug', 'name']


class PageCategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name']


class PageRetrieveSerializer(serializers.ModelSerializer):
    product = PageProductRetrieveSerializer(many=True, read_only=True)
    brand = PageBrandRetrieveSerializer(read_only=True)
    category = PageCategoryRetrieveSerializer(read_only=True)

    class Meta:
        model = Page
        fields = ['slug', 'title', 'description',
                  'brand', 'category', 'pre_category_rank', 'pre_brand_rank',
                  'rel_Brownells', 'rel_Palmetto', 'rel_EuroOptic', 'rel_Gritr', 'rel_Guns', 'rel_PrimaryArms', 'rel_Sportsman',
                  'product']


#######################################################
##################### Category ########################
#######################################################
class CategoryListSerializer(serializers.ModelSerializer):
    page_num = serializers.SerializerMethodField(read_only=True)

    def get_page_num(self, category):
        return category.page.count()

    class Meta:
        model = Category
        fields = ['url', 'slug', 'name', 'page_num', 'updated_at']


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name']


#######################################################
################### Subcategory #######################
#######################################################
class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['url', 'slug', 'name', 'brand', 'updated_at']


class SubcategoryProductPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug']


class SubcategoryProductSerializer(serializers.ModelSerializer):
    page = SubcategoryProductPageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'sale_price', 'thumb_url',
                  'image_url', 'retailer', 'page']


class SubcategoryRetrieveSerializer(serializers.ModelSerializer):
    product = SubcategoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = ['slug', 'name', 'product']


#######################################################
####################### Brand #########################
#######################################################
class BrandListSerializer(serializers.ModelSerializer):
    page_num = serializers.SerializerMethodField(read_only=True)

    def get_page_num(self, category):
        return category.page.count()

    class Meta:
        model = Brand
        fields = ['url', 'slug', 'name', 'page_link',
                  'logo_image', 'page_num', 'updated_at']


class BrandSubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ['slug', 'name']


class BrandRetrieveSerializer(serializers.ModelSerializer):
    subcategory = BrandSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['url', 'slug', 'name',
                  'page_link', 'logo_image', 'subcategory']


#######################################################
##################### Sitemap #########################
#######################################################
class PageSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'updated_at']


class BrandSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['slug', 'updated_at']


class CategorySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'updated_at']


class SubcategorySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['slug', 'updated_at']
