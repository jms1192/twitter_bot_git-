from django.contrib import admin
from .models import Platform_recent_activity, ShroomAPIQuery, TwitterBot, BlockchainDashboards 

admin.site.register(ShroomAPIQuery)
admin.site.register(Platform_recent_activity)
admin.site.register(TwitterBot)
admin.site.register(BlockchainDashboards)