## importing required modules
from googleapiclient.discovery import build
from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
import requests

#@ initializing the flask app
application = Flask(__name__) 
app=application

## routing to index.html by default 
@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html") ## rendering html

## routing to result page to show the data
@app.route("/result" , methods = ['POST' , 'GET'])
@cross_origin()
def index():
        try:
            api_key = "AIzaSyBjCXRf9LqbY9R1yfK4RqBLfI-uIwQMdlM"
            channel_id = "UCphU2bAGmw304CFAzy0Enuw"
            uploads_id = "UUphU2bAGmw304CFAzy0Enuw"

            ## initiating youtube funtion  
            youtube = build( "youtube", 'v3', developerKey=f'{api_key}')

            ## getting video details of first 5 videos
            videos_data = youtube.playlistItems().list(playlistId='UUphU2bAGmw304CFAzy0Enuw', part = 'snippet,contentDetails',maxResults=5).execute()

            ## storing 'items' section of the data into a varaible
            items = videos_data['items']

            ## creating empty lists to store all data
            video_ids = []
            view_count = []
            titles = []
            publish_at = []
            urls = []
            thumbnail_urls = []
            details = []

            ## creating csv file
            fw = open("data.csv", "w")
            headers = "Title, Views, Uploaded, videoLink, ThumbnailLink \n"
            fw.write(headers)

            ## using for loop to get values we need 
            for i in items:
                ## getting video ID and adinf youtube url
                url = "https://www.youtube.com/watch?v=" + i['contentDetails']['videoId']
                urls.append(url)

            for j in items:
                ## gettign thumbnail url of first 5 videos
                thumbnail_url = j['snippet']['thumbnails']['high']['url']
                thumbnail_urls.append(thumbnail_url)

            for k in items:
                ## getting title of videos
                title = k['snippet']['title']
                titles.append(title)

            for h in items:
                ## getting time of posting of videos 
                publish = h['snippet']['publishedAt']
                publish_at.append(publish)

            for l in items:
                ## getting only video ids  
                v_id = i['contentDetails']['videoId']
                video_ids.append(v_id)

            ## requesting details of each video from api using video id
            request = youtube.videos().list(part="snippet,contentDetails,statistics",id = video_ids)
            response = request.execute()

            for video in response['items']:
                ## getting view count of each video
                stats = video['statistics']['viewCount']
                view_count.append(stats)
            
            ## using for loop to print out the results one by one
            for a,b,c,d,e in zip(titles,view_count,publish_at,urls,thumbnail_urls):
                mydict = {"Title": a, "Views": b, "Uploaded": c, "VideoLink": d,"ThumbnailLink": e}   
                details.append(mydict)

            ## returning the data to html    
            return render_template('result.html', reviews=details)

        except Exception as e:
            return 'something is wrong'

if __name__=="__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
        #app.run(debug=True)
