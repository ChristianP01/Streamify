# Generated by Django 4.0.4 on 2022-05-11 14:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamify', '0002_genere_remove_utente_id_alter_utente_username_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='valutazione',
            field=models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='film',
            name='anno_uscita',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1888), django.core.validators.MaxValueValidator(2022)]),
        ),
    ]