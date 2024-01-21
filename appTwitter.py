import datetime
import tweepy
import requests
import pytz
from bs4 import BeautifulSoup

'''
    get_image_url_from_wikimedia_commons
'''  
def get_image_url_from_wikimedia_commons(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    meta_tags = soup.find_all('meta', {'property': 'og:image'})
    if meta_tags:
        meta_tag = meta_tags[-1]
        if 'content' in meta_tag.attrs:
            return meta_tag.attrs['content']
    return None

 
'''
    tweet_upload_v2
'''         
def tweet_upload_v2(title, url):
    # Twitter API v2 User Authentication Credentials
    consumer_key = 'XXXXX'
    consumer_secret = 'XXXXX'
    access_token = 'XXXXX'
    access_token_secret = 'XXXXX'

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    try:
        # Create a tweet
        tweet = f"{title} {url}"
        #print(tweet)
        response = client.create_tweet(text=tweet)
        if response:
            print("Tweeted:", tweet)
        else:
            print("Failed to tweet.")
    except Exception as e: 
        print(e)


'''
    get_wiki_content
''' 
def get_wiki_content(page_title):
    wiki_api_url = 'https://commons.wikimedia.org/w/api.php'
    wiki_params = {
        'action': 'query',
        'titles': page_title,
        'prop': 'revisions',
        'rvprop': 'content',
        'format': 'json'
    }

    try:
        response = requests.get(wiki_api_url, params=wiki_params)
        data = response.json()
        #print("Response data:", data) 
        pages = data.get('query', {}).get('pages', {})
        page_id = next(iter(pages), None)
        if page_id and 'revisions' in pages[page_id]:
            content = pages[page_id]['revisions'][0]['*']
            return content
        else:
            print(f"No revisions found for {page_title}")
            return ''
    except Exception as e:
        print("Error in fetching wiki content:", e)
        return ''


'''
    is_recent_upload
''' 
def is_recent_upload(timestamp):
    current_time = datetime.datetime.now(pytz.utc)
    upload_time = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
    time_difference = current_time - upload_time
    time_difference = time_difference.total_seconds()
    print(time_difference)
    isRecent = time_difference <= 60
    print(isRecent)
    return isRecent

'''
    get_recent_uploads
'''
def get_recent_uploads(user_name):
    api_url = 'https://commons.wikimedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'allimages',
        'aiprop': 'timestamp|url',
        'aisort': 'timestamp',
        'aiuser': user_name,
        'format': 'json',
        'ailimit': 10,  
        'aidir': 'descending'
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    recent_uploads = []
    if 'query' in data and 'allimages' in data['query']:
        for upload in data['query']['allimages']:
            timestamp = upload['timestamp']
            if is_recent_upload(timestamp):
                page_title = upload['title']
                wiki_content = get_wiki_content(page_title)
                if '{{Creator:Benoît Prieur}}' in wiki_content:
                    title = upload['name'].split('.')[0].replace('_', ' ')
                    url = f"https://commons.wikimedia.org/wiki/{page_title.replace(' ', '_')}"
                    recent_uploads.append((title, url))
                else:
                    print(f"Image {page_title} skipped: Creator tag not found.")
            else:
                break 

    return recent_uploads


'''
    main
'''
def main():
    recent_uploads = get_recent_uploads('Benoît Prieur')
    
    if recent_uploads:
        for title, url in recent_uploads:
            tweet_upload_v2(title, url)
    else:
        print("main: no recent uploads to tweet.")

if __name__ == '__main__':
    main()