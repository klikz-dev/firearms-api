from django.core.management.base import BaseCommand
from feed.models import DanielDefense

import sys
import os
import csv
import codecs

from library import debug, common

debug = debug.debug

FILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    help = 'Build DanielDefense Database'

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        if "getdata" in options['functions']:
            self.getData()

    def getData(self):
        debug("DanielDefense", 0, "Start Processing DanielDefense Data Feed")

        if common.filedownload(
                "http://datafeed.avantlink.com/download_feed.php?id=290369&auth=45be2e0bb44175e8729e235882ad17a5", "DanielDefense.csv") == False:
            sys.exit(1)

        fileSize = os.stat(FILEDIR + "/files/DanielDefense.csv").st_size
        if fileSize < 1000:
            sys.exit(1)

        DanielDefense.objects.all().delete()

        f = open(FILEDIR + "/files/DanielDefense.csv", "rb")
        cr = csv.reader(codecs.iterdecode(f, encoding="ISO-8859-1"))

        for row in cr:
            if row[0] == 'SKU':
                continue

            try:
                product = DanielDefense.objects.create(
                    sku=row[0],
                )
            except Exception as e:
                print(e)
                debug("DanielDefense", 1,
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
            product.parent_group = row[19]
            product.color = row[20]
            product.size = row[21]
            product.pattern = row[22]
            product.material = row[23]
            try:
                product.weight = float(row[24])
            except:
                pass
            product.age_group = row[25]
            product.gender = row[26]
            product.upc = row[27]
            product.gtin = row[28]
            product.guid = row[30]

            product.sale_price_effective_date = row[31]
            if row[32] == "False":
                product.availability = False
            if row[33] == "False":
                product.visibility = False

            product.model_number = row[34]
            try:
                if row[35] == '':
                    product.quantity = -1
                else:
                    product.quantity = int(row[35])
            except:
                pass
            product.alternative_buy_link = row[36]
            product.alternative_product_id = row[37]
            product.alternative_image_id = row[38]
            product.medium_image_url = row[39]
            product.content_widget = row[40]

            product.google_categorization = row[41]
            try:
                product.commission = float(row[42])
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

        debug("DanielDefense", 0, "Completed Processing DanielDefense Data Feed")
