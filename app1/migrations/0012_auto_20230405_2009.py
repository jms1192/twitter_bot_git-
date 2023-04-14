# Generated by Django 3.2 on 2023-04-06 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_auto_20230404_2225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blockchaindashboards',
            old_name='description',
            new_name='f_string',
        ),
        migrations.AddField(
            model_name='blockchaindashboards',
            name='shroom_api_query',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.shroomapiquery'),
        ),
        migrations.AddField(
            model_name='blockchaindashboards',
            name='twitter_bot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.twitterbot'),
        ),
    ]
