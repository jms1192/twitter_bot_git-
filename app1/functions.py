from .models import Platform_recent_activity, ShroomAPIQuery

def update_data_and_score(id):
        print(id)
        try:
            Platform_recent_activity.update_data_from_shroom_api(id)
            Platform_recent_activity.trending_score(id)
        except:
            score = Platform_recent_activity.objects.get(id=id)
            score.activity_score = -10000
            score.save()