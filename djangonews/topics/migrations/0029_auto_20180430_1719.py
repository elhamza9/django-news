# Generated by Django 2.0.3 on 2018-04-30 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0028_auto_20180430_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='upvote',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]