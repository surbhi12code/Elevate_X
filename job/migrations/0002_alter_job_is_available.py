# Generated by Django 4.2.4 on 2024-02-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]