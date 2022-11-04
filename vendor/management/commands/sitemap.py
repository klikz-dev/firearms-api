from django.core.management.base import BaseCommand

from vendor.models import Brand, Category, Page, Subcategory

import os
import ftplib

from library import debug

debug = debug.debug

FILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    help = 'Build Product Database'

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        if "category" in options['functions']:
            self.category()
        if "brand" in options['functions']:
            self.brand()
        if "subcategory" in options['functions']:
            self.subcategory()
        if "product" in options['functions']:
            self.product()
        if "popularCategory" in options['functions']:
            self.popularCategory()
        if "popularBrand" in options['functions']:
            self.popularBrand()

    def category(self):
        if os.path.isfile(FILEDIR + "/files/category.xml"):
            os.remove(FILEDIR + "/files/category.xml")
        f = open(FILEDIR + "/files/category.xml", "w+")

        f.write('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="https://www.americanfirearms.org/sitemaps_xsl.xsl"?>')
        f.write('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url>')
        f.write('<loc>https://www.americanfirearms.org</loc></url>')

        categories = Category.objects.values('slug', 'updated_at')
        for category in categories:
            try:
                f.write('<url>')
                f.write(
                    '<loc>https://www.americanfirearms.org/shop/categories/{}/</loc>'.format(category['slug']))
                f.write(
                    '<lastmod>{}</lastmod>'.format(category['updated_at'].strftime('%Y-%m-%d')))
                f.write('</url>')
                print("Wrote Category Sitemap for {}".format(category['slug']))
            except Exception as e:
                print(e)
                continue

        f.write('</urlset>')
        f.close()

        self.upload(FILEDIR + "/files/category.xml", "category.xml")

        debug("Sitemap", 0, "Category sitemap has been generated")

    def brand(self):
        if os.path.isfile(FILEDIR + "/files/brand.xml"):
            os.remove(FILEDIR + "/files/brand.xml")
        f = open(FILEDIR + "/files/brand.xml", "w+")

        f.write('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="https://www.americanfirearms.org/sitemaps_xsl.xsl"?>')
        f.write('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url>')
        f.write('<loc>https://www.americanfirearms.org</loc></url>')

        brands = Brand.objects.values('slug', 'updated_at')
        for brand in brands:
            if brand['slug'] == "":
                continue

            try:
                f.write('<url>')
                f.write(
                    '<loc>https://www.americanfirearms.org/shop/brands/{}/</loc>'.format(brand['slug']))
                f.write(
                    '<lastmod>{}</lastmod>'.format(brand['updated_at'].strftime('%Y-%m-%d')))
                f.write('</url>')
                print("Wrote Category Sitemap for {}".format(brand['slug']))
            except Exception as e:
                print(e)
                continue

        f.write('</urlset>')
        f.close()

        self.upload(FILEDIR + "/files/brand.xml", "brand.xml")

        debug("Sitemap", 0, "Brand sitemap has been generated")

    def subcategory(self):
        if os.path.isfile(FILEDIR + "/files/subcategory.xml"):
            os.remove(FILEDIR + "/files/subcategory.xml")
        f = open(FILEDIR + "/files/subcategory.xml", "w+")

        f.write('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="https://www.americanfirearms.org/sitemaps_xsl.xsl"?>')
        f.write('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url>')
        f.write('<loc>https://www.americanfirearms.org</loc></url>')

        subcategories = Subcategory.objects.all()
        for subcategory in subcategories:
            brand = subcategory.brand
            try:
                f.write('<url>')
                f.write(
                    '<loc>https://www.americanfirearms.org/shop/{}/{}/</loc>'.format(brand.slug, subcategory.slug))
                f.write(
                    '<lastmod>{}</lastmod>'.format(subcategory.updated_at.strftime('%Y-%m-%d')))
                f.write('</url>')
                print(
                    "Wrote Category Sitemap for {}/{}".format(brand.slug, subcategory.slug))
            except Exception as e:
                print(e)
                continue

        f.write('</urlset>')
        f.close()

        self.upload(FILEDIR + "/files/subcategory.xml", "subcategory.xml")

        debug("Sitemap", 0, "Subcategory sitemap has been generated")

    def product(self):
        pages = Page.objects.values('slug', 'updated_at')

        for sitemap_num in range(1, int(len(pages) / 50000) + 2):
            if os.path.isfile(FILEDIR + "/files/product-{}.xml".format(sitemap_num)):
                os.remove(FILEDIR + "/files/product-{}.xml".format(sitemap_num))
            f = open(FILEDIR + "/files/product-{}.xml".format(sitemap_num), "w+")

            f.write('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="https://www.americanfirearms.org/sitemaps_xsl.xsl"?>')
            f.write('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url>')
            f.write('<loc>https://www.americanfirearms.org</loc></url>')

            for page_num in range(50000 * (sitemap_num-1), 50000 * sitemap_num - 1):
                try:
                    page = pages[page_num]
                except:
                    break

                try:
                    f.write('<url>')
                    f.write(
                        '<loc>https://www.americanfirearms.org/shop/{}/</loc>'.format(page['slug']))
                    f.write(
                        '<lastmod>{}</lastmod>'.format(page['updated_at'].strftime('%Y-%m-%d')))
                    f.write('</url>')
                    print("Wrote Product Sitemap for {}".format(page['slug']))
                except Exception as e:
                    print(e)
                    continue

            f.write('</urlset>')
            f.close()

            self.upload(FILEDIR + "/files/product-{}.xml".format(sitemap_num),
                        "product-{}.xml".format(sitemap_num))

        debug("Sitemap", 0, "Product sitemap has been generated")

    def popularCategory(self):
        if os.path.isfile(FILEDIR + "/files/popular-category.xml"):
            os.remove(FILEDIR + "/files/popular-category.xml")
        f = open(FILEDIR + "/files/popular-category.xml", "w+")

        f.write('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="https://www.americanfirearms.org/sitemaps_xsl.xsl"?>')
        f.write('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url>')
        f.write('<loc>https://www.americanfirearms.org</loc></url>')

        categories = Category.objects.all()
        for category in categories:
            pages = Page.objects.filter(category=category)
            if len(pages) < 10:
                continue

            try:
                f.write('<url>')
                f.write(
                    '<loc>https://www.americanfirearms.org/shop/categories/popular/{}/</loc>'.format(category.slug))
                f.write(
                    '<lastmod>{}</lastmod>'.format(category.updated_at.strftime('%Y-%m-%d')))
                f.write('</url>')
                print("Wrote Category Sitemap for {}".format(category.slug))
            except Exception as e:
                print(e)
                continue

        f.write('</urlset>')
        f.close()

        self.upload(FILEDIR + "/files/popular-category.xml",
                    "popular-category.xml")

        debug("Sitemap", 0, "Category sitemap has been generated")

    def popularBrand(self):
        if os.path.isfile(FILEDIR + "/files/popular-brand.xml"):
            os.remove(FILEDIR + "/files/popular-brand.xml")
        f = open(FILEDIR + "/files/popular-brand.xml", "w+")

        f.write('<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="https://www.americanfirearms.org/sitemaps_xsl.xsl"?>')
        f.write('<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url>')
        f.write('<loc>https://www.americanfirearms.org</loc></url>')

        brands = Brand.objects.all()
        for brand in brands:
            pages = Page.objects.filter(brand=brand)
            if len(pages) < 10 or brand.slug == "":
                continue

            try:
                f.write('<url>')
                f.write(
                    '<loc>https://www.americanfirearms.org/shop/brands/popular/{}/</loc>'.format(brand.slug))
                f.write(
                    '<lastmod>{}</lastmod>'.format(brand.updated_at.strftime('%Y-%m-%d')))
                f.write('</url>')
                print("Wrote brand Sitemap for {}".format(brand.slug))
            except Exception as e:
                print(e)
                continue

        f.write('</urlset>')
        f.close()

        self.upload(FILEDIR + "/files/popular-brand.xml",
                    "popular-brand.xml")

        debug("Sitemap", 0, "brand sitemap has been generated")

    def upload(self, file, filename):
        session = ftplib.FTP('americanfirearms.org',
                             'murrell@americanfirearms.org', 'Ldm.8.17')
        session.encoding = "utf-8"
        session.cwd('/americanfirearms.org/public_html/sitemaps/')

        with open(file, "rb") as data:
            session.storbinary(f"STOR {filename}", data)

        debug("Sitemap", 0, "Uploaded {}/{}".format(session.pwd(), filename))
        session.quit()
