# Generated by Django 3.2.9 on 2023-03-01 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('floor', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default='1', max_length=2)),
                ('is_occupied', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('map_id', models.CharField(blank=True, max_length=45, null=True)),
                ('role', models.ManyToManyField(blank=True, null=True, to='user.Role')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='SettingsKeyTaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_code', models.CharField(max_length=100)),
                ('code_timestamp', models.DateTimeField(blank=True, null=True)),
                ('is_confirm', models.BooleanField(default=False)),
                ('in_process', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('QR', 'QR'), ('Manually', 'Manually')], default='Manually', max_length=10)),
                ('step', models.IntegerField(default=1)),
                ('error', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='keytaker.room')),
            ],
            options={
                'verbose_name': 'Settings KeyTaker',
                'verbose_name_plural': 'Settings KeyTaker',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_code', models.CharField(max_length=100)),
                ('note', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('orders_timestamp', models.DateTimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('is_confirm', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keytaker.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.mainuser')),
            ],
            options={
                'verbose_name': 'Orders',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_return', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.role')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='keytaker.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.mainuser')),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'History',
            },
        ),
    ]
