# Generated by Django 3.2.16 on 2023-05-21 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_create_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='auth_token',
            field=models.CharField(default='g5g4dfgh', max_length=100),
        ),
    ]