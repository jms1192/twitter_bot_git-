# Generated by Django 3.2 on 2023-04-06 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20230405_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchaindashboards',
            name='start_string',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
