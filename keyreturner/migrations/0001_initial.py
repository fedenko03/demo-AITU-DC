# Generated by Django 3.2.16 on 2023-02-15 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingsKeyReturner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('token_timestamp', models.DateTimeField(blank=True, null=True)),
                ('in_process', models.BooleanField(default=False)),
                ('step', models.IntegerField(default=1)),
                ('error', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.mainuser')),
            ],
            options={
                'verbose_name': 'Settings KeyReturner',
                'verbose_name_plural': 'Settings KeyReturner',
            },
        ),
    ]