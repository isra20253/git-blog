from django.contrib import admin
from .models import profileModel

print("--------------------------------------------------")
print("JE CHARGE LE FICHIER ADMIN DE USERS !!!")
print("--------------------------------------------------")

admin.site.register(profileModel)