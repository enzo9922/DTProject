# Generated by Django 4.2.7 on 2024-01-16 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_rename_idparticipant_bidding_idparticipants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidding',
            name='item11',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bidding',
            name='item12',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bidding',
            name='item13',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bidding',
            name='item14',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bidding',
            name='item15',
            field=models.IntegerField(default=0),
        ),
    ]
