# Generated by Django 3.0.8 on 2020-08-02 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='short_desc',
            new_name='short_descexit',
        ),
        migrations.AddField(
            model_name='product',
            name='image_small',
            field=models.ImageField(blank=True, upload_to='products_images/small'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products_images/big'),
        ),
    ]
