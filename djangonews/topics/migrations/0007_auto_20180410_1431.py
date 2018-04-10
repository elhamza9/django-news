# Generated by Django 2.0.3 on 2018-04-10 14:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0006_auto_20180410_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2018, 4, 10, 14, 31, 54, 314665, tzinfo=utc))),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='topics.Topic', verbose_name='Upvoted Topic')),
                ('upvoter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User who upvoted')),
            ],
            options={
                'db_table': 'upvotes',
            },
        ),
        migrations.AlterField(
            model_name='comment',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 10, 14, 31, 54, 313984, tzinfo=utc)),
        ),
    ]
