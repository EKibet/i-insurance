# Generated by Django 3.1.3 on 2020-11-16 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0004_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
