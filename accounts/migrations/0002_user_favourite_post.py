# Generated by Django 3.2.4 on 2021-06-17 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microposts', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_post',
            field=models.ManyToManyField(blank=True, to='microposts.Post', verbose_name='お気に入りの投稿'),
        ),
    ]
