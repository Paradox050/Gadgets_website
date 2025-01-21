# Generated by Django 5.1.2 on 2024-11-11 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock',
            new_name='stock_4gb_128gb',
        ),
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='ram',
            field=models.CharField(choices=[('4GB', '4GB'), ('8GB', '8GB')], default='4GB', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_4gb_1tb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_4gb_256gb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_4gb_512gb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_8gb_128gb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_8gb_1tb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_8gb_256gb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_8gb_512gb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='storage',
            field=models.CharField(choices=[('128GB', '128GB'), ('256GB', '256GB'), ('512GB', '512GB'), ('1TB', '1TB')], default='128GB', max_length=20),
        ),
    ]
