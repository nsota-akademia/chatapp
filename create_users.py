import os
import random
import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE","chatapp.settings.dev")
django.setup()

from myapp.models import CustomUser,Messages

fakegen = Faker(["ja_JP"])

def create_users(n):
    users = [
        CustomUser(username=fakegen.user_name(),email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]
    
    CustomUser.objects.bulk_create(users,ignore_conflicts=True)
    my_pk = CustomUser.objects.get(username="admin").pk
    user_pks = CustomUser.objects.exclude(pk=my_pk).values_list("id",flat=True)
    
    talks = []
    for _ in range(len(user_pks)):
        sent_talk = Messages(
            message_from = my_pk,
            message_to = random.choice(user_pks),
            message = fakegen.text(),
        )
        received_talk = Messages(
            message_from = random.choice(user_pks),
            message_to = my_pk,
            message=fakegen.text(),
        )
        talks.extend([sent_talk,received_talk])
    Messages.objects.bulk_create(talks,ignore_conflicts=True)
    
    talks = Messages.objects.order_by("-time")[: 2 * len(user_pks)]
    for talk in talks:
        talk.time = fakegen.date_time_this_year(tzinfo = tz.gettz("Asia/Tokyo"))
    Messages.objects.bulk_update(talks,fields=["time"])
    
if __name__ == "__main__":
    print("creating users...",end="")
    create_users(1000)
    print("done")