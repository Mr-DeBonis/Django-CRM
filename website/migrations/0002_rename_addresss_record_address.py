# Generated by Django 5.0.6 on 2024-06-28 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='addresss',
            new_name='address',
        ),
    ]
