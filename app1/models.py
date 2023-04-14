from django.db import models
from shroomdk import ShroomDK
from decimal import Decimal
import tweepy
import requests

#bot account data 
class TwitterBot(models.Model):
    name = models.CharField(max_length=100)
    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send_tweet(self, tweet_text, tweet_img=None):

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth)

        if not tweet_img == None:
            image_path = tweet_img

            # Upload the image to Twitter
            uploaded_image = api.media_upload(image_path)

            # Attach the media ID of the uploaded image to your tweet
            media_ids = [uploaded_image.media_id_string]

            api.update_status(status=tweet_text, media_ids=media_ids)
        else:
            api.update_status(tweet_text)

    def __str__(self):
        return self.name
    
#human created
class ShroomAPIQuery(models.Model):
    name = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=100, default='')
    sub_type = models.CharField(max_length=100, default='')
    query = models.TextField(default='')
    
    def __str__(self):
        return self.name

    def execute(self):
        api_key = 'b0fbd41f-d37b-4909-9074-f5360c4262de'
        # Initialize ShroomDK with your API Key
        sdk = ShroomDK(api_key)

        # Execute the query and return the result set
        return sdk.query(self.query)
    
#human created list of good dasshboards 
class BlockchainDashboards(models.Model):
    name = models.CharField(max_length=100)
    builder = models.CharField(max_length=200)
    url = models.URLField()
    hashtags = models.CharField(max_length=500, help_text="Comma-separated list of hashtags")
    start_string = models.CharField(max_length=200, null=True)
    f_string = models.TextField(blank=True, null=True)
    twitter_bot = models.ForeignKey(TwitterBot, on_delete=models.CASCADE, null=True)
    shroom_api_query = models.ForeignKey(ShroomAPIQuery, on_delete=models.CASCADE, null=True)
    tweet_img = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
    def send_tweet(self):
        if self.twitter_bot:
            pre_data_text = self.start_string
            flipside_api_link = self.url
            dashboard_author_twitter = self.builder
            dashboard_link = self.url

            #extcute flipside query
            data = self.shroom_api_query.execute()

            # Build tweet text using f-string
            tweet_text = pre_data_text + "\n\n"
            for item in data.records:
                if 'value2' in item:
                    item['emoji'] = '📈' if float(item['value2']) >= 0 else '📉'
                    item['percent'] = abs(float(item['value2']))

                #tweet_text += eval(f'f"""{self.f_string}"""')
                tweet_text += self.f_string.format(**item) + '\n'
                
            tweet_text += f"\nLearn more with this dashboard by {dashboard_author_twitter} brought to you by @Pine13579573: \n{dashboard_link}"

            # Send tweet using TwitterBot's send_tweet function
            #if self.tweet_img == '1':
            #    self.twitter_bot.send_tweet(tweet_text)
            #else:
            self.twitter_bot.send_tweet(tweet_text, self.tweet_img)
            print(tweet_text)
        else:
            print("Error: No TwitterBot associated with this dashboard")


#api created
class Platform_recent_activity(models.Model):
    name = models.CharField(max_length=100)
    shroom_api_query = models.ForeignKey('ShroomAPIQuery', on_delete=models.CASCADE, null=True)
    total_transactions_24h = models.PositiveIntegerField(default=0, null=True)
    avg_transaction_fee_24h = models.DecimalField(max_digits=20, decimal_places=10, default=0, null=True)
    active_wallets_24h = models.PositiveIntegerField(default=0, null=True)
    total_transactions_7d = models.PositiveIntegerField(default=0, null=True)
    avg_transaction_fee_7d = models.DecimalField(max_digits=20, decimal_places=10, default=0, null=True)
    active_wallets_7d = models.PositiveIntegerField(default=0, null=True)
    total_transactions_30d = models.PositiveIntegerField(default=0, null=True)
    avg_transaction_fee_30d = models.DecimalField(max_digits=20, decimal_places=10, default=0, null=True)
    active_wallets_30d = models.PositiveIntegerField(default=0, null=True)
    new_users_24h = models.PositiveIntegerField(default=0, null=True) 
    new_users_7d = models.PositiveIntegerField(default=0, null=True) 
    new_users_30d = models.PositiveIntegerField(default=0, null=True) 
    activity_score = models.DecimalField(max_digits=20, decimal_places=10, default=0, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def update_data_from_shroom_api(cls, b_id):
        
        data = cls.objects.get(id=b_id).shroom_api_query.execute()
        print(data)
        blockchain = cls.objects.get(id=b_id)  # Replace "Ethereum" with the name of the blockchain you want to update
        blockchain.avg_transaction_fee_24h = data.rows[0][0] #data["AVG_TX_FEE_24_HOUR"]
        blockchain.active_wallets_24h = data.rows[0][1]
        blockchain.total_transactions_24h = data.rows[0][2]
        blockchain.avg_transaction_fee_7d = data.rows[0][3]
        blockchain.active_wallets_7d = data.rows[0][4]
        blockchain.total_transactions_7d = data.rows[0][5]
        blockchain.avg_transaction_fee_30d = data.rows[0][6]
        blockchain.active_wallets_30d = data.rows[0][7]
        blockchain.total_transactions_30d = data.rows[0][8]
        blockchain.new_users_24h = data.rows[0][9]
        blockchain.new_users_7d = data.rows[0][10]
        blockchain.new_users_30d = data.rows[0][11]
        blockchain.save()


    @classmethod
    def trending_score(cls, b_id):
        print('trending score 1')
        platform_activity = Platform_recent_activity.objects.filter(id=b_id)[0]
        # Calculate activity increase for different time periods
        wallet_growth_24h_7d = (platform_activity.active_wallets_24h - platform_activity.active_wallets_7d) / platform_activity.active_wallets_7d
        wallet_growth_7d_30d = (platform_activity.active_wallets_7d - platform_activity.active_wallets_30d) / platform_activity.active_wallets_30d
        
        transaction_growth_24h_7d = (platform_activity.total_transactions_24h - platform_activity.total_transactions_7d) / platform_activity.total_transactions_7d
        transaction_growth_7d_30d = (platform_activity.total_transactions_7d - platform_activity.total_transactions_30d) / platform_activity.total_transactions_30d

        gas_growth_24h_7d = (platform_activity.avg_transaction_fee_24h - platform_activity.avg_transaction_fee_7d) / platform_activity.avg_transaction_fee_7d
        gas_growth_7d_30d = (platform_activity.avg_transaction_fee_7d - platform_activity.avg_transaction_fee_30d) / platform_activity.avg_transaction_fee_30d
        
        new_users_growth_24h_7d = (platform_activity.new_users_24h - platform_activity.new_users_7d) / platform_activity.new_users_7d
        new_users_growth_7d_30d = (platform_activity.new_users_7d - platform_activity.new_users_30d) / platform_activity.new_users_30d
    
        # Calculate the average growth for wallets, transactions, and gas fees
        avg_wallet_growth = (wallet_growth_24h_7d + wallet_growth_7d_30d) / 2
        avg_transaction_growth = (transaction_growth_24h_7d + transaction_growth_7d_30d) / 2
        avg_gas_growth = (gas_growth_24h_7d + gas_growth_7d_30d) / 2
        avg_new_users_growth = (new_users_growth_24h_7d + new_users_growth_7d_30d) / 2
    
        # Normalize the scores
        normalized_wallet_growth = avg_wallet_growth / (1 + avg_wallet_growth)
        normalized_transaction_growth = avg_transaction_growth / (1 + avg_transaction_growth)
        normalized_gas_growth = avg_gas_growth / (1 + avg_gas_growth)
        normalized_new_users_growth = avg_new_users_growth / (1 + avg_new_users_growth)

        # Calculate the weighted trending score
        wallet_weight = Decimal('0.3')
        gas_weight = Decimal('0.45')
        transaction_weight = Decimal('0.05')
        new_users_weight = Decimal('0.2')

        trending_score = (Decimal(normalized_wallet_growth) * wallet_weight) + (Decimal(normalized_gas_growth) * gas_weight) + (Decimal(normalized_transaction_growth) * transaction_weight) + (Decimal(normalized_new_users_growth) * new_users_weight)
    
        # Update the activity_score field and save the object
        blockchain = cls.objects.get(id=b_id)
        blockchain.activity_score = trending_score
        print(trending_score)
        blockchain.save()