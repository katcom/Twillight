from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FacePamphletUser)
admin.site.register(StatusEntry)
admin.site.register(FriendRequestEntry)
admin.site.register(UnilateralFriendship)

admin.site.register(ValidUnilateralFriendship)
admin.site.register(StatusEntryImage)