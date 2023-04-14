from multiprocessing import Pool
from django.shortcuts import render
from .functions import update_data_and_score
from django.http import HttpResponse
from concurrent.futures import ThreadPoolExecutor
from .models import Platform_recent_activity, ShroomAPIQuery, BlockchainDashboards, TwitterBot
from django.core.cache import cache
from .tasks import my_background_task, launch_twitter_bot
import requests
from io import BytesIO
import time

# data update view 
def test2(request, b_id):


    #turn new_blockchain querys into data moddle
    shroomquerys = ShroomAPIQuery.objects.filter(sub_type="chain_use_metrics_1")

    for query in shroomquerys:
        if len(Platform_recent_activity.objects.filter(name=query.name)) == 0:
                
                new_blockchain = Platform_recent_activity(
                    name=query.name,
                    shroom_api_query=query,
                    total_transactions_24h=0,
                    avg_transaction_fee_24h=0.01,
                    active_wallets_24h=0,
                    total_transactions_7d=0,
                    avg_transaction_fee_7d=0.008,
                    active_wallets_7d=0,
                    total_transactions_30d=0,
                    avg_transaction_fee_30d=0.007,
                    active_wallets_30d=0
                )
                new_blockchain.save()

    ## updata blochain data 
    blockchains = Platform_recent_activity.objects.all()
    blockchain_ids = [blockchain.id for blockchain in blockchains]
    print(blockchain_ids)
    for id in blockchain_ids:
        try:
            Platform_recent_activity.update_data_from_shroom_api(id)
            Platform_recent_activity.trending_score(id)
        except:
            score = Platform_recent_activity.objects.get(id=id)
            score.activity_score = -10000
            score.save()

    ##with Pool(processes=4) as pool:  # Replace 5 with the number of processes you want to use
    ##    pool.map(update_data_and_score, blockchain_ids)


    return HttpResponse('hi')


def test1(request, b_id):
    # Turn new_blockchain queries into data model
    shroomquerys = ShroomAPIQuery.objects.filter(sub_type="chain_use_metrics_1").prefetch_related('platform_recent_activity_set')
    
    existing_names = set(Platform_recent_activity.objects.values_list('name', flat=True))

    new_blockchains = [
        Platform_recent_activity(
            name=query.name,
            shroom_api_query=query,
            total_transactions_24h=0,
            avg_transaction_fee_24h=0.01,
            active_wallets_24h=0,
            total_transactions_7d=0,
            avg_transaction_fee_7d=0.008,
            active_wallets_7d=0,
            total_transactions_30d=0,
            avg_transaction_fee_30d=0.007,
            active_wallets_30d=0
        ) for query in shroomquerys if query.name not in existing_names
    ]
    Platform_recent_activity.objects.bulk_create(new_blockchains)

    # Update blockchain data
    blockchain_ids = cache.get('blockchain_ids')
    
    if not blockchain_ids:
        blockchain_ids = list(Platform_recent_activity.objects.select_related('shroom_api_query').values_list('id', flat=True))
        cache.set('blockchain_ids', blockchain_ids, 60 * 5)  # Cache for 5 minutes

    with ThreadPoolExecutor() as executor:
        executor.map(update_data_and_score, blockchain_ids)

    return HttpResponse('hi')


# data look at view 
def data_display(request):

    platforms = Platform_recent_activity.objects.all().order_by('-activity_score')
    data = []
    #my_background_task(param1="example1", param2="example2")
    #try:
    #inc = platforms.avg_transaction_fee_24h
    #except:
    #    inc = 0

    for platform in platforms:
        if not platform.avg_transaction_fee_24h == None and not platform.avg_transaction_fee_7d == None:
            inc = platform.avg_transaction_fee_24h / (platform.avg_transaction_fee_7d/7)
        else:
            inc = 0 

        platform_data = {
            'name': platform.name,
            'liquidity_score': platform.activity_score,
            '7_d_gas_increase': inc
        }
        data.append(platform_data)


    #data = BlockchainDashboards.objects.filter(name='Avalanche BTC.b Bridgooors')[0]
    #data.send_tweet()
    #launch_twitter_bot('Spring Bot')

    tweet_list = BlockchainDashboards.objects.filter(twitter_bot=TwitterBot.objects.get(name='Spring Bot')) #.exclude(name='Avalanche BTC.b Bridgooors')
    tweet_list.reverse()

    while True:
        for tweet in tweet_list:
            tweet.send_tweet() 
            time.sleep(60 * 60 * 6) 
            print(tweet)

    return render(request, 'data_display1.html', {'data': data})


def data_display1(request):
    app_names = [
        'xen crypto',
        'lens protocol',
        'uniswap',
        'the sandbox',
        'lido',
        'sushiswap',
        'aave',
        'opensea',
        'candydex',
        'balancer',
        'stargate finance',
        'superfluid',
        '1inch',
        'curve fi',
        'wormhole',
        'gains network	',
        'stader labs',
        'synapse',
        'dodo',
        'squid',
        'kybernetwork'
    ]  # Replace with your list of app names
    
    query_template = """
    SELECT *
    FROM (
    SELECT 
        sum(CASE when block_timestamp > current_date - 1 then tx_fee * gas_usd end) as avg_tx_fee_1_day,
        count(DISTINCT(CASE when block_timestamp > current_date - 1 then from_address end)) as active_users_1_day,
        count(DISTINCT(CASE when block_timestamp > current_date - 1 then tx_hash end)) as transactions_1_day,
        sum(CASE when block_timestamp > current_date - 7 then tx_fee * gas_usd end) as avg_tx_fee_7_day,
        count(DISTINCT(CASE when block_timestamp > current_date - 7 then from_address end)) as active_users_7_day,
        count(DISTINCT(CASE when block_timestamp > current_date - 7 then tx_hash end)) as transactions_7_day,
        sum(CASE when block_timestamp > current_date - 30 then tx_fee * gas_usd end) as avg_tx_fee_30_day,
        count(DISTINCT(CASE when block_timestamp > current_date - 30 then from_address end)) as active_users_30_day,
        count(DISTINCT(CASE when block_timestamp > current_date - 30 then tx_hash end)) as transactions_30_day 
    FROM polygon.core.fact_transactions
        LEFT OUTER JOIN 
            (
            SELECT
                date_trunc('day', hour) as day,
                median(price) as gas_usd
            FROM ethereum.core.fact_hourly_token_prices
            WHERE symbol LIKE 'MATIC'
            GROUP BY 1 
            ) ON date_trunc('day', block_timestamp) = day
    WHERE to_address IN (
        SELECT
            address
        FROM crosschain.core.address_labels
        WHERE blockchain LIKE 'polygon'
        AND PROJECT_NAME LIKE '{app_name}'
    )
    ) as a LEFT outer JOIN (
    SELECT
        count(DISTINCT CASE when first_day > current_date - 1 then from_address end) as new_users_24h,
        count(DISTINCT CASE when first_day > current_date - 7 then from_address end) as new_users_7d,
        count(DISTINCT CASE when first_day > current_date - 30 then from_address end) as new_users_30d,
        count(DISTINCT from_address) as total_users
    FROM (
    SELECT
        from_address,
        min(block_timestamp) as first_day
    FROM polygon.core.fact_transactions
    WHERE to_address IN (
        SELECT
            address
        FROM crosschain.core.address_labels
        WHERE blockchain LIKE 'polygon'
        AND PROJECT_NAME LIKE '{app_name}'
    )
    GROUP BY 1 
    )
    ) as b
    """

    for app_name in app_names:
        query = query_template.format(app_name=app_name)
        
        shroom_api_query = ShroomAPIQuery(
            name=f'{app_name.replace(" ", "")}_polygon_use_metrics_1',
            type=f'{app_name.replace(" ", "")}_polygon',
            sub_type='chain_use_metrics_1',
            query=query
        )
        shroom_api_query.save()

    return HttpResponse("ShroomAPIQuery objects created successfully.", status=201)