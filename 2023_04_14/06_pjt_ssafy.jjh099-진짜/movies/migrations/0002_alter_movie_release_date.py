# Generated by Django 3.2.18 on 2023-03-24 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
