# Generated by Django 4.2.2 on 2023-12-06 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_item_items_id_participant_iditems_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.participant')),
            ],
        ),
    ]
