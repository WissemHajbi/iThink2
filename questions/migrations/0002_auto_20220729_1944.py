# Generated by Django 3.2.7 on 2022-07-29 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='poll',
            field=models.IntegerField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='question',
            field=models.IntegerField(blank=True, max_length=20, null=True),
        ),
    ]