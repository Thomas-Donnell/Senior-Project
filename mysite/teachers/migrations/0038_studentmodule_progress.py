# Generated by Django 5.0.2 on 2024-04-15 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0037_alter_studentmodule_input_values'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodule',
            name='progress',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]