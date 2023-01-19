from django.core.management.base import BaseCommand
from django.db.models.aggregates import Count

from feed.models import AeroPrecision, Brownells, DanielDefense, EuroOptic, Gear1800, Guns, Palmetto, PrimaryArms, SportsmansGuide
from vendor.models import Brand, Category, Product, Page, Subcategory

import os
import random

from library import debug, common

debug = debug.debug

FILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    help = 'Build Product Database'

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        if "product" in options['functions']:
            self.aero()
            self.brownells()
            self.daniel()
            self.euro()
            self.gear1800()
            self.guns()
            self.palmetto()
            self.primaryarms()
            self.sportsmans()

        if "page" in options['functions']:
            self.page()

        if "clean" in options['functions']:
            self.clean()

        if "deletebuggy" in options['functions']:
            self.deletebuggy()

        if "updateRankAndRelPrice" in options['functions']:
            self.updateRankAndRelPrice()

    def aero(self):
        rows = AeroPrecision.objects.all()
        self.update(rows, "AeroPrecision")

    def brownells(self):
        rows = Brownells.objects.all()
        self.update(rows, "Brownells")

    def daniel(self):
        rows = DanielDefense.objects.all()
        self.update(rows, "DanielDefense")

    def euro(self):
        rows = EuroOptic.objects.all()
        self.update(rows, "EuroOptic")

    def gear1800(self):
        rows = Gear1800.objects.all()
        self.update(rows, "Gear1800")

    def guns(self):
        rows = Guns.objects.all()
        self.update(rows, "Guns")

    def palmetto(self):
        rows = Palmetto.objects.all()
        self.update(rows, "Palmetto")

    def primaryarms(self):
        rows = PrimaryArms.objects.all()
        self.update(rows, "PrimaryArms")

    def sportsmans(self):
        rows = SportsmansGuide.objects.all()
        self.update(rows, "SportsmansGuide")

    def update(self, rows, retailer):
        debug("Product", 0, "Start Processing {} Products".format(retailer))

        for row in rows:
            try:
                product = Product.objects.get(sku=row.sku)
            except Product.DoesNotExist:
                product = Product.objects.create(sku=row.sku)

            product.retailer = retailer
            product.manufacturer_id = row.manufacturer_id

            if row.product_name == "" or row.product_name == None:
                continue
            product.name = row.product_name
            product.slug = common.get_slug(product.name)

            product.long_description = row.long_description
            product.short_description = row.short_description

            product.product_group = row.product_group
            product.thumb_url = row.thumb_url
            product.image_url = row.image_url
            product.buy_link = row.buy_link
            product.keywords = row.keywords
            product.reviews = row.reviews
            try:
                product.retail_price = float(row.retail_price)
            except:
                pass
            try:
                product.sale_price = float(row.sale_price)
            except:
                pass

            product.tracking = row.tracking
            product.parent_group = row.parent_group
            product.color = row.color
            product.size = row.size
            product.pattern = row.pattern
            product.material = row.material
            try:
                product.weight = float(row.weight)
            except:
                pass
            product.age_group = row.age_group
            product.gender = row.gender
            product.upc = row.upc
            product.gtin = row.gtin
            product.guid = row.guid

            product.sale_price_effective_date = row.sale_price_effective_date
            if row.availability == "False":
                product.availability = False
            if row.visibility == "False":
                product.visibility = False

            product.model_number = row.model_number
            try:
                if row.quantity == '':
                    product.quantity = -1
                else:
                    product.quantity = int(row.quantity)
            except:
                pass
            product.alternative_buy_link = row.alternative_buy_link
            product.alternative_product_id = row.alternative_product_id
            product.alternative_image_id = row.alternative_image_id
            product.medium_image_url = row.medium_image_url
            product.content_widget = row.content_widget

            product.google_categorization = row.google_categorization
            try:
                product.commission = float(row.commission)
            except:
                pass

            category_name = row.category
            brand_name = row.brand_name
            brand_page_link = row.brand_page_link
            brand_logo_image = row.brand_logo_image
            subcategory_name = row.sub_category

            # Set Brand/Subcategory
            if subcategory_name == "":
                if "|" in category_name:
                    subcategory_name = category_name.split("|")[1].strip()
                    category_name = category_name.split("|")[0].strip()
                elif ">" in category_name:
                    subcategory_name = category_name.split(">")[-1].strip()
                    category_name = category_name.split(">")[-2].strip()
                else:
                    subcategory_name = "General"

            if brand_name == "":
                brand = Brand(slug='default', name='Default')
            else:
                brand = Brand(slug=common.get_slug(
                    brand_name), name=brand_name)

            if brand.page_link == "" or brand.page_link == None:
                brand.page_link = brand_page_link
            if brand.logo_image == "" or brand.logo_image == None:
                brand.logo_image = brand_logo_image
            brand.retailer = retailer
            brand.save()

            subcategory = Subcategory(slug=common.get_slug(
                brand_name + " " + subcategory_name), name=subcategory_name, brand=brand)
            subcategory.save()

            product.subcategory = subcategory
            ##############################

            # Set Category
            if category_name == "":
                category = Category(slug="default", name="Default")
            else:
                category = Category(slug=common.get_slug(
                    category_name), name=category_name)
            category.save()

            product.category = category
            ##############################

            try:
                product.save()
            except Exception as e:
                print(e)
                debug("Product", 1,
                      "Failed Processing {}".format(row.sku))
                continue

            # Set Price History
            product.pricehistory.create(
                new_retail=row.sale_price,
                new_auction=round(row.sale_price * 0.613, 2),
                used_retail=round(
                    row.sale_price * random.uniform(0.8161, 0.9161), 2),
                used_auction=round(
                    row.sale_price * random.uniform(0.513, 0.613), 2),
            )
            ##############################

            print("Product {} has been saved successfully".format(product.sku))

        debug("Product", 0, "Completed Processing {} Products".format(retailer))

    def page(self):
        categories = set(
            [p['category'] for p in Product.objects.values('category')])

        for category_name in categories:
            products = Product.objects.filter(category=category_name)

            for product1 in products:
                largest_common_name_words = []
                product2 = product1

                for comp in products:
                    if product1.slug == comp.slug:
                        continue

                    common_name_words = set(product1.name.split()) & set(
                        comp.name.split())
                    common_name_words = sorted(
                        common_name_words, key=lambda k: product1.name.split().index(k))

                    if len(common_name_words) > len(product1.name.split()) * 0.7 and len(common_name_words) > len(comp.name.split()) * 0.7:
                        if len(common_name_words) < len(largest_common_name_words):
                            continue
                        else:
                            largest_common_name_words = common_name_words
                            product2 = comp

                if product2 == product1 or len(largest_common_name_words) < 1:
                    pageTitle = product1.name
                    pageSlug = common.get_slug(pageTitle)
                else:
                    pageTitle = " ".join((largest_common_name_words))
                    pageSlug = common.get_slug(pageTitle)

                if pageSlug == "":
                    continue

                page = Page(slug=pageSlug)
                page.title = pageTitle

                category = Category.objects.get(slug=category_name)
                category.save()

                page.category = category
                subcategory = Subcategory.objects.get(
                    slug=product1.subcategory)
                brand = Brand.objects.get(slug=subcategory.brand)
                page.brand = brand

                page.save()

                product1.page.add(page)
                product2.page.add(page)
                product1.save()
                product2.save()

                print("Page {} has been created.".format(pageSlug))

            debug("Page", 0, "Pages for category {} have been created successfully".format(
                category_name))

    def clean(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
        Subcategory.objects.all().delete()

    def deletebuggy(self):
        products = Product.objects.values('sku', 'subcategory')
        for product in products:
            if "not-specified" in product['subcategory']:
                buggyProduct = Product.objects.get(sku=product['sku'])
                buggyProduct.delete()

                print("Buggy product SKU: {}, Subcategory: {} has been deleted".format(
                    product['sku'], product['subcategory']))

        subcategories = Subcategory.objects.values('slug')
        for subcategory in subcategories:
            if "not-specified" in subcategory['slug']:
                buggySubcategory = Subcategory.objects.get(
                    slug=subcategory['slug'])
                buggySubcategory.delete()

                print("Buggy Subcategory Slug: {} has been deleted".format(
                    subcategory['slug']))

        pages = Page.objects.values('slug', 'product')
        for page in pages:
            if page['product'] == None or len(page['product']) == 0:
                buggyPage = Page.objects.get(slug=page['slug'])
                buggyPage.delete()

                print("Buggy Page Slug: {} has been deleted".format(
                    page['slug']))

    def updateRankAndRelPrice(self):
        categories = Category.objects.all()

        for category in categories:
            debug("Page", 0, "Updating page ranks in Category: {}".format(category))

            pages = Page.objects.filter(category=category).annotate(
                product_num=Count('product')).order_by('-product_num')

            brands = []
            rank_category = 0
            for page in pages:
                rank_category += 1
                page.pre_category_rank = rank_category
                page.rel_Brownells = round(random.uniform(1, 2), 2)
                page.rel_Palmetto = round(random.uniform(1, 2), 2)
                page.rel_EuroOptic = round(random.uniform(1, 2), 2)
                page.rel_Gritr = round(random.uniform(1, 2), 2)
                page.rel_Guns = round(random.uniform(1, 2), 2)
                page.rel_PrimaryArms = round(random.uniform(1, 2), 2)
                page.rel_Sportsman = round(random.uniform(1, 2), 2)
                page.save()

                if page.brand not in brands:
                    brands.append(page.brand)

            for brand in brands:
                debug("Page", 0, "Updating page ranks in Category: {}, Brand: {}".format(
                    category, brand))

                pages = Page.objects.filter(category=category, brand=brand).annotate(
                    product_num=Count('product')).order_by('-product_num')

                rank_brand = 0
                for page in pages:
                    rank_brand += 1
                    page.pre_brand_rank = rank_brand
                    page.save()
