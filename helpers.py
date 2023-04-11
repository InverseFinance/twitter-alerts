import tweepy
import os
import base64
import requests
import seaborn as sns
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from prettytable import PrettyTable
import matplotlib.style as style
from bs4 import BeautifulSoup

load_dotenv()

def post_tweet(content=None,filename=None):
    try:
        # Set up API keys and access tokens
        consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

        # OAuth process, using the keys and tokens
        auth = tweepy.OAuth1UserHandler(
            consumer_key, 
            consumer_secret, 
            access_token, 
            access_token_secret
        )

        # Creation of the actual interface, using authentication
        api = tweepy.Client(
            consumer_key=consumer_key, 
            consumer_secret=consumer_secret, 
            access_token=access_token, 
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )

        api2 = tweepy.API(auth, wait_on_rate_limit = True)
        
        # Upload image if provided
        if filename is not None:
            # Check if the file is a png file
            if filename.lower().endswith('.png'):
                with open(filename, 'rb') as image_file:
                    media = api2.media_upload(filename, file=image_file)
                    media_id = media.media_id
            else:
                raise ValueError("Image file must be a png file.")
        else:
            media_id = None

        # Create the tweet with or without the image
        if media_id is not None:
            tweet = api.create_tweet(text=content, media_ids=[media_id])
        else:
            tweet = api.create_tweet(text=content)

        return tweet
    except Exception as e:
        print("Error: Unable to post tweet.")
        #print line of error
        import traceback
        traceback.print_exc()
        pass


#get data from https://www.inverse.finance/api/oppyS
def get_apy_data():
    url = "https://www.inverse.finance/api/oppys"
    response = requests.get(url)
    data = response.json()

    df = pd.json_normalize(data["pools"])

    # Convert columns from object to numeric types
    numeric_cols = [
        "tvlUsd",
        "apyBase", 
        "apyReward", 
        "apy", 
        "apyPct1D", 
        "apyPct7D", 
        "apyPct30D", 
        "mu", 
        "sigma", 
        "count", 
        "il7d", 
        "apyBase7d", 
        "apyMean30d", 
        "volumeUsd1d", 
        "volumeUsd7d", 
        "apyBaseInception"
        ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

    # Sort by apy column in descending order
    df_sorted = df.sort_values(by=["apy"], ascending=False)

    return (df_sorted)


def get_top_apy(type):
    df = get_apy_data()
    df = df[[
        "project",
        "symbol",
        "tvlUsd",
        "apy"
        ]]
    
    # list of key owrds
    volatile = ["VELO","INV","INV","WETH","DBR","ETH"]
    stable = ["CUSD","USDC","FRAX","USD+","MAI","3POOL"]
    exclude = ["EULER"]
    # excludes if symbol includes 'EULER'
    df = df[~df.symbol.str.contains('|'.join(exclude))]
    #get top 5 rows
    if type == 'volatile':
        df = df[df.symbol.str.contains('|'.join(volatile))]
    elif type == 'stable':
        df = df[df.symbol.str.contains('|'.join(stable))]

    df = df.head(5)
    return df

def post_stable():

    #post_tweet(content="", filename="test.png")
    table = get_top_apy('stable')

    message = "💪🏼 Top 5 APR Stable : \n" +\
    "🔸" + table.iloc[0]['symbol'] +": " + "{:.2%}".format(table.iloc[0]['apy'] / 100) + "\n" +\
    "🔸" + table.iloc[1]['symbol'] +": " + "{:.2%}".format(table.iloc[1]['apy'] / 100) + "\n" +\
    "🔸" + table.iloc[2]['symbol'] +": " + "{:.2%}".format(table.iloc[2]['apy'] / 100) + "\n" +\
    "🔸" + table.iloc[3]['symbol'] +": " + "{:.2%}".format(table.iloc[3]['apy'] / 100) + "\n" +\
    "🔸" + table.iloc[4]['symbol'] +": " + "{:.2%}".format(table.iloc[4]['apy'] / 100) + "\n" +"\n" +\
    "https://inverse.finance/yield-opportunities"

    print(message)
    #message = message + " " + message.split()[-1]
    post_tweet(content=message)

def post_volatile():
    
        #post_tweet(content="", filename="test.png")
        table = get_top_apy('volatile')
    
        message = "🚀 Top 5 APR Volatile : \n" +\
        "🔹" + table.iloc[0]['symbol'] +": " + "{:.2%}".format(table.iloc[0]['apy'] / 100) + "\n" +\
        "🔹" + table.iloc[1]['symbol'] +": " + "{:.2%}".format(table.iloc[1]['apy'] / 100) + "\n" +\
        "🔹" + table.iloc[2]['symbol'] +": " + "{:.2%}".format(table.iloc[2]['apy'] / 100) + "\n" +\
        "🔹" + table.iloc[3]['symbol'] +": " + "{:.2%}".format(table.iloc[3]['apy'] / 100) + "\n" +\
        "🔸" + table.iloc[4]['symbol'] +": " + "{:.2%}".format(table.iloc[4]['apy'] / 100) + "\n" +"\n" +\
        "https://inverse.finance/yield-opportunities"
    
        print(message)
        #message = message + " " + message.split()[-1]    
        post_tweet(content=message)



def get_liquidity_data():
    url = "https://www.inverse.finance/api/transparency/liquidity?deduce=1"
    response = requests.get(url)
    data = response.json()

    df = pd.json_normalize(data["liquidity"])

    # Convert columns from object to numeric types
    numeric_cols = [
        "chainId",
        "decimals", 
        "tvl",
        "ownedAmount",
        "perc",
        "pairingDepth",
        "dolaBalance",
        "dolaWeight",
        "rewardDay"
        ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    
    # exclude fields whith an lpName that doesnt include dOLA
    df = df[df.lpName.str.contains('DOLA')]
    df = df[df.deduce.isnull()]



    # Sort by apy column in descending order
    df_sorted = df.sort_values(by=["apy"], ascending=False)

    return (df_sorted)


# get the sum from the tvl column from liquidity data
def get_total_liquidity():
    df = get_liquidity_data()
    df = df[[
        "tvl"
        ]]
    total_liquidity = df.sum()
    #format to currency
    total_liquidity = "${:,.2f}".format(total_liquidity[0])
    return total_liquidity

def get_average_dola_weight():
    df = get_liquidity_data()
    average_dola_weight = (df['dolaWeight'].fillna(0) * df['tvl']).sum() / df['tvl'].sum() / 100
    # format to percentage
    average_dola_weight = "{:.2%}".format(average_dola_weight)
    return average_dola_weight



def get_protocol_owned():
    df = get_liquidity_data()
    df = df[[
        "ownedAmount"
        ]]
    protocol_owned = df.sum()
    #format to currency
    protocol_owned = "${:,.2f}".format(protocol_owned[0])
    return protocol_owned

def get_avg_apy():
    df = get_liquidity_data()
    avg_apy = (df['apy'].fillna(0) * df['tvl']).sum() / df['tvl'].sum() / 100
    # format to percentage
    avg_apy = "{:.2%}".format(avg_apy)
    return avg_apy



def post_liquidity():
    message = "DOLA Liquidity Snapshot: \n" +\
    "📈 Total Liquidity: " + get_total_liquidity() + "\n" +\
    " Σ  Average DOLA Weight: " + get_average_dola_weight() + "\n" +\
    "💰 Protocol Owned: " + get_protocol_owned() + "\n" +\
    "➡️ Average APY: " + get_avg_apy() + "\n"
    
    print(message)
    
    post_tweet(content=message)

