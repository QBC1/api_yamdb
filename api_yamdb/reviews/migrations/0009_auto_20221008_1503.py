# Generated by Django 2.2.16 on 2022-10-08 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20220830_0656'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['role'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
