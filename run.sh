#!/bin/sh

# Production
python3 /home/ubuntu/firearms/firearms/manage.py aero getdata
python3 /home/ubuntu/firearms/firearms/manage.py brownells getdata
python3 /home/ubuntu/firearms/firearms/manage.py daniel getdata
python3 /home/ubuntu/firearms/firearms/manage.py euro getdata
python3 /home/ubuntu/firearms/firearms/manage.py gear1800 getdata
python3 /home/ubuntu/firearms/firearms/manage.py guns getdata
python3 /home/ubuntu/firearms/firearms/manage.py palmetto getdata
python3 /home/ubuntu/firearms/firearms/manage.py primaryarms getdata
python3 /home/ubuntu/firearms/firearms/manage.py sportsmans getdata
python3 /home/ubuntu/firearms/firearms/manage.py vendor product page

# Development
python3 manage.py aero getdata
python3 manage.py brownells getdata
python3 manage.py daniel getdata
python3 manage.py euro getdata
python3 manage.py gear1800 getdata
python3 manage.py guns getdata
python3 manage.py palmetto getdata
python3 manage.py primaryarms getdata
python3 manage.py sportsmans getdata
python3 manage.py vendor product page
