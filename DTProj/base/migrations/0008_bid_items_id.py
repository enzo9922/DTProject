# Generated by Django 4.2.2 on 2023-12-06 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='Items_ID',
            field=models.CharField(default='none', max_length=1000),
        ),
    ]
