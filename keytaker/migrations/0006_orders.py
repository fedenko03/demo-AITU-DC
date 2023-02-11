# Generated by Django 3.2.16 on 2023-02-10 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('keytaker', '0005_rename_category_room_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_code', models.CharField(max_length=100)),
                ('note', models.CharField(default='', max_length=100)),
                ('orders_timestamp', models.DateTimeField()),
                ('is_available', models.BooleanField(default=False)),
                ('is_confirm', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keytaker.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.mainuser')),
            ],
        ),
    ]
