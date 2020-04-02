import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

import django
django.setup()

from gamer_view.models import Category ,Page

def clean():
    Category.objects.all().delete()
    Page.objects.all().delete()

def add_cat(name):
    c=Category.objects.get_or_create(category=name)[0]
    c.save()

def add_page(name, cat,date, desc, image,views):
    page=Page.objects.get_or_create(gamename=name, cat=cat,date_created=date, description=desc, image=image, views=views)[0]
    page.save()
    return page

def populate():

    #list of categories
    category=['FPS', 'MOBA', 'Action', 'MMORPG', 'Strategy', 'Sport', 'Simulator']

    #list of games
    games= [{'gamename': 'Call Of Duty', 'category':'FPS','date': '2018-07-10','description': "shoot people",'image': 'game_images/cod.jfif','views':'5'},
            {'gamename': 'League of Legends', 'category':'MOBA','date': '2012-03-20','description': "destroy towers",'image': 'game_images/lol.jpg','views':'50'},
            {'gamename': 'BattleField', 'category':'FPS','date': '2019-09-29','description': "shoot people 2",'image': 'game_images/bat.jpg','views':'10'},
            {'gamename': 'MonsterHunter', 'category':'Action','date': '2020-01-12','description': "Hunt monsters",'image': 'game_images/MH.jfif','views':'15'},
            {'gamename': 'Dark Souls', 'category':'Action','date': '2011-12-1','description': "Gather souls",'image': 'game_images/ds.jpg','views':'30'},
            {'gamename': 'Fifa 18', 'category':'Sport','date': '2018-11-29','description': "Score goals",'image': 'game_images/fifa.jpg','views':'8'},
            {'gamename': 'Bloons Tower Defense', 'category':'Strategy','date': '2010-02-26','description': "Pop balloons and defend base",'image': 'game_images/btd.jpg','views':'20'},
            {'gamename': 'World of Warcraft', 'category':'MMORPG','date': '2005-04-10','description': "Go on a legendary adventure",'image': 'game_images/wow.jpg','views':'40'},
            {'gamename': 'Dota 2', 'category':'MOBA','date': '2015-05-6','description': "destroy towers 2",'image': 'game_images/dota.jpg','views':'35'},
            {'gamename': 'Animal Crossing', 'category':'Simulator','date': '2020-03-10','description': "Making a Village",'image': 'game_images/ac.jpg','views':'25'}
    ]
    
           
    print("Adding Categories")
    for cat in category:
        add_cat(cat)
        print("Added", cat)

    print("\nAdding Games")
    for game in games:
        category=Category.objects.get(category=game['category'])
        add_page(game['gamename'], category,game['date'], game['description'], game['image'], game['views'])
        print("Added", game['gamename'])

if __name__=='__main__':
    clean()
    print('populating...\n')
    populate()
    print('\n---Finished---')
                  
