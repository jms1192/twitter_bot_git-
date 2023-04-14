# tasks.py
import time
from background_task import background
from concurrent.futures import ThreadPoolExecutor
from .models import Platform_recent_activity, ShroomAPIQuery, BlockchainDashboards, TwitterBot
from .functions import update_data_and_score
from django.core.cache import cache

@background(schedule=1)
def my_background_task(param1, param2):
    print("Hello, World!")
    # Update blockchain data
    blockchain_ids = cache.get('blockchain_ids')
    
    if not blockchain_ids:
        blockchain_ids = list(Platform_recent_activity.objects.select_related('shroom_api_query').values_list('id', flat=True))
        cache.set('blockchain_ids', blockchain_ids, 60 * 5)  # Cache for 5 minutes

    with ThreadPoolExecutor() as executor:
        executor.map(update_data_and_score, blockchain_ids)

    time.sleep(60 * 60 * 12)
    
    #my_background_task(param1, param2, schedule=60)

@background(schedule=1)
def launch_twitter_bot(bot_name):
    #gets all the dashboard objest that have the bot with selected name as their bot 
    tweet_list = BlockchainDashboards.objects.filter(twitter_bot=TwitterBot.objects.get(name=bot_name))

    for tweet in tweet_list:
        tweet.send_tweet()
        time.sleep(60 * 60 * 6) 