import os
import re
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

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
        index_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'home':
                    index_mapping_exists = True
        
        self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The home URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('gamer_view:home'), '/gamer_view/', f"{FAILURE_HEADER}The index URL lookup failed. Check gamer_view's urls.py module. You're missing something in there.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('gamer_view:home'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the home page failed. Check your URLs and view.{FAILURE_FOOTER}")
#        self.assertContains(response, "Rango says hey there partner!", msg_prefix=f"{FAILURE_HEADER}The index view does not return the expected response. Be careful you haven't missed any punctuation, and that your cAsEs are correct.{FAILURE_FOOTER}")
    
    def test_for_about_hyperlink(self):
        response = self.client.get(reverse('gamer_view:home'))
        
        about_button_check = '<a href="/gamer_view/about/" style="color:white; text-decoration:none">About Us</a>' in response.content.decode()
        trending_button_check = '<a href="/gamer_view/trending/" style="color:white; text-decoration:none"> Trending </a>' in response.content.decode()
        categories_button_check = '<a href="/gamer_view/categories/" style="color:white; text-decoration:none"> Categories </a>' in response.content.decode()
        sign_in_button_check = '<a href="/gamer_view/login/" style="color:white; text-decoration:none">Sign In</a>' in response.content.decode()
        register_button_check = '<a href="/gamer_view/register/" style="color:white; text-decoration:none">Register</a>' in response.content.decode()
        
        self.assertTrue(about_button_check and trending_button_check and categories_button_check and sign_in_button_check and register_button_check, f"{FAILURE_HEADER}We couldn't find the hyperlink to the /gamer_view/about/ URL in your index page. Check that it appears EXACTLY as in the book.{FAILURE_FOOTER}")

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
    
    def test_for_index_hyperlink(self):
        response = self.client.get(reverse('gamer_view:about'))
        
        home_hyperlink_check = '<a href="/gamer_view/">' in response.content.decode()
        
        self.assertTrue(home_hyperlink_check, f"{FAILURE_HEADER}We could not find a hyperlink back to the index page in your about view. Check your about.html template, and try again.{FAILURE_FOOTER}")
        
class TemplateStructureTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.gamer_view_templates_dir = os.path.join(self.templates_dir, 'gamer_view')
        
    def test_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")

    def test_rango_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.gamer_view_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The Rango templates directory does not exist.{FAILURE_FOOTER}")

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
        index_path = os.path.join(self.gamer_view_templates_dir, 'home.html')
        about_path = os.path.join(self.gamer_view_templates_dir, 'about.html')
        
        self.assertTrue(os.path.isfile(index_path), f"{FAILURE_HEADER}Your index.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(about_path), f"{FAILURE_HEADER}Your about.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        