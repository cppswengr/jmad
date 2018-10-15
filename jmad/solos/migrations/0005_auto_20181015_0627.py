# Generated by Django 2.1.2 on 2018-10-15 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solos', '0004_solo_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solo',
            name='album',
        ),
        migrations.AlterField(
            model_name='solo',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.Track'),
        ),
    ]