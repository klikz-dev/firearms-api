# Generated by Django 4.1.3 on 2023-02-27 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_page_stat_acc_page_stat_erg_page_stat_fit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='rel_Brownells',
        ),
        migrations.RemoveField(
            model_name='page',
            name='rel_EuroOptic',
        ),
        migrations.RemoveField(
            model_name='page',
            name='rel_Gritr',
        ),
        migrations.RemoveField(
            model_name='page',
            name='rel_Guns',
        ),
        migrations.RemoveField(
            model_name='page',
            name='rel_Palmetto',
        ),
        migrations.RemoveField(
            model_name='page',
            name='rel_PrimaryArms',
        ),
        migrations.RemoveField(
            model_name='page',
            name='rel_Sportsman',
        ),
    ]