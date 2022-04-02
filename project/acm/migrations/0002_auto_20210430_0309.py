# Generated by Django 2.2.19 on 2021-04-30 03:09

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acm', '0001_initial'),
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolspage',
            name='schools',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='widgets.School'),
        ),
        migrations.AddField(
            model_name='programspage',
            name='programs',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='acm.Program'),
        ),
        migrations.AddField(
            model_name='program',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document', verbose_name='Fichier'),
        ),
    ]