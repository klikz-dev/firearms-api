# Generated by Django 4.1.3 on 2023-02-27 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_remove_page_rel_brownells_remove_page_rel_eurooptic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='rel_Brownells',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='rel_EuroOptic',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='rel_Gritr',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='rel_Guns',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='rel_Palmetto',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='rel_PrimaryArms',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='rel_Sportsman',
            field=models.FloatField(blank=True, default=1.5, null=True),
        ),
    ]
