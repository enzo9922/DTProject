# Generated by Django 4.2.7 on 2023-11-30 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='items',
            new_name='Item',
        ),
        migrations.RenameModel(
            old_name='participants',
            new_name='Participant',
        ),
        migrations.RenameModel(
            old_name='results',
            new_name='Result',
        ),
    ]
