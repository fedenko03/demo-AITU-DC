# Generated by Django 3.2.16 on 2023-02-06 18:59

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
                ('name', models.CharField(max_length=15)),
                ('category', models.CharField(choices=[('Staff only', 'Staff only'), ('For everyone', 'For everyone')], max_length=15)),
                ('is_occupied', models.BooleanField(default=False)),
                ('is_visible', models.BooleanField(default=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customuser')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='SettingsKeyTaking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_code', models.CharField(max_length=100)),
                ('code_timestamp', models.DateTimeField(blank=True, null=True)),
                ('is_confirm', models.BooleanField(default=False)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='keytaking.room')),
            ],
            options={
                'verbose_name': 'Settings KeyTaking',
                'verbose_name_plural': 'Settings KeyTaking',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('Student', 'Student'), ('Professor', 'Professor'), ('Other', 'Other')], max_length=32)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_return', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='keytaking.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customuser')),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'History',
            },
        ),
    ]
