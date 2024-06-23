# Generated by Django 5.0.4 on 2024-06-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_repository_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]