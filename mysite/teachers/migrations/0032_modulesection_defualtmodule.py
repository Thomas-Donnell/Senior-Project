# Generated by Django 5.0.2 on 2024-03-29 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0031_prefab'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulesection',
            name='defualtModule',
            field=models.CharField(max_length=100, null=True),
        ),
    ]