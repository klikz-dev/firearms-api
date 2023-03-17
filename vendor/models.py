from django.db import models
from django import forms
from django.http import HttpResponseRedirect


class Brand(models.Model):
    slug = models.CharField(
        primary_key=True, max_length=200, null=False, blank=True)
    name = models.CharField(max_length=200, null=False)
    page_link = models.URLField(
        max_length=1000, default=None, null=True, blank=True)
    logo_image = models.URLField(default=None, null=True, blank=True)
    retailer = models.CharField(max_length=200, null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.slug)

    def subcategory_num(self):
        return self.subcategory.count()

    def product_num(self):
        count = 0
        for subcategory in self.subcategory.all():
            count += subcategory.product.count()
        return count

    __original_slug = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_slug = self.slug

    def save(self, *args, **kwargs):
        self.slug = str(self.slug).lower()

        if " " in self.slug:
            raise forms.ValidationError(
                {'slug': "Slugs should always standardize to alphanumeric, lowercase, and hypens only!"})

        super(Brand, self).save(*args, **kwargs)

        if self.slug != self.__original_slug:
            original = Brand(slug=self.__original_slug)
            original.delete()

        self.__original_slug = self.slug

        return HttpResponseRedirect("/admin/vendor/brand/{}".format(self.slug))


class Subcategory(models.Model):
    slug = models.CharField(
        primary_key=True, max_length=200, null=False, blank=True)
    name = models.CharField(max_length=200, default="General", null=False)

    brand = models.ForeignKey(
        Brand, related_name='subcategory', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.slug)

    __original_slug = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_slug = self.slug

    def save(self, *args, **kwargs):
        self.slug = str(self.slug).lower()

        if " " in self.slug:
            raise forms.ValidationError(
                {'slug': "Slugs should always standardize to alphanumeric, lowercase, and hypens only!"})

        super(Subcategory, self).save(*args, **kwargs)

        if self.slug != self.__original_slug:
            original = Subcategory(slug=self.__original_slug)
            original.delete()

        self.__original_slug = self.slug

        return HttpResponseRedirect("/admin/vendor/subcategory/{}".format(self.slug))


class Category(models.Model):
    slug = models.CharField(
        primary_key=True, max_length=200, null=False, blank=True)
    name = models.CharField(max_length=200, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)

    __original_slug = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_slug = self.slug

    def save(self, *args, **kwargs):
        self.slug = str(self.slug).lower()

        if " " in self.slug:
            raise forms.ValidationError(
                {'slug': "Slugs should always standardize to alphanumeric, lowercase, and hypens only!"})

        super(Category, self).save(*args, **kwargs)

        if self.slug != self.__original_slug:
            original = Category(slug=self.__original_slug)
            original.delete()

        self.__original_slug = self.slug

        return HttpResponseRedirect("/admin/vendor/category/{}".format(self.slug))


class Product(models.Model):
    sku = models.CharField(
        max_length=200, primary_key=True, null=False, blank=True)
    retailer = models.CharField(max_length=200, default=None, null=True)

    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE, null=True, blank=True)

    subcategory = models.ForeignKey(
        Subcategory, related_name='product', on_delete=models.CASCADE, null=True, blank=True)

    manufacturer_id = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    name = models.CharField(max_length=200, null=False)
    slug = models.CharField(max_length=200, null=False)

    long_description = models.TextField(
        max_length=5000, default=None, null=True, blank=True)
    short_description = models.TextField(
        max_length=2500, default=None, null=True, blank=True)

    thumb_url = models.URLField(default=None, null=True)
    image_url = models.URLField(default=None, null=True, blank=True)
    medium_image_url = models.URLField(default=None, null=True, blank=True)

    buy_link = models.URLField(default=None, null=True, blank=True)
    alternative_buy_link = models.URLField(default=None, null=True, blank=True)

    keywords = models.TextField(
        max_length=1000, default=None, null=True, blank=True)
    reviews = models.TextField(
        max_length=2000, default=None, null=True, blank=True)

    retail_price = models.FloatField(default=0)
    sale_price = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)

    color = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    size = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    pattern = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    material = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    weight = models.FloatField(default=1)
    age_group = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    gender = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    upc = models.CharField(max_length=200, default=None, null=True, blank=True)
    gtin = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    guid = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    sale_price_effective_date = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    availability = models.BooleanField(default=True)
    visibility = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    condition = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_status = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    tracking = models.TextField(
        max_length=200, default=None, null=True, blank=True)
    product_group = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    parent_group = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    model_number = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    content_widget = models.TextField(
        max_length=1000, default=None, null=True, blank=True)
    alternative_product_id = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    alternative_image_id = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    google_categorization = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    commission = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.slug)

    def quantity_status(self):
        if self.quantity == -1:
            return "In Stock"
        elif self.quantity == 0:
            return "Out of Stock"
        else:
            return self.quantity


class Page(models.Model):
    slug = models.CharField(
        primary_key=True, max_length=200, null=False, blank=True)
    title = models.CharField(max_length=200, default=None, null=True)

    category = models.ForeignKey(
        Category, related_name='page', on_delete=models.CASCADE)

    brand = models.ForeignKey(
        Brand, related_name='page', on_delete=models.CASCADE)

    pre_category_rank = models.IntegerField(default=-1, null=True, blank=True)
    pre_brand_rank = models.IntegerField(default=-1, null=True, blank=True)

    rel_Brownells = models.FloatField(default=1.5, null=True, blank=True)
    rel_Palmetto = models.FloatField(default=1.5, null=True, blank=True)
    rel_EuroOptic = models.FloatField(default=1.5, null=True, blank=True)
    rel_Gritr = models.FloatField(default=1.5, null=True, blank=True)
    rel_Guns = models.FloatField(default=1.5, null=True, blank=True)
    rel_PrimaryArms = models.FloatField(default=1.5, null=True, blank=True)
    rel_Sportsman = models.FloatField(default=1.5, null=True, blank=True)

    stat_acc = models.IntegerField(default=-1, null=True, blank=True)
    stat_erg = models.IntegerField(default=-1, null=True, blank=True)
    stat_ftr = models.IntegerField(default=-1, null=True, blank=True)
    stat_fit = models.IntegerField(default=-1, null=True, blank=True)
    stat_rel = models.IntegerField(default=-1, null=True, blank=True)
    stat_val = models.IntegerField(default=-1, null=True, blank=True)

    description = models.TextField(default=None, null=True, blank=True)

    product = models.ManyToManyField(Product, related_name='page')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    __original_slug = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_slug = self.slug

    def save(self, *args, **kwargs):
        self.slug = str(self.slug).lower()

        if " " in self.slug:
            raise forms.ValidationError(
                {'slug': "Slugs should always standardize to alphanumeric, lowercase, and hypens only!"})

        super(Page, self).save(*args, **kwargs)

        if self.slug != self.__original_slug:
            original = Page(slug=self.__original_slug)
            original.delete()

        self.__original_slug = self.slug

        return HttpResponseRedirect("/admin/vendor/page/{}".format(self.slug))


class Review(models.Model):
    page = models.ForeignKey(
        Page, related_name='reviews', on_delete=models.CASCADE)

    name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    email = models.EmailField(
        max_length=200, default=None, null=True, blank=True)
    review = models.TextField(
        max_length=5000, default=None, null=True, blank=True)
    stat_acc = models.IntegerField(default=-1, null=True, blank=True)
    stat_erg = models.IntegerField(default=-1, null=True, blank=True)
    stat_ftr = models.IntegerField(default=-1, null=True, blank=True)
    stat_fit = models.IntegerField(default=-1, null=True, blank=True)
    stat_rel = models.IntegerField(default=-1, null=True, blank=True)
    stat_val = models.IntegerField(default=-1, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class PriceHistory(models.Model):
    product = models.ForeignKey(
        Product, related_name='pricehistory', on_delete=models.CASCADE)

    new_retail = models.FloatField(default=0, null=True, blank=True)
    new_auction = models.FloatField(default=0, null=True, blank=True)
    used_retail = models.FloatField(default=0, null=True, blank=True)
    used_auction = models.FloatField(default=0, null=True, blank=True)

    date = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.new_retail)
