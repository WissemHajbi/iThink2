# Generated by Django 3.2.7 on 2022-07-29 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20220729_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('approved', 'approved'), ('pending', 'pending'), ('disapproved', 'disapproved')], default='disapproved', max_length=11),
        ),
    ]