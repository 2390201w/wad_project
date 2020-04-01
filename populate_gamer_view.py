import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

import django
django.setup()

from gamer_view.models import Category ,Page
from datetime import datetime
from PIL import Image

def add_cat(name):
    c=Category.objects.get_or_create(category=name)[0]
    c.save()

def add_page(name, cat, desc, image,views):
    page=Page.objects.get_or_create(gamename=name, cat=cat, description=desc, image=image, views=views)[0]
    page.save()
    return page

def populate():
    category=['FPS', 'MOBA', 'Action', 'MMORPG', 'Strategy', 'Sport']
    games= [{'gamename': 'Call Of Duty', 'category':'FPS','description': "shoot people",'image': 'game_images/cod.jfif','views':'5'},
            {'gamename': 'League of Legends', 'category':'MOBA','description': "destroy towers",'image': 'game_images/lol.jpg','views':'20'},
            {'gamename': 'BattleField', 'category':'FPS','description': "shoot people 2",'image': 'game_images/bat.jpg','views':'10'}]
            
    print("Adding Categories")
    for cat in category:
        add_cat(cat)
        print("Added", cat)

    print("\nAdding Games")
    for game in games:
        category=Category.objects.get(category=game['category'])
        add_page(game['gamename'], category, game['description'], game['image'], game['views'])
        print("Added", game['gamename'])

if __name__=='__main__':
    print('populating...')
    populate()
                  
