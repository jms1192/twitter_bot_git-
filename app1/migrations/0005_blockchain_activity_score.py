# Generated by Django 4.1.7 on 2023-04-01 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_trendingscore_dapp_delete_dapp'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchain',
            name='activity_score',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
    ]
