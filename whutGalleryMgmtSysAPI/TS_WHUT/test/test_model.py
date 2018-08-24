import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TS_WHUT.settings")

import django
django.setup()

from django.db.models import Q
from images.models import ImageModel, Groups, SmallGroups, GroupImage


def main():
    obj = Groups.objects.filter(id=1)[0]
    groups = SmallGroups.objects.filter(group=obj)
    q = Q()
    q.connector = 'OR'

    for group in groups:
        q.children.append(('group', group))

    page = GroupImage.objects.filter(q)
    page = ImageModel.objects.filter(groupimage__in=page, if_active=True)
    return page

main()
