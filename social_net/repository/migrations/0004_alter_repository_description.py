# Generated by Django 5.0.4 on 2024-05-09 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_alter_repository_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
