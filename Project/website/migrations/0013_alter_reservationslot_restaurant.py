# Generated by Django 3.2 on 2021-05-03 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_reservationslot_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationslot',
            name='restaurant',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='website.restaurant'),
        ),
    ]
