# Generated by Django 4.1.7 on 2023-04-01 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_blockchain_activity_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockchain',
            name='active_wallets_24h',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='active_wallets_30d',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='active_wallets_7d',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='activity_score',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='avg_transaction_fee_24h',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='avg_transaction_fee_30d',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='avg_transaction_fee_7d',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='total_transactions_24h',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='total_transactions_30d',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='total_transactions_7d',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
