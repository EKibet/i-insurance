# Generated by Django 3.1.3 on 2020-11-16 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0003_auto_20201116_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
