# Generated by Django 2.2.5 on 2019-11-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20190912_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='flat',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
    ]
