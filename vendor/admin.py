from django import forms
from django.db.models import Count
from django.contrib import admin
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.admin.widgets import FilteredSelectMultiple
from advanced_filters.admin import AdminAdvancedFiltersMixin
from rangefilter.filters import DateRangeFilter
from django.utils.translation import gettext_lazy as _
from vendor.models import Brand, Category, PriceHistory, Product, Page, Subcategory


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0

    fields = ('date', 'new_retail', 'new_auction',
              'used_retail', 'used_auction')

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProductPageInline(admin.TabularInline):
    model = Product.page.through
    extra = 0


class ProductAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    actions = ['new_page', 'update_page']

    def new_page(self, request, queryset):
        if 'apply' in request.POST and 'new_page' in request.POST['action']:
            page = Page(slug=request.POST['page_slug'])

            page.title = request.POST['page_title']
            page.category = Category.objects.get(
                name=request.POST['page_category'])

            page.save()

            for product in queryset:
                product.page.add(page)

            self.message_user(request,
                              "Successfully created a page {}".format(queryset.count()))
            return HttpResponseRedirect("/admin/vendor/page/{}".format(page.slug))

        category_ok = True
        for product in queryset:
            if product.category != queryset[0].category:
                category_ok = False

        if category_ok:
            return render(request,
                          'admin/new_page_intermediate.html',
                          context={'products': queryset, 'category': queryset[0].category})
        else:
            self.message_user(
                request, "Select the products in the same category only.", level=messages.ERROR)

    def update_page(self, request, queryset):
        if 'apply' in request.POST and 'update_page' in request.POST['action']:
            page = Page(slug=request.POST['selected_page'])

            for product in queryset:
                product.page.add(page)

            self.message_user(request,
                              "Successfully added products")
            return HttpResponseRedirect("/admin/vendor/page/{}".format(page.slug))

        category_ok = True
        for product in queryset:
            if product.category != queryset[0].category:
                category_ok = False

        if category_ok:
            category = Category.objects.get(name=queryset[0].category)
            pages = Page.objects.filter(category=category)
            return render(request,
                          'admin/update_page_intermediate.html',
                          context={'products': queryset, 'pages': pages})
        else:
            self.message_user(
                request, "Select the products in the same category only.", level=messages.ERROR)

    new_page.short_description = "Create Page from Selection"
    update_page.short_description = "Add products to Page"

    def has_add_permission(self, request):
        return False

    fieldsets = [
        (None, {'fields': ['sku']}),
        ('Collection', {'fields': [
         'retailer', 'manufacturer_id', 'category', 'subcategory']}),
        ('Content', {'fields': [
         'name', 'long_description', 'short_description']}),
        ('Images', {'fields': ['thumb_url', 'image_url', 'medium_image_url']}),
        ('Checkout', {'fields': ['buy_link', 'alternative_buy_link']}),
        ('Tagging', {'fields': ['keywords', 'reviews']}),
        ('Pricing', {'fields': ['retail_price',
         'sale_price', 'shipping_cost']}),
        ('Detail', {'fields': ['color', 'size', 'pattern', 'material',
         'weight', 'age_group', 'gender', 'upc', 'gtin', 'guid']}),
        ('Availability', {'fields': [
         'availability', 'sale_price_effective_date', 'visibility', 'quantity', 'condition', 'shipping_status']}),
        ('Additional Information', {'fields': [
         'tracking', 'product_group', 'parent_group', 'model_number', 'content_widget', 'alternative_product_id', 'alternative_image_id', 'google_categorization', 'commission']}),
    ]

    # inlines = [PriceHistoryInline, ProductPageInline]
    inlines = [PriceHistoryInline]

    list_display = ('sku', 'retailer', 'brand', 'category', 'subcategory', 'name',
                    'retail_price', 'sale_price', 'availability', 'quantity_status')

    list_filter = [('updated_at', DateRangeFilter),
                   'retailer', 'category', 'availability']

    advanced_filter_fields = (
        'sku',
        'name',
        'long_description',
        'short_description',
        'retail_price',
        'sale_price',
    )

    search_fields = ['retailer', 'sku', 'name']

    def brand(self, obj):
        return obj.subcategory.brand


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

    fields = ['sku', 'name', 'slug', 'sale_price']

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].required = False
        self.fields['product'].widget = FilteredSelectMultiple(
            verbose_name=_('Products'),
            is_stacked=False)
        try:
            self.fields['product'].queryset = Product.objects.filter(
                category=self.instance.category)
        except:
            self.fields['product'].queryset = Product.objects.filter(
                category='Default')


class PageAdmin(admin.ModelAdmin):
    actions = ['combine_pages']

    def combine_pages(self, request, queryset):
        if 'apply' in request.POST and 'combine_pages' in request.POST['action']:
            dst_page = Page.objects.get(slug=request.POST['selected_page'])

            for page in queryset:
                products = page.product.all()
                for product in products:
                    product.page.add(dst_page)

                if page != dst_page:
                    page.delete()

            self.message_user(request, "Successfully combine pages")
            return HttpResponseRedirect("/admin/vendor/page/{}".format(dst_page.slug))

        category_ok = True
        for page in queryset:
            if page.category != queryset[0].category:
                category_ok = False

        if category_ok:
            return render(request,
                          'admin/combine_pages_intermediate.html',
                          context={'pages': queryset})
        else:
            self.message_user(
                request, "Select the products in the same category only.", level=messages.ERROR)

    form = PageAdminForm
    filter_horizontal = ('product',)

    list_filter = ['category']

    search_fields = ['slug', 'title']

    list_display = (
        'slug',
        'title',
        'brand',
        'category',
        'product_num',
        'pre_category_rank',
        'pre_brand_rank',
    )

    fieldsets = (
        ('Main', {
            "fields": (
                'slug',
                'title',
                'brand',
                'category'
            ),
        }),
        ('Rank', {
            "fields": (
                'pre_category_rank',
                'pre_brand_rank',
            ),
        }),
        ('Brand Cross sell', {
            "fields": (
                'rel_Brownells',
                'rel_Palmetto',
                'rel_EuroOptic',
                'rel_Gritr',
                'rel_Guns',
                'rel_PrimaryArms',
                'rel_Sportsman'
            ),
        }),
        ('Overwrite Stat Values', {
            "fields": (
                'stat_acc',
                'stat_erg',
                'stat_ftr',
                'stat_fit',
                'stat_rel',
                'stat_val',
            ),
        }),
        ('Product', {
            "fields": (
                'product',
            ),
        }),
    )

    def get_queryset(self, request):
        qs = super(PageAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('product'))
        return qs

    def product_num(self, obj):
        return obj.product__count

    product_num.admin_order_field = 'product__count'


class PageInline(admin.TabularInline):
    model = Page
    extra = 0

    fields = ['slug', 'title']

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):
    actions = ['combine_categories']

    def combine_categories(self, request, queryset):
        if 'apply' in request.POST and 'combine_categories' in request.POST['action']:
            dst_category = Category(slug=request.POST['selected_category'])

            for category in queryset:
                pages = category.page.all()
                for page in pages:
                    page.category = dst_category
                    page.save()

                products = category.product.all()
                for product in products:
                    product.category = dst_category
                    product.save()

                if category != dst_category:
                    category.delete()

            self.message_user(request, "Successfully combine categories")
            return HttpResponseRedirect("/admin/vendor/category/{}".format(dst_category.slug))

        return render(request,
                      'admin/combine_categories_intermediate.html',
                      context={'categories': queryset})

    fields = ['slug', 'name']

    list_display = ('slug', 'name', 'page_num')

    search_fields = ['slug', 'name']

    inlines = [PageInline]

    # def get_readonly_fields(self, request, obj=None):
    #     return self.fields or [f.name for f in self.model._meta.fields]

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('page'))
        return qs

    def page_num(self, obj):
        return obj.page__count

    page_num.admin_order_field = 'page__count'


class SubcategoryAdmin(admin.ModelAdmin):
    actions = ['combine_subcategories']

    def combine_subcategories(self, request, queryset):
        if 'apply' in request.POST and 'combine_subcategories' in request.POST['action']:
            dst_subcategory = Subcategory(
                slug=request.POST['selected_subcategory'])

            for subcategory in queryset:
                products = subcategory.product.all()
                for product in products:
                    product.subcategory = dst_subcategory
                    product.save()

                if subcategory != dst_subcategory:
                    subcategory.delete()

            self.message_user(request, "Successfully combined subcategories")
            return HttpResponseRedirect("/admin/vendor/subcategory/{}".format(dst_subcategory.slug))

        return render(request,
                      'admin/combine_subcategories_intermediate.html',
                      context={'subcategories': queryset})

    fields = ['slug', 'name']

    list_display = ('slug', 'name', 'brand', 'product_num')

    search_fields = ['slug', 'name']

    inlines = [ProductInline]

    # def get_readonly_fields(self, request, obj=None):
    #     return self.fields or [f.name for f in self.model._meta.fields]

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(SubcategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('product'))
        return qs

    def product_num(self, obj):
        return obj.product__count

    product_num.admin_order_field = 'product__count'


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BrandAdmin(admin.ModelAdmin):
    actions = ['combine_brands']

    def combine_brands(self, request, queryset):
        if 'apply' in request.POST and 'combine_brands' in request.POST['action']:
            dst_brand = Brand(slug=request.POST['selected_brand'])

            for brand in queryset:
                subcategories = brand.subcategory.all()
                for subcategory in subcategories:
                    subcategory.brand = dst_brand
                    subcategory.save()

                if brand != dst_brand:
                    brand.delete()

            self.message_user(request, "Successfully combine brands")
            return HttpResponseRedirect("/admin/vendor/brand/{}".format(dst_brand.slug))

        return render(request,
                      'admin/combine_brands_intermediate.html',
                      context={'brands': queryset})

    fields = ['slug', 'name', 'page_link', 'logo_image']

    list_display = ('slug', 'name', 'page_link', 'logo_image',
                    'subcategory_num', 'product_num')

    search_fields = ['slug', 'name']

    inlines = [SubcategoryInline]

    # def get_readonly_fields(self, request, obj=None):
    #     return self.fields or [f.name for f in self.model._meta.fields]

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Product, ProductAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
