# Generated by Django 3.2.16 on 2023-04-17 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keytaker', '0003_auto_20230417_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]
