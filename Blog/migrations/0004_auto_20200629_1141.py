# Generated by Django 3.0.7 on 2020-06-29 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='message',
        ),
    ]