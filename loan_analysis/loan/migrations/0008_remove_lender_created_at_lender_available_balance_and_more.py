# Generated by Django 5.0.3 on 2025-03-17 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0007_loanapplication_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lender',
            name='created_at',
        ),
        migrations.AddField(
            model_name='lender',
            name='available_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='lender',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='lender',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lender',
            name='lending_period',
            field=models.IntegerField(default=5, help_text='Lending Period (months)'),
            preserve_default=False,
        ),
    ]
