# Generated by Django 3.2.16 on 2023-04-22 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytaker', '0006_auto_20230422_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
