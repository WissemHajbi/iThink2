# Generated by Django 3.2.7 on 2022-03-16 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answered',
            name='answer',
            field=models.CharField(max_length=1000),
        ),
    ]
