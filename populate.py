from topics.models import User, Topic
from django.utils import timezone

import os
import random
import datetime

User.objects.all().delete()

dummy_user = User.objects.create_user(username=os.environ.get('DUMMY_USER'), password=os.environ.get('DUMMY_PASS'))

tz = timezone.get_current_timezone()

f = open('../../lorem.txt', 'r')
if f.mode == 'r':
    text = f.read()
else:
    text = 'nothing'

Topic.objects.all().delete()


for i in range(100):
    t = Topic()
    day = random.randrange(1,30)
    month = random.randrange(1,12)
    year = 2010 + random.randrange(1,8)
    date = datetime.date(year,month,day)
    time = datetime.time(8,0,tzinfo=timezone.get_current_timezone())
    t.published_at = datetime.datetime.combine(date,time)
    t.title = 'New Article {}/{}/{}'.format(day,month,year)
    t.slug = 'new-article-{}-{}-{}'.format(day,month,year)
    t.content = text
    t.author = dummy_user
    Topic.save(t)

