# Generated by Django 4.0.4 on 2022-07-04 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamify', '0007_remove_utente_date_joined_remove_utente_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='utente',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='utente',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]