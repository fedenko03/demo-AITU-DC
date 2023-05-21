from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model('user', 'Role')  # Замените 'user' на имя вашего приложения Django, содержащего модель Role
    Role.objects.bulk_create([
        Role(name='Student'),
        Role(name='Professor'),
        Role(name='Personal'),
        Role(name='Other')
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_mainuser_role'),  # Замените 'user' на имя вашего приложения Django
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
