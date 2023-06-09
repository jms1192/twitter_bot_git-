# Generated by Django 4.1.7 on 2023-04-01 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_remove_shroomapiquery_api_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchain',
            name='shroom_api_query',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.shroomapiquery'),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='active_wallets_24h',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='active_wallets_30d',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='active_wallets_7d',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='avg_transaction_fee_24h',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='avg_transaction_fee_30d',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='avg_transaction_fee_7d',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='total_transactions_24h',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='total_transactions_30d',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='total_transactions_7d',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
