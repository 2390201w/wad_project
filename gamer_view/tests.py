import os
import importlib
import warnings
from django.urls import reverse, resolve
from django.test import TestCase
from django.conf import settings
from gamer_view.models import Category, Page
from django.contrib.auth.models import User
from django.forms import fields as django_fields
import re
from population_script import populate
from datetime import datetime, timedelta

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class StructureTest(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.gamer_view_app_dir = os.path.join(self.project_base_dir,'gamer_view')
        
    def test_project_created(self):
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'wad_project'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'wad_project', 'urls.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your wad_project configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")
        
    def test_gamer_view_app_created(self):
        directory_exists = os.path.isdir(self.gamer_view_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.gamer_view_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.gamer_view_app_dir, 'views.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The gamer_view app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The gamer_view directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The gamer_view directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_gamer_view_has_urls_module(self):
        module_exists = os.path.isfile(os.path.join(self.gamer_view_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The gamer_view app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")

    def test_is_gamer_view_app_configured(self):
        is_app_configured = 'gamer_view' in settings.INSTALLED_APPS
        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The gamer_view app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")

class HomePageTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('gamer_view.views')
        self.views_module_listing = dir(self.views_module)
        self.response = self.client.get(reverse('gamer_view:home'))
        self.project_urls_module = importlib.import_module('wad_project.urls')
        
    def test_view_exists(self):
        name_exists = 'home' in self.views_module_listing
        is_callable = callable(self.views_module.home)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The home() view for gamer_view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the home() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")
    
    def test_mappings_exists(self):
        home_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'home':
                    home_mapping_exists = True
        
        self.assertTrue(home_mapping_exists, f"{FAILURE_HEADER}The home URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('gamer_view:home'), '/gamer_view/', f"{FAILURE_HEADER}The home URL lookup failed. Check gamer_view's urls.py module. You're missing something in there.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('gamer_view:home'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the home page failed. Check your URLs and view.{FAILURE_FOOTER}")

    def test_home_uses_template(self):
        self.assertTemplateUsed(self.response, 'gamer_view/home.html', f"{FAILURE_HEADER}Your home() view does not use the expected home.html template.{FAILURE_FOOTER}")
        
    def test_home_starts_with_doctype(self):
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your home.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
        

class AboutPageTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('gamer_view.views')
        self.views_module_listing = dir(self.views_module)
        
    def test_view_exists(self):
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}We couldn't find the view for your about view! It should be called about().{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check you have defined your about() view correctly. We can't execute it.{FAILURE_FOOTER}")

    def test_mapping_exists(self):
        self.assertEquals(reverse('gamer_view:about'), '/gamer_view/about/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('gamer_view:about'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly. Is everything correct in your URL mappings and the view?{FAILURE_FOOTER}")
        self.assertContains(response, "About Us", msg_prefix=f"{FAILURE_HEADER}The about view did not respond with the expected message. Check that the message matches EXACTLY with what is requested of you in the book.{FAILURE_FOOTER}")
    
    def test_for_home_hyperlink(self):
        response = self.client.get(reverse('gamer_view:about'))
        
        home_hyperlink_check = '<a href="/gamer_view/">' in response.content.decode()
        
        self.assertTrue(home_hyperlink_check, f"{FAILURE_HEADER}We could not find a hyperlink back to the home page in your about view. Check your about.html template, and try again.{FAILURE_FOOTER}")
        
class TemplateStructureTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.gamer_view_templates_dir = os.path.join(self.templates_dir, 'gamer_view')
        
    def test_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")

    def test_gamer_view_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.gamer_view_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The gamer_view templates directory does not exist.{FAILURE_FOOTER}")

    def test_template_dir_setting(self):
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined!{FAILURE_FOOTER}")
        
        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")
    
    def test_template_lookup_path(self):
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False
        
        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)
            
            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True
        
        self.assertTrue(found_path, f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")
    
    def test_templates_exist(self):
        paths = ['home.html',
                 'about.html',
                 'add_category.html',
                 'add_page.html',
                 'add_review.html',
                 'base.html',
                 'categories.html',
                 'category.html',
                 'login.html',
                 'my_account.html',
                 'page.html',
                 'register.html',
                 'trending.html',]
        for p in paths:
            self.assertTrue(os.path.isfile(os.path.join(self.gamer_view_templates_dir,p)), f"{FAILURE_HEADER}Your templates does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        

class StaticMediaTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')
        
    def test_css_exist(self):
        paths = ['home',
                 'about',
                 'base',
                 'categories',
                 'category',
                 'login',
                 'my_account',
                 'page',
                 'register',
                 'trending',
                 'star',]
        for p in paths:
            self.assertTrue(os.path.isfile(os.path.join(self.static_dir,'css',p+'.css')), f"{FAILURE_HEADER}Your CSS does not exist, or is in the wrong location.{FAILURE_FOOTER}")

    def test_js_exist(self):
        paths = ['star',
                 ]
        for p in paths:
            self.assertTrue(os.path.isfile(os.path.join(self.static_dir,'js',p+'.js')),f"{FAILURE_HEADER}Your JavaScript does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        

    def test_static_and_media_configuration(self):
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable STATIC_DIR defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path, f"{FAILURE_HEADER}The value of STATIC_DIR does not equal the expected path. It should point to your project root, with 'static' appended to the end of that.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The required setting STATICFILES_DIRS is not present in your project's settings.py module. Check your settings carefully. So many students have mistyped this one.{FAILURE_FOOTER}")
        self.assertEqual([static_path], settings.STATICFILES_DIRS, f"{FAILURE_HEADER}Your STATICFILES_DIRS setting does not match what is expected. Check your implementation against the instructions provided.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The STATIC_URL variable has not been defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual('/static/', settings.STATIC_URL, f"{FAILURE_HEADER}STATIC_URL does not meet the expected value of /static/. Make sure you have a slash at the end!{FAILURE_FOOTER}")
        
        media_dir_exists = 'MEDIA_DIR' in dir(settings)
        self.assertTrue(media_dir_exists, f"{FAILURE_HEADER}The MEDIA_DIR variable in settings.py has not been defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.media_dir)
        media_path = os.path.normpath(settings.MEDIA_DIR)
        self.assertEqual(expected_path, media_path, f"{FAILURE_HEADER}The MEDIA_DIR setting does not point to the correct path. Remember, it should have an absolute reference to tango_with_django_project/media/.{FAILURE_FOOTER}")
        
        media_root_exists = 'MEDIA_ROOT' in dir(settings)
        self.assertTrue(media_root_exists, f"{FAILURE_HEADER}The MEDIA_ROOT setting has not been defined.{FAILURE_FOOTER}")
        
        media_root_path = os.path.normpath(settings.MEDIA_ROOT)
        self.assertEqual(media_path, media_root_path, f"{FAILURE_HEADER}The value of MEDIA_ROOT does not equal the value of MEDIA_DIR.{FAILURE_FOOTER}")
        
        media_url_exists = 'MEDIA_URL' in dir(settings)
        self.assertTrue(media_url_exists, f"{FAILURE_HEADER}The setting MEDIA_URL has not been defined in settings.py.{FAILURE_FOOTER}")
        
        media_url_value = settings.MEDIA_URL
        self.assertEqual('/media/', media_url_value, f"{FAILURE_HEADER}Your value of the MEDIA_URL setting does not equal /media/. Check your settings!{FAILURE_FOOTER}")
    
    def test_context_processor_addition(self):
        context_processors_list = settings.TEMPLATES[0]['OPTIONS']['context_processors']
        self.assertTrue('django.template.context_processors.media' in context_processors_list, f"{FAILURE_HEADER}The 'django.template.context_processors.media' context processor was not included. Check your settings.py module.{FAILURE_FOOTER}")

class DatabaseConfigurationTests(TestCase):
    def setUp(self):
        pass
    
    def does_gitignore_include_database(self, path):
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
        
    def test_databases_variable_exists(self):
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. Check the start of Chapter 5.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable. Check the start of Chapter 5.{FAILURE_FOOTER}")

    def test_gitignore_for_database(self):
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        
        if git_base_dir.startswith('fatal'):
            warnings.warn("You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')
            
            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn("You don't appear to have a .gitignore file in place in your repository. We ask that you consider this! Read the Don't git push your Database paragraph in Chapter 5.")

class ModelTests(TestCase):
    def setUp(self):
        category_moba = Category.objects.get_or_create(category='MOBA')
        Category.objects.get_or_create(category='FPS')
        
        Page.objects.get_or_create(cat=category_moba[0],
                                   gamename='League of Legends',
                                   description='Riot Game',
                                   views=216)
        
    def test_page_model(self):
        category_moba = Category.objects.get(category='MOBA')
        page = Page.objects.get(gamename='League of Legends')
        self.assertEqual(page.cat, category_moba, f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.views, 216, f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.description, 'Riot Game', f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")
        self.assertEqual(page.gamename, 'League of Legends', f"{FAILURE_HEADER}Tests on the Page model failed. Check you have all required attributes (including those specified in the exercises!), and try again.{FAILURE_FOOTER}")

    def test_str_method(self):
        category_moba = Category.objects.get(category='MOBA')
        page = Page.objects.get(gamename='League of Legends')
        
        self.assertEqual(str(category_moba), 'MOBA', f"{FAILURE_HEADER}The __str__() method in the Category class has not been implemented according to the specification given in the book.{FAILURE_FOOTER}")
        self.assertEqual(str(page), 'League of Legends', f"{FAILURE_HEADER}The __str__() method in the Page class has not been implemented according to the specification given in the book.{FAILURE_FOOTER}")

class AdminInterfaceTests(TestCase):
    def setUp(self):
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')
        
        category_test = Category.objects.get_or_create(category='TestCategory')[0]
        Page.objects.get_or_create(gamename='TestGame', description='this is Description', cat=category_test)
    
    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The admin interface is not accessible. Check that you didn't delete the 'admin/' URL pattern in your project's urls.py module.{FAILURE_FOOTER}")
    
    def test_models_present(self):
        response = self.client.get('/admin/')
        response_body = response.content.decode()
        
        # Is the gamer_view app present in the admin interface's homepage?
        self.assertTrue('Models in the Gamer_View application' in response_body, f"{FAILURE_HEADER}The gamer_view app wasn't listed on the admin interface's homepage. You haven't added the models to the admin interface.{FAILURE_FOOTER}")
        
        # Check each model is present.
        self.assertTrue('Categories' in response_body, f"{FAILURE_HEADER}The Category model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (Categories)?{FAILURE_FOOTER}")
        self.assertTrue('Pages' in response_body, f"{FAILURE_HEADER}The Page model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (Pages)?{FAILURE_FOOTER}")
        self.assertTrue('Reviews' in response_body, f"{FAILURE_HEADER}The Reviews model was not found in the admin interface. If you did add the model to admin.py, did you add the correct plural spelling (Pages)?{FAILURE_FOOTER}")
    
class FormClassTests(TestCase):
    def test_module_exists(self):
        project_path = os.getcwd()
        gamer_view_app_path = os.path.join(project_path, 'gamer_view')
        forms_module_path = os.path.join(gamer_view_app_path, 'forms.py')

        self.assertTrue(os.path.exists(forms_module_path), f"{FAILURE_HEADER}We couldn't find gamer_view's new forms.py module. This is required to be created at the top of Section 7.2. This module should be storing your two form classes.{FAILURE_FOOTER}")

    def test_category_form_class(self):
        # Check that we can import CategoryForm.
        import gamer_view.forms
        self.assertTrue('CategoryForm' in dir(gamer_view.forms), f"{FAILURE_HEADER}The class CategoryForm could not be found in gamer_view's forms.py module. Check you have created this class in the correct location, and try again.{FAILURE_FOOTER}")

        from gamer_view.forms import CategoryForm
        category_form = CategoryForm()

        # Do you correctly link Category to CategoryForm?
        self.assertEqual(type(category_form.__dict__['instance']), Category, f"{FAILURE_HEADER}The CategoryForm does not link to the Category model. Have a look in the CategoryForm's nested Meta class for the model attribute.{FAILURE_FOOTER}")

        # Now check that all the required fields are present, and of the correct form field type.
        fields = category_form.fields

        expected_fields = {
            'category': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in your CategoryForm implementation. Check you have all required fields, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in CategoryForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")

class PageFormClassTests(TestCase):
    def test_page_form_class(self):
        # Check that we can import PageForm.
        import gamer_view.forms
        self.assertTrue('PageForm' in dir(gamer_view.forms), f"{FAILURE_HEADER}The class PageForm could not be found in gamer_view's forms.py module. Check you have created this class in the correct location, and try again.{FAILURE_FOOTER}")

        from gamer_view.forms import PageForm
        page_form = PageForm()

        # Do you correctly link Page to PageForm?
        self.assertEqual(type(page_form.__dict__['instance']), Page, f"{FAILURE_HEADER}The PageForm does not link to the Page model. Have a look in the PageForm's nested Meta class for the model attribute.{FAILURE_FOOTER}")

        # Now check that all the required fields are present, and of the correct form field type.
        fields = page_form.fields

        expected_fields = {
            'gamename': django_fields.CharField,
            'image': django_fields.ImageField,
            'description': django_fields.CharField,
            'views':django_fields.IntegerField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in your PageForm implementation. Check you have all required fields, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in PageForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")

class TemplateTests(TestCase):
    def get_template(self, path_to_template):
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str
    
    def test_base_template_exists(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'gamer_view', 'base.html')
        self.assertTrue(os.path.exists(template_base_path), f"{FAILURE_HEADER}We couldn't find the new base.html template that's required in the templates/gamer_view directory. Did you create the template in the right place?{FAILURE_FOOTER}")

class ConfigurationTests(TestCase):

    def test_middleware_present(self):

        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)
    
    def test_session_app_present(self):

        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)



    
    
    
    
    
    
    
    
    
        
        
        
        
        
        