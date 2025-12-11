from django.contrib import admin
from.models import postModel,comment
 
# Register your models here.

class postModelAdmin(admin.ModelAdmin):
    list_display = ('title',  'date_created')
    
admin.site.register(postModel, postModelAdmin)
   
admin.site.register(comment)