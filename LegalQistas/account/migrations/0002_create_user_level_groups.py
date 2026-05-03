from django.db import migrations


def create_groups_and_assign_users(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    LawyerProfile = apps.get_model('account', 'LawyerProfile')

    level_0, _ = Group.objects.get_or_create(name='level_0')
    level_1, _ = Group.objects.get_or_create(name='level_1')
    level_2, _ = Group.objects.get_or_create(name='level_2')

    lawyer_user_ids = set(LawyerProfile.objects.values_list('user_id', flat=True))

    for user in User.objects.all():
        if user.is_superuser or user.is_staff:
            user.groups.add(level_2)
        elif user.pk in lawyer_user_ids:
            user.groups.add(level_1)
        else:
            user.groups.add(level_0)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['level_0', 'level_1', 'level_2']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_assign_users, reverse_code=remove_groups),
    ]
