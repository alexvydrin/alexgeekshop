# Generated by Django 3.0.8 on 2020-09-15 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активен'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активная'),
        ),
    ]
