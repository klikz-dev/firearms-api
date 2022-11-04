from django.core.management.base import BaseCommand
from feed.models import AeroPrecision

import sys
import os
import csv
import codecs

from library import debug, common

debug = debug.debug

FILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    help = 'Build AeroPrecision Database'

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        if "getdata" in options['functions']:
            self.getData()

    def getData(self):
        debug("AeroPrecision", 0, "Start Processing AeroPrecision Data Feed")

        if common.filedownload(
                "http://datafeed.avantlink.com/download_feed.php?id=290501&auth=45be2e0bb44175e8729e235882ad17a5", "AeroPrecision.csv") == False:
            sys.exit(1)

        fileSize = os.stat(FILEDIR + "/files/AeroPrecision.csv").st_size
        if fileSize < 1000:
            sys.exit(1)

        AeroPrecision.objects.all().delete()

        f = open(FILEDIR + "/files/AeroPrecision.csv", "rb")
        cr = csv.reader(codecs.iterdecode(f, encoding="ISO-8859-1"))

        for row in cr:
            if row[0] == 'SKU':
                continue

            try:
                product = AeroPrecision.objects.create(
                    sku=row[0],
                )
            except Exception as e:
                print(e)
                debug("AeroPrecision", 1,
                      "Failed Creating Product Object for SKU: {}".format(row[0]))
                continue

            product.manufacturer_id = row[1]
            product.brand_name = row[2]
            product.product_name = row[3]
            product.long_description = row[4]
            product.short_description = row[5]
            product.category = row[6]
            product.sub_category = row[7]
            product.product_group = row[8]
            product.thumb_url = row[9]
            product.image_url = row[10]
            product.buy_link = row[11]
            product.keywords = row[12]
            product.reviews = row[13]
            try:
                product.retail_price = float(row[14])
            except:
                pass
            try:
                product.sale_price = float(row[15])
            except:
                pass
            product.brand_page_link = row[16]
            product.brand_logo_image = row[17]
            product.tracking = row[18]

            product.quantity = -1

            product.medium_image_url = row[19]

            product.content_widget = row[20]

            product.google_categorization = row[21]
            try:
                product.commission = float(row[22])
            except:
                pass

            if product.sale_price == 0 or product.image_url == "" or product.buy_link == "" or len(product.category) > 50 or len(product.brand_name) > 50:
                product.delete()
                continue

            try:
                product.save()
            except Exception as e:
                print(e)
                continue

        debug("AeroPrecision", 0, "Completed Processing AeroPrecision Data Feed")
