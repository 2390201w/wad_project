import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

import django
django.setup()

from gamer_view.models import Category

def populate():
    FPS= [{'title': 'Call Of Duty'}]
    category={'FPS': {'pages': FPS}}

    for cat, data in category.items():
        c=add_cat(cat)
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'-{c}:{p}')

def add_cat(name):
    c=Category.objects.get_or_create(category=name)[0]
    c.save()
    return c

if __name__=='__main__':
    print('populating...')
    populate()
                  
