# WAD_Project

#### Set Up
1. Make sure you have python 3.7.2 and Anaconda 3
2. Clone/ download the project from this repository
3. In Anaconda 3 Prompt, navigate to where the project was saved using `cd [path]/wad_project`
4. Create a virtual enviroment with the command `conda create -n gamer_view python=3.7.2`
5. Activate the virtual enviroment with `conda activate gamer_view`
6. Then install the requirements from the requirements.txt with `pip install -r requirements.txt`

#### Populate database
1. Navigate to the `[path]/wad_project` where `population_script.py` is stored
2. Then, enter the command `python manage.py makemigrations`
3. Next, migrate the database with `python manage.py migrate`
4. Now populate the database with `python population_script.py`

#### Start website
1. Navigate to the `[path]/wad_project` where `manage.py` is stored
2. Use command `python manage.py runserver`
 
#### Admin User
1.  Create an Admin user using the command `python manage.py createsuperuser` and enter admin details
2.	To access admin, run server and enter `http://127.0.0.1:8000/admin`
