# Generated by Django 5.0.4 on 2024-05-09 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_rename_user_id_repository_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
