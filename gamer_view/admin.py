from django.contrib import admin
from gamer_view.models import Category, Page, Review

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('gamename',)}
    


admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(Review)

