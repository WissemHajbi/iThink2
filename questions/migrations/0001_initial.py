# Generated by Django 3.2.7 on 2022-05-06 17:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('approved', 'approved'), ('disapproved', 'disapproved')], default='disapproved', max_length=11)),
                ('question', models.CharField(max_length=200)),
                ('creator', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='question_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_str', models.CharField(default='empty', max_length=300)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.user')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='question_answered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answered_question', to='polls.user')),
            ],
        ),
    ]
