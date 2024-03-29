# Generated by Django 4.0.4 on 2022-06-18 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamify', '0003_film_trama'),
    ]

    operations = [
        migrations.AddField(
            model_name='utente',
            name='film_preferiti',
            field=models.ManyToManyField(default=None, related_name='film_preferiti', to='streamify.film'),
        ),
        migrations.AlterField(
            model_name='utente',
            name='film_guardati',
            field=models.ManyToManyField(default=None, related_name='film_guardati', to='streamify.film'),
        ),
    ]
