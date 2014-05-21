from django.contrib import admin
import reversion

from .models import *

# class YourModelAdmin(reversion.VersionAdmin):
#     pass

admin.site.register(Facility)
admin.site.register(FacilityType)
admin.site.register(Fee)
admin.site.register(FacilityFee)
admin.site.register(Language)
admin.site.register(Condition)
admin.site.register(Amenity)
admin.site.register(RoomType)
