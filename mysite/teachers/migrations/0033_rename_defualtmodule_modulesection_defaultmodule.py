# Generated by Django 5.0.2 on 2024-03-29 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0032_modulesection_defualtmodule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modulesection',
            old_name='defualtModule',
            new_name='defaultModule',
        ),
    ]