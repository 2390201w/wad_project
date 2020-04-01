import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

import django
django.setup()

from gamer_view.models import Category
from datetime import datetime
from PIL import Image

def add_cat(name):
    c=Category.objects.get_or_create(category=name)[0]
    c.save()
    return c

def add_page(name, cat, date, desc, image,views):
    page-Page.objects.get_or_create(gamename=name, category=cat, time_created=date, description=desc, image=image, views=views)
    page.save()
    return page

def populate():
    category=['FPS', 'MOBA', 'Action', 'MMORPG', 'Strategy', 'Sport']
    games= [{'gamename': 'Call Of Duty', 'category': 'FPS','date': 'datetime.now()','description': "shoot people",'image': 'game_images/cod.jfif','views':'5'},
            {'gamename': 'League of Legends', 'category': 'MOBA','date': 'datetime.now()','description': "destroy towers",'image': 'game_images/lol.jpg','views':'20'},
            {'gamename': 'BattleField', 'category': 'FPS','date': 'datetime.now()','description': "shoot people 2",'image': 'game_images/bat.jpg','views':'10'}]
            
    print("Adding categories")
    for cat in category:
        add_cat(cat)
        print("Added", cat)

    print("Adding games")
    for game in games:
        add_page(game['gamename'], game['category'], game['date'], game['description'], game['image'], game['views'])
        print("Added", game[gamename])

if __name__=='__main__':
    print('populating...')
    populate()
                  
