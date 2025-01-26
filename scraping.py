from urllib.parse import urlparse
from googleapiclient.discovery import build
from datetime import datetime
import os.path
import csv





def identify(url):
    parsed = urlparse(url)
    host= parsed.netloc
    print(host)
    if 'youtube.com' in host:
        return 'YouTube'
    
    elif 'instagram.com' in host:
        return 'Instagram'
   
    else:
        return 'Unknown'

def identify_type(url):
    if '/watch' in url or '/p/' in url or '/shorts/' in url :  
        return 'Post'
    else:  
        return 'Homepage'
with open('api.txt','r') as f:
    api=f.read()
API_KEY=api#eneter your api



def handle(url):
    youtube = build('youtube', 'v3', developerKey=API_KEY)  # Initialize API client

    handle=url.split('/')[3]
    response = youtube.search().list(
        part="snippet",           #https://www.youtube.com/@ncrmotorcycles/videos
        q=f"@{handle}",
        type="channel",
        maxResults=1
    ).execute()
    
    if 'items' in response and response['items']:
        channel_id = response['items'][0]['id']['channelId']
        return channel_id
    else:
        return None


    

def ytscraper(url):
    youtube = build('youtube', 'v3', developerKey=API_KEY)  # Initialize API client
    identify(url)
    identify_type(url)
    
    
    if 'watch?v='in url:# Video Page
        try:
            idd = url.split("watch?v=")[-1]# get unique channel id/no
            print(idd)
            response = youtube.videos().list(part="snippet,statistics", id=idd).execute()#get the data from api in list type json format
            video_data = response['items'][0]#get first item
            dic={
                'TITLE': video_data['snippet']['title'],
                'VIEWS': video_data['statistics']['viewCount'],
                'LIKES': video_data['statistics'].get('likeCount', 'N/A'),#used to bypass any error if like dsiabled
                'COMMENTS': video_data['statistics'].get('commentCount', 'N/A'),
                'AT TIME':datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                }
            if os.path.isfile('statistics.csv'):
                with open ('statistics.csv',"a+",newline='') as f:
                    fieldnames = dic.keys()

                    
                    writer = csv.DictWriter(f,fieldnames=fieldnames)

                    writer.writerow(dic)
                    f.seek(0)
                    r= csv.DictReader(f)
                

                    for i in r:
                        print(i)

            else:
                with open ('statistics.csv',"a+",newline='') as f:
                
                    fieldnames = ['TITLE', 'VIEWS', 'LIKES', 'COMMENTS', 'AT TIME']

                    writer = csv.DictWriter(f,fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(dic)
                    f.seek(0)
                    r=csv.DictReader(f)
                    for i in r:
                        print(i)

                

                    

                    

                
                
                
        except  Exception as e:
            print(e)
        
    elif '@' in url or 'featured' in url or 'home'in url  or'shorts'in url:# Channel Page
        try:
            channel_id=handle(url)
            if channel_id is not None:
                response = youtube.channels().list(part="snippet,statistics", id=channel_id).execute()
                channel_data = response['items'][0]
                dic={
                    'channel_name'.upper(): channel_data['snippet']['title'],
                    'subscribers'.upper(): channel_data['statistics']['subscriberCount'],
                    'videos'.upper(): channel_data['statistics']['videoCount'],
                    'AT TIME':datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                    }
                if os.path.isfile('channeldata.csv'):
                    with open ('channeldata.csv',"a+",newline='') as f:
                                  fieldnames = dic.keys()
                                  writer = csv.DictWriter(f,fieldnames=fieldnames)
                                  writer.writerow(dic)
                                  

                    with open('channeldata.csv', "r", newline='') as f:
                        reader = csv.DictReader(f)

                        for row in reader:
                            print(row)
                else:
                    
                    with open ('channeldata.csv',"a+",newline='') as f:
                        fieldnames = ['CHANNEL_NAME', 'SUBSCRIBERS', 'VIDEOS', 'AT TIME']

                        
                        writer = csv.DictWriter(f,fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow(dic)
                        f.seek(0)
                        r=csv.DictReader(f)
                        for i in r:
                            print(i)
        except Exception as e:
            print(e)
    else:
        print('wrong url ')


       
a=ytscraper('https://www.youtube.commhiogDesi')
print(a)
