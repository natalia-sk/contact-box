# Generated by Django 2.2.5 on 2019-09-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20190906_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='house',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
