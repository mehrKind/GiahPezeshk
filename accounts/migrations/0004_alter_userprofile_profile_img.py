# Generated by Django 5.1.4 on 2024-12-09 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_country_alter_userprofile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(blank=True, default='userProfile/default.png', upload_to='userProfile/'),
        ),
    ]