# Generated by Django 5.1.4 on 2024-12-18 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialist',
            name='experience_years',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]