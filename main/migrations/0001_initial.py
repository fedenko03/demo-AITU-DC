from django.db import migrations, models


def create_initial_pin(apps, schema_editor):
    PIN = apps.get_model('main', 'PIN')
    PIN.objects.create(code='your_code_here', is_locked=False)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PIN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=15)),
                ('is_locked', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'PIN code',
                'verbose_name_plural': 'PIN code',
            },
        ),
        migrations.RunPython(create_initial_pin),
    ]
