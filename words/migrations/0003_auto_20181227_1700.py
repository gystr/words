# Generated by Django 2.1.3 on 2018-12-27 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_tag_is_main_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=144, unique=True),
        ),
    ]