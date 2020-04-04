import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

import django
django.setup()

from gamer_view.models import Category ,Page, UserProfile, User ,Review

# Cleans the Database
def clean():
    Category.objects.all().delete()
    Page.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.all().delete()
    Review.objects.all().delete()

# function that adds categories
def add_cat(name):
    cat=Category.objects.get_or_create(category=name)[0]
    cat.save()
    
# function that adds games
def add_page(name, cat,date, desc, image,views):
    page=Page.objects.get_or_create(gamename=name, cat=cat,date_created=date, description=desc, image=image, views=views)[0]
    page.save()

# function that adds users
def add_user(username, pas, email):
    user=User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(pas)
    user.save()
    return user

# function that creates user profiles
def create_profile(name, image):
    user_prof= UserProfile.objects.get_or_create(user=name, picture=image)[0]
    user_prof.save()

## function that adds reviews
def add_review(game, review, user, date, rating):
    rev=Review.objects.get_or_create(gamename=game, review=review, madeby=user, datecreated=date, rating=rating)[0]
    rev.save()



def populate():

    #list of Categories
    category=['FPS', 'MOBA', 'Action', 'MMORPG', 'Strategy', 'Sport', 'Simulator', 'Racing']

    #list of Games
    games= [{'gamename': 'CallOfDuty', 'category':'FPS','date': '2018-07-10','description': "shoot people",'image': 'game_images/cod.jfif','views':'5'},
            {'gamename': 'BattleField', 'category':'FPS','date': '2019-09-29','description': "shoot people 2",'image': 'game_images/bat.jpg','views':'10'},
            {'gamename': 'CSGO', 'category':'FPS','date': '2014-02-03','description': "shoot people 3",'image': 'game_images/csgo.jfif','views':'18'},
            {'gamename': 'LeagueOfLegends', 'category':'MOBA','date': '2012-03-20','description': "destroy towers",'image': 'game_images/lol.jpg','views':'50'},
            {'gamename': 'Dota2', 'category':'MOBA','date': '2015-05-06','description': "destroy towers 2",'image': 'game_images/dota.jpg','views':'35'},
            {'gamename': 'Smite', 'category':'MOBA','date': '2016-08-15','description': "destroy towers 3",'image': 'game_images/smite.jpg','views':'30'},
            {'gamename': 'MonsterHunter', 'category':'Action','date': '2020-01-12','description': "Hunt monsters",'image': 'game_images/MH.jfif','views':'45'},
            {'gamename': 'DarkSouls', 'category':'Action','date': '2011-12-01','description': "Gather souls",'image': 'game_images/ds.jpg','views':'30'},
            {'gamename': 'TheWitcher3', 'category':'Action','date': '2018-04-23','description': "Story driven",'image': 'game_images/witcher.jfif','views':'40'},
            {'gamename': 'Fifa18', 'category':'Sport','date': '2018-11-29','description': "Play Football",'image': 'game_images/fifa.jpg','views':'8'},
            {'gamename': 'NBA2K20', 'category':'Sport','date': '2019-12-23','description': "Play Basketball",'image': 'game_images/nba.jfif','views':'24'},
            {'gamename': 'BloonsTowerDefense', 'category':'Strategy','date': '2010-02-26','description': "Pop balloons and defend base",'image': 'game_images/btd.jpg','views':'20'},
            {'gamename': 'Hearthstone', 'category':'Strategy','date': '2016-05-03','description': "Turn based card game",'image': 'game_images/hearthstone.jpg','views':'28'},
            {'gamename': 'WorldOfWarcraft', 'category':'MMORPG','date': '2005-04-10','description': "Go on a legendary adventure",'image': 'game_images/wow.jpg','views':'40'},
            {'gamename': 'AnimalCrossing', 'category':'Simulator','date': '2020-03-10','description': "Making a Village",'image': 'game_images/ac.jpg','views':'25'}]

    #list of Users
    users= [{'username': 'Sheldon', 'password': 'password1', 'image': 'profile_images/user1.png','email' : "user1@gmail.com"},
            {'username': 'Abigail', 'password': 'password1', 'image': 'profile_images/user2.png','email' : "user2@gmail.com"},
            {'username': 'Ben', 'password': 'password1', 'image': 'profile_images/user3.jfif','email' : "user3@gmail.com"},
            {'username': 'Adam', 'password': 'password1', 'image': 'profile_images/user4.jfif','email' : "user4@gmail.com"},
            {'username': 'Katy', 'password': 'password1', 'image': 'profile_images/user5.png','email' : "user5@gmail.com"},]

    #list of Reviews
    reviews=[{'gamename': 'BloonsTowerDefense', 'review' : 'A good game for passing time and does not require much attention','madeby':'Sheldon', 'date':'2011-01-30', 'rating': '3'},
             {'gamename': 'AnimalCrossing', 'review' : 'An excellent game to escape reality','madeby':'Abigail', 'date':'2020-04-01', 'rating': '4'},
             {'gamename': 'MonsterHunter', 'review' : 'Never gets boring due to the constant new free DLCs','madeby':'Adam', 'date':'2020-02-18', 'rating': '5'},
             {'gamename': 'DarkSouls', 'review' : 'Quiet a lot of exploring and has intresting boss fights','madeby':'Sheldon', 'date':'2011-01-30', 'rating': '4'}]

           
    print("Adding Categories")
    for cat in category:
        add_cat(cat)
        print("Category:", cat)

    print("\nAdding Games")
    for game in games:
        category=Category.objects.get(category=game['category'])
        add_page(game['gamename'], category ,game['date'], game['description'], game['image'], game['views'])
        print("Game:", game['gamename'])

    print("\nAdding Users")
    for user in users:
        name=add_user(user['username'], user['password'],user['email'])
        create_profile(name, user['image'])
        print("User:", user['username'])

    print("\nAdding Reviews")
    for review in reviews:
        game=Page.objects.get(gamename=review['gamename'])
        user=UserProfile.objects.get(user__username=review['madeby'])
        add_review(game, review['review'], user, review['date'], review['rating'])
        print("Review for", game, "added")
        
            
if __name__=='__main__':
    print('\nPopulating gamer_view database...\n')
    clean()
    populate()
    print('\n---Finished---')
                  
