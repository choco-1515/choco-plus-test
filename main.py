from flask import Flask, render_template, request, jsonify
import requests
import random
import os

app = Flask(__name__)

YOUTUBE_API_KEYS = [
    "AIzaSyBQ-40ld7erVfx7s6iKBYl-GjDqJVYBwrc",
    "AIzaSyCoz9NrmBu5mFRm_-qD4XoTFaqu7AGvGeU",
    "AIzaSyDdgsY60mxo98j99leqp1pb5aFYvSSvrSc",
    "AIzaSyC__tVvRkEHBtGIjfxhD_FbG3fAcjiaXlc",
    "AIzaSyAZwLva1HxzDbKFJuE9RVcxS5B4q_ol8yE",
    "AIzaSyCqvGnAlX4_Ss7PInUEg3RWucbdjmnWP6U",
    "AIzaSyBw0JamBkR5eOJLYnmBBxEoptlVm22Q0oA",
    "AIzaSyCz7f0X_giaGyC9u1EfGZPBuAC9nXiL5Mo",
    "AIzaSyBmzCw7-sX1vm-uL_u2Qy3LuVZuxye4Wys",
    "AIzaSyBWScla0K91jUL6qQErctN9N2b3j9ds7HI",
    "AIzaSyA17CdOQtQRC3DQe7rgIzFwTUjwAy_3CAc",
    "AIzaSyDdk_yY0tN4gKsm4uyMYrIlv1RwXIYXrnw",
    "AIzaSyDeU5zpcth2OgXDfToyc7-QnSJsDc41UGk",
    "AIzaSyClu2V_22XpCG2GTe1euD35_Mh5bn4eTjA"
]

INVIDIOUS_INSTANCES = [
    "https://yt.omada.cafe",
    "https://invidious.lunivers.trade",
    "https://invidious.ritoge.com",
    "https://super8.absturztau.be",
    "https://invidious.f5.si",
    "https://lekker.gay",
    "https://iv.melmac.space",
    "https://invidious.vern.cc",
    "https://yt.vern.cc",
    "https://inv.kamuridesu.com",
    "https://inv.thepixora.com",
    "https://invidious.tiekoetter.com",
    "https://youtube.mosesmang.com",
    "https://invidious.ducks.party",
    "https://inv.zoomerville.com",
    "https://invidious.materialio.us",
    "https://inv.nadeko.net",
    "https://yt.thechangebook.org",
    "https://y.com.sb",
    "https://invidious.reallyaweso.me",
    "https://invidious.dhusch.de"
]

def search_youtube(query):
    for key in YOUTUBE_API_KEYS:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=20&key={key}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get('items', []):
                    results.append({
                        'id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'thumbnail': item['snippet']['thumbnails']['high']['url'],
                        'channel': item['snippet']['channelTitle']
                    })
                return results
        except:
            continue
    return None

def search_invidious(query):
    instances = INVIDIOUS_INSTANCES.copy()
    random.shuffle(instances)
    for instance in instances:
        url = f"{instance}/api/v1/search?q={query}&type=video"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data:
                    results.append({
                        'id': item['videoId'],
                        'title': item['title'],
                        'thumbnail': item['videoThumbnails'][0]['url'] if item.get('videoThumbnails') and len(item['videoThumbnails']) > 0 else '',
                        'channel': item['author']
                    })
                return results
        except:
            continue
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'inv_first') # inv_first or yt_first
    if not query:
        return render_template('search.html', results=[], query="")
    
    results = None
    if mode == 'inv_first':
        results = search_invidious(query)
        if not results:
            results = search_youtube(query)
    else:
        results = search_youtube(query)
        if not results:
            results = search_invidious(query)
        
    return render_template('search.html', results=results if results else [], query=query, mode=mode)

@app.route('/watch/<video_id>')
def watch(video_id):
    return render_template('watch.html', video_id=video_id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
