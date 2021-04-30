# Generated by Django 2.2.4 on 2021-04-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('godzilla_app', '0003_message_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ManyToManyField(related_name='movies', to='godzilla_app.User')),
            ],
        ),
    ]
