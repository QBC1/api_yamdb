# Generated by Django 2.2.16 on 2022-08-29 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20220829_2332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['slug']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['slug']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['role']},
        ),
    ]
