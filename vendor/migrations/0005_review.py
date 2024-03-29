# Generated by Django 4.1.3 on 2023-03-08 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_page_rel_brownells_page_rel_eurooptic_page_rel_gritr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('review', models.TextField(blank=True, default=None, max_length=5000, null=True)),
                ('stat_acc', models.IntegerField(blank=True, default=-1, null=True)),
                ('stat_erg', models.IntegerField(blank=True, default=-1, null=True)),
                ('stat_ftr', models.IntegerField(blank=True, default=-1, null=True)),
                ('stat_fit', models.IntegerField(blank=True, default=-1, null=True)),
                ('stat_rel', models.IntegerField(blank=True, default=-1, null=True)),
                ('stat_val', models.IntegerField(blank=True, default=-1, null=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page', to='vendor.page')),
            ],
        ),
    ]
