# Generated by Django 2.2.5 on 2019-09-06 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20190906_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='flat_number',
            new_name='flat',
        ),
    ]
