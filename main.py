from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import requests
import random
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'choco-tube-dev-key')
CORS(app)

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
    "https://invidious.darkness.services",
    "https://invidious.lol",
    "https://invidious.st",
    "https://inv.in.projectsegfau.lt",
    "https://invidious.twigotech.eu",
    "https://invidious.mint.lgbt",
    "https://invidious.einfachzocken.eu",
    "https://invidious.sethforprivacy.com",
    "https://invidious.reallyaweso.me",
    "https://invidious.asir.dev",
    "https://inv.nadeko.net",
    "https://yewtu.be",
    "https://invidious.nerdvpn.de",
    "https://inv.riverside.rocks",
]

INVIDIOUS_STREAM_INSTANCES = [
    "https://app.materialio.us",
    "https://inv.kamuridesu.com",
    "https://inv.nadeko.net",
    "https://inv.vern.cc",
    "https://inv1.nadeko.net",
    "https://inv2.nadeko.net",
    "https://inv3.nadeko.net",
    "https://inv4.nadeko.net",
    "https://inv5.nadeko.net",
    "https://inv6.nadeko.net",
    "https://inv7.nadeko.net",
    "https://inv8.nadeko.net",
    "https://inv9.nadeko.net",
    "https://invidious.f5.si",
    "https://invidious.lunivers.trade",
    "https://invidious.nerdvpn.de",
    "https://invidious.nietzospannend.nl",
    "https://invidious.projektegfau.lt",
    "https://invidious.protokolla.fi",
    "https://invidious.tiekoetter.com",
    "https://lekker.gay",
    "https://nyc1.iv.ggtyler.dev",
    "https://rust.oskamp.nl",
    "https://y.com.sb",
    "https://yewtu.be",
    "https://yt.thechangebook.org",
    "https://yt.vern.cc",
    "https://invidious.darkness.services",
    "https://invidious.privacyredirect.com",
    "https://invidious.fdn.fr",
    "https://iv.ggtyler.dev",
    "https://invidious.lunar.icu",
    "https://yt.artemislena.eu",
    "https://invidious.flokinet.to",
    "https://invidious.sethforprivacy.com",
]

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_proxy_thumbnail(video_id, proxy_type="wsrv.nl"):
    if proxy_type == "i.ytimg.com":
        return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    elif proxy_type == "self-hosted":
        # Self-hosted proxy thumbnail method
        return f"/api/thumbnail/{video_id}"
    elif proxy_type == "wsrv.nl":
        # wsrv.nl proxy thumbnail method
        return f"https://wsrv.nl/?url=https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

def search_invidious(query, page=1, proxy_type="img.youtube.com", search_type="video"):
    instances = INVIDIOUS_INSTANCES.copy()
    random.shuffle(instances)
    for instance in instances:
        url = f"{instance}/api/v1/search?q={query}&type={search_type}&page={page}"
        try:
            response = requests.get(url, timeout=5, headers=BROWSER_HEADERS, allow_redirects=True)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data:
                    try:
                        if search_type == "channel":
                            results.append({
                                'id': item['authorId'],
                                'title': item['author'],
                                'thumbnail': item.get('authorThumbnails', [{}])[0].get('url', ''),
                                'type': 'channel',
                                'description': item.get('description', '')
                            })
                        else:
                            v_id = item.get('videoId', '')
                            if not v_id:
                                continue
                            view_count = item.get('viewCount', 0)
                            results.append({
                                'id': v_id,
                                'title': item.get('title', 'Untitled'),
                                'thumbnail': get_proxy_thumbnail(v_id, proxy_type),
                                'channel': item.get('author', 'Unknown Channel'),
                                'channel_id': item.get('authorId', ''),
                                'type': 'video',
                                'views': format_view_count(view_count) if view_count else 'N/A',
                                'published_at': item.get('publishedText', '')
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing search item: {e}")
                        continue
                return results, page + 1
        except Exception as e:
            logger.debug(f"Invidious error {instance}: {e}")
            continue
    logger.warning(f"All Invidious instances failed for query: {query}")
    return None, None

def parse_iso8601_duration(duration_str):
    """Parse ISO 8601 duration (e.g., PT1H23M45S) to readable format (1:23:45 or 23:45)"""
    if not duration_str:
        return ""
    try:
        import re
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0

            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
        return ""
    except:
        return ""

def search_youtube(query, page_token=None, proxy_type="img.youtube.com", search_type="video"):
    for key in YOUTUBE_API_KEYS:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type={search_type}&maxResults=20&key={key}"
        if page_token:
            url += f"&pageToken={page_token}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                video_ids = []
                for item in data.get('items', []):
                    if search_type == "channel":
                        results.append({
                            'id': item['id']['channelId'],
                            'title': item['snippet']['title'],
                            'thumbnail': item['snippet']['thumbnails']['default']['url'],
                            'type': 'channel',
                            'description': item['snippet']['description']
                        })
                    else:
                        v_id = item['id']['videoId']
                        video_ids.append(v_id)
                        results.append({
                            'id': v_id,
                            'title': item['snippet']['title'],
                            'thumbnail': get_proxy_thumbnail(v_id, proxy_type),
                            'channel': item['snippet']['channelTitle'],
                            'channel_id': item['snippet']['channelId'],
                            'type': 'video',
                            'views': 'N/A',
                            'published_at': item['snippet']['publishedAt'],
                            'duration': ''
                        })

                # Fetch video statistics and duration to get view count and length
                if video_ids and search_type == "video":
                    try:
                        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails&id={','.join(video_ids)}&key={key}"
                        stats_response = requests.get(stats_url, timeout=5)
                        if stats_response.status_code == 200:
                            stats_data = stats_response.json()
                            stats_map = {item['id']: item for item in stats_data.get('items', [])}
                            for result in results:
                                if result['type'] == 'video' and result['id'] in stats_map:
                                    item = stats_map[result['id']]
                                    view_count = int(item.get('statistics', {}).get('viewCount', 0))
                                    if view_count >= 1000000:
                                        result['views'] = f"{view_count/1000000:.1f}M"
                                    elif view_count >= 1000:
                                        result['views'] = f"{view_count/1000:.1f}K"
                                    else:
                                        result['views'] = str(view_count)

                                    duration = item.get('contentDetails', {}).get('duration', '')
                                    result['duration'] = parse_iso8601_duration(duration)
                    except Exception as e:
                        logger.debug(f"Error fetching video stats: {e}")

                return results, data.get('nextPageToken')
        except Exception as e:
            logger.debug(f"YouTube API error with key {key[:10]}...: {e}")
            continue
    logger.warning(f"All YouTube API keys failed for query: {query}")
    return None, None


@app.route('/')
def index():
    # Get preferences from cookies or set defaults
    proxy_type = request.cookies.get('proxy_type', 'wsrv.nl')
    search_mode = request.cookies.get('search_mode', 'inv_first')

    response = make_response(render_template('index.html', proxy_type=proxy_type, search_mode=search_mode))

    # Set default cookies
    response.set_cookie('proxy_type', proxy_type, max_age=2592000)  # 30 days
    response.set_cookie('search_mode', search_mode, max_age=2592000)  # 30 days

    return response

@app.route('/search')
def search():
    query = request.args.get('q', '')
    mode = request.cookies.get('search_mode', 'inv_first')
    page = request.args.get('page', 1, type=int)
    token = request.args.get('token', None)
    proxy_type = request.cookies.get('proxy_type', 'wsrv.nl')
    search_type = request.cookies.get('search_type', 'video')
    date_format = request.cookies.get('date_format', 'ago')

    # Track which source provided the results (invidious or youtube)
    search_source = 'youtube'

    if not query:
        response = make_response(render_template('search.html', results=[], query="", proxy_type=proxy_type, mode=mode, search_type=search_type, date_format=date_format, search_source=search_source))
        response.set_cookie('proxy_type', proxy_type, max_age=2592000)
        response.set_cookie('search_mode', mode, max_age=2592000)
        response.set_cookie('search_type', search_type, max_age=2592000)
        response.set_cookie('date_format', date_format, max_age=2592000)
        return response

    results = None
    next_page = None

    if mode == 'inv_first':
        results, next_page = search_invidious(query, page, proxy_type, search_type)
        if results:
            search_source = 'invidious'
        else:
            results, next_page = search_youtube(query, token, proxy_type, search_type)
            search_source = 'youtube'
    else:
        results, next_page = search_youtube(query, token, proxy_type, search_type)
        search_source = 'youtube'
        if not results:
            results, next_page = search_invidious(query, page, proxy_type, search_type)
            search_source = 'invidious'

    response = make_response(render_template('search.html', results=results if results else [], query=query, mode=mode, next_page=next_page, page=page, proxy_type=proxy_type, search_type=search_type, date_format=date_format, search_source=search_source))
    response.set_cookie('proxy_type', proxy_type, max_age=2592000)
    response.set_cookie('search_mode', mode, max_age=2592000)
    response.set_cookie('search_type', search_type, max_age=2592000)
    response.set_cookie('date_format', date_format, max_age=2592000)
    return response

def get_japan_trend_by_category(category='all', proxy_type='self-hosted'):
    """
    日本トレンドをカテゴリ別に取得します

    Args:
        category: 'all' (全て), 'game' (ゲーム), 'music' (音楽)
        proxy_type: サムネイルプロキシの種類

    Returns:
        トレンド動画のリスト
    """
    results = []

    try:
        if category == 'all':
            # 全てカテゴリ: wakameリポジトリから取得
            url = "https://raw.githubusercontent.com/siawaseok3/wakame/refs/heads/master/trend.json"
        else:
            # ゲーム・音楽: ajgpwリポジトリから取得
            url = "https://raw.githubusercontent.com/ajgpw/youtubedata/refs/heads/main/trend-base64.json"

        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()

            # カテゴリ別に対応するキーを決定
            if category == 'all':
                # wakameリポジトリの場合は'trending'キーを使用
                trending_list = data.get('trending', data) if isinstance(data, dict) else data
            elif category == 'game':
                # ajgpwリポジトリのgamingキーを使用
                trending_list = data.get('gaming', [])
            elif category == 'music':
                # ajgpwリポジトリのmusicキーを使用
                trending_list = data.get('music', [])
            else:
                # デフォルト
                trending_list = data.get('trending', data) if isinstance(data, dict) else data

            video_ids = []
            for item in trending_list:
                v_id = item.get('id') or item.get('videoId')
                if not v_id: continue
                video_ids.append(v_id)

                published = item.get('published') or item.get('publishedAt') or item.get('uploadedAt') or ''
                results.append({
                    'id': v_id,
                    'title': item.get('title') or 'No Title',
                    'thumbnail': get_proxy_thumbnail(v_id, proxy_type),
                    'channel': item.get('channel') or item.get('author') or item.get('channelTitle') or item.get('uploader') or 'Unknown',
                    'duration': '',
                    'views': 'N/A',
                    'published_at': published
                })

            # Fetch duration and view count from YouTube API
            if video_ids:
                for key in YOUTUBE_API_KEYS:
                    try:
                        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={','.join(video_ids[:50])}&key={key}"
                        stats_response = requests.get(stats_url, timeout=5)
                        if stats_response.status_code == 200:
                            stats_data = stats_response.json()
                            stats_map = {item['id']: item for item in stats_data.get('items', [])}
                            for result in results:
                                if result['id'] in stats_map:
                                    item = stats_map[result['id']]
                                    duration = item.get('contentDetails', {}).get('duration', '')
                                    result['duration'] = parse_iso8601_duration(duration)

                                    # Check if live
                                    is_live = item.get('contentDetails', {}).get('projection', None) == 'live'
                                    if is_live:
                                        result['duration'] = 'LIVE'

                                    view_count = int(item.get('statistics', {}).get('viewCount', 0))
                                    if view_count >= 1000000:
                                        result['views'] = f"{view_count/1000000:.1f}M"
                                    elif view_count >= 1000:
                                        result['views'] = f"{view_count/1000:.1f}K"
                                    else:
                                        result['views'] = str(view_count)
                            break
                    except Exception as e:
                        logger.debug(f"Error fetching JP trend stats: {e}")
                        continue
    except Exception as e:
        logger.warning(f"Error fetching JP trend (category={category}): {e}")
        pass

    return results

@app.route('/trend')
def trend():
    region = request.cookies.get('trend_region', 'JP')
    proxy_type = request.cookies.get('proxy_type', 'wsrv.nl')
    date_format = request.cookies.get('date_format', 'ago')
    jp_category = request.cookies.get('trend_category', 'all')
    results = []

    # For non-JP regions, force 'ago' format only
    if region != 'JP':
        date_format = 'ago'

    if region == 'JP':
        results = get_japan_trend_by_category(jp_category, proxy_type)
    else:
        instances = INVIDIOUS_INSTANCES.copy()
        random.shuffle(instances)
        for instance in instances:
            url = f"{instance}/api/v1/trending?region={region}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    video_ids = []
                    for item in data:
                        try:
                            v_id = item.get('videoId', '')
                            if not v_id:
                                continue
                            video_ids.append(v_id)

                            length_seconds = item.get('lengthSeconds')
                            duration = format_time_seconds(length_seconds) if length_seconds else ''
                            view_count = item.get('viewCount', 0)
                            results.append({
                                'id': v_id,
                                'title': item.get('title', 'Untitled'),
                                'thumbnail': get_proxy_thumbnail(v_id, proxy_type),
                                'channel': item.get('author', 'Unknown Channel'),
                                'duration': duration,
                                'views': format_view_count(view_count) if view_count else 'N/A',
                                'published_at': item.get('publishedText', '')
                            })
                        except KeyError as e:
                            logger.debug(f"Error parsing trend item: {e}")
                            continue
                    break
            except Exception as e:
                logger.warning(f"Error fetching from {instance}: {e}")
                continue

    flask_response = make_response(render_template('trend.html', results=results, region=region, proxy_type=proxy_type, date_format=date_format, jp_category=jp_category))
    flask_response.set_cookie('proxy_type', proxy_type, max_age=2592000)
    flask_response.set_cookie('date_format', date_format, max_age=2592000)
    flask_response.set_cookie('trend_region', region, max_age=2592000)
    flask_response.set_cookie('trend_category', jp_category, max_age=2592000)
    return flask_response

@app.route('/api/thumbnail/<video_id>')
def proxy_thumbnail(video_id):
    """Self-hosted proxy thumbnail - fetches from YouTube and serves locally"""
    try:
        url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.content, 200, {'Content-Type': response.headers.get('Content-Type', 'image/jpeg')}
    except:
        pass
    # Fallback to 1x1 transparent pixel if fetch fails
    return bytes.fromhex(
        '47494638396101000100800000FFFFFF00000021F90400000000002C00000000010001000002024401003B'
    ), 200, {'Content-Type': 'image/gif'}


XEROX_API_LIST_URL = "https://raw.githubusercontent.com/choco-1515/About-youtube/refs/heads/main/stream/xerox-api.json"
_xerox_api_list_cache = None
_xerox_api_list_cache_time = 0

MIN2_TUBE_API_LIST_URL = "https://raw.githubusercontent.com/choco-1515/About-youtube/refs/heads/main/stream/min-tube-api.json"
_min2_tube_api_list_cache = None
_min2_tube_api_list_cache_time = 0


def fetch_xerox_api_list():
    """Fetch list of xerox API base URLs from GitHub JSON (cached 5 minutes)"""
    import time
    global _xerox_api_list_cache, _xerox_api_list_cache_time
    now = time.time()
    if _xerox_api_list_cache and (now - _xerox_api_list_cache_time) < 300:
        return _xerox_api_list_cache
    try:
        response = requests.get(XEROX_API_LIST_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                urls = [item if isinstance(item, str) else item.get('url', '') for item in data]
            elif isinstance(data, dict):
                urls = data.get('apis', data.get('urls', []))
            else:
                urls = []
            urls = [u for u in urls if u]
            if urls:
                _xerox_api_list_cache = urls
                _xerox_api_list_cache_time = now
                return urls
    except Exception:
        pass
    return _xerox_api_list_cache or []


# YouTube itag → (height, is_audio_only, label_hint)
_ITAG_INFO = {
    17: (144, False, 'mp4'), 18: (360, False, 'mp4'), 22: (720, False, 'mp4'),
    37: (1080, False, 'mp4'), 38: (3072, False, 'mp4'),
    82: (360, False, 'mp4'), 83: (480, False, 'mp4'), 84: (720, False, 'mp4'), 85: (1080, False, 'mp4'),
    133: (240, False, 'mp4v'), 134: (360, False, 'mp4v'), 135: (480, False, 'mp4v'),
    136: (720, False, 'mp4v'), 137: (1080, False, 'mp4v'), 138: (2160, False, 'mp4v'),
    160: (144, False, 'mp4v'), 264: (1440, False, 'mp4v'), 266: (2160, False, 'mp4v'),
    167: (360, False, 'webmv'), 168: (480, False, 'webmv'), 169: (1080, False, 'webmv'),
    218: (480, False, 'webmv'), 219: (144, False, 'webmv'),
    242: (240, False, 'webmv'), 243: (360, False, 'webmv'), 244: (480, False, 'webmv'),
    245: (480, False, 'webmv'), 246: (480, False, 'webmv'), 247: (720, False, 'webmv'),
    248: (1080, False, 'webmv'), 271: (1440, False, 'webmv'), 272: (2160, False, 'webmv'),
    302: (720, False, 'webmv'), 303: (1080, False, 'webmv'), 308: (1440, False, 'webmv'),
    313: (2160, False, 'webmv'), 315: (2160, False, 'webmv'),
    139: (0, True, 'm4a'), 140: (0, True, 'm4a'), 141: (0, True, 'm4a'),
    171: (0, True, 'webma'), 172: (0, True, 'webma'),
    249: (0, True, 'webma'), 250: (0, True, 'webma'), 251: (0, True, 'webma'),
}


def _xerox_build_label(url, quality='', height=0, container='mp4', is_audio=False):
    """URLパラメータと形式情報からボタン用ラベルを生成する"""
    from urllib.parse import urlparse, parse_qs
    import re
    try:
        params = parse_qs(urlparse(url).query)

        # itag から品質・フォーマットを補完
        itag_str = params.get('itag', [None])[0]
        if itag_str:
            try:
                itag_int = int(itag_str)
                info = _ITAG_INFO.get(itag_int)
                if info:
                    itag_h, itag_audio, itag_fmt = info
                    if not height and itag_h:
                        height = itag_h
                    if not is_audio and itag_audio:
                        is_audio = True
            except ValueError:
                pass

        # ビットレートを clen と dur から計算
        bitrate_str = ''
        clen = params.get('clen', [None])[0]
        dur = params.get('dur', [None])[0]
        if clen and dur:
            try:
                kbps = round(int(clen) * 8 / float(dur) / 1000)
                bitrate_str = f'{kbps}kbps'
            except Exception:
                pass

        # mime タイプを取得
        mime = params.get('mime', [''])[0]

        if is_audio or (mime and mime.startswith('audio')):
            # 音声のみ: ○kbps (フォーマット大文字)
            if 'webm' in mime:
                fmt = 'WebM'
            elif 'mp4' in mime or 'aac' in mime:
                fmt = 'M4A'
            else:
                fmt = (container or 'audio').upper()
            return f'{bitrate_str} ({fmt})' if bitrate_str else fmt
        else:
            # 映像: 解像度のみ ○p
            if not height and quality:
                m = re.match(r'(\d+)', quality)
                if m:
                    height = int(m.group(1))
            return f'{height}p' if height else (quality or 'Auto')
    except Exception:
        return quality or 'Auto'


def fetch_xerox_stream(api_url, video_id):
    """Fetch stream data from a single xerox API and return structured streams list"""
    try:
        response = requests.get(
            f"{api_url}/stream?id={video_id}",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            streams = []
            seen_urls = set()

            # formats[] から映像(+音声)ストリームを組み立てる
            for fmt in data.get('formats', []):
                url = fmt.get('url') or fmt.get('streamingUrl')
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                quality = fmt.get('quality', '')
                height = fmt.get('height', 0)
                container = fmt.get('container', 'mp4')
                label = _xerox_build_label(url, quality, height, container, is_audio=False)
                streams.append({
                    'url': url,
                    'quality': label,
                    'format': 'mp4',
                    'container': container,
                    'hasAudio': True,
                    'hasVideo': True,
                    'isHLS': False
                })

            # formats[] が空なら streamingUrl を使う
            streaming_url = data.get('streamingUrl') or data.get('url')
            if not streams and streaming_url and streaming_url not in seen_urls:
                seen_urls.add(streaming_url)
                label = _xerox_build_label(streaming_url, '', 0, 'mp4', is_audio=False)
                streams.append({
                    'url': streaming_url,
                    'quality': label,
                    'format': 'mp4',
                    'container': 'mp4',
                    'hasAudio': True,
                    'hasVideo': True,
                    'isHLS': False
                })

            # audioUrl → 音声のみカテゴリ
            audio_url = data.get('audioUrl')
            if audio_url and audio_url not in seen_urls:
                seen_urls.add(audio_url)
                label = _xerox_build_label(audio_url, '', 0, 'm4a', is_audio=True)
                streams.append({
                    'url': audio_url,
                    'quality': label,
                    'format': 'audio',
                    'container': 'm4a',
                    'hasAudio': True,
                    'hasVideo': False,
                    'isHLS': False
                })

            return streams if streams else None
    except Exception:
        pass
    return None


def fetch_min2_tube_api_list():
    """Fetch list of min2-tube API base URLs from GitHub JSON (cached 5 minutes)"""
    import time
    global _min2_tube_api_list_cache, _min2_tube_api_list_cache_time
    now = time.time()
    if _min2_tube_api_list_cache and (now - _min2_tube_api_list_cache_time) < 300:
        return _min2_tube_api_list_cache
    try:
        response = requests.get(MIN2_TUBE_API_LIST_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                urls = [item if isinstance(item, str) else item.get('url', '') for item in data]
            elif isinstance(data, dict):
                urls = data.get('apis', data.get('urls', []))
            else:
                urls = []
            urls = [u for u in urls if u]
            if urls:
                _min2_tube_api_list_cache = urls
                _min2_tube_api_list_cache_time = now
                return urls
    except Exception:
        pass
    return _min2_tube_api_list_cache or []


def _min2_stream_entry(url, seen_urls, quality='', height=0, container='mp4',
                        is_audio=False, is_video_only=False, is_hls=False):
    """min2-tube用: URLから1ストリームエントリを生成して返す（重複チェック付き）"""
    from urllib.parse import urlparse, parse_qs
    if not url or url in seen_urls:
        return None
    seen_urls.add(url)

    # itag から format/hasAudio/hasVideo/container を自動判定
    try:
        params = parse_qs(urlparse(url).query)
        itag_str = params.get('itag', [None])[0]
        if itag_str:
            itag_int = int(itag_str)
            info = _ITAG_INFO.get(itag_int)
            if info:
                itag_h, itag_is_audio, itag_fmt = info
                if not height and itag_h:
                    height = itag_h
                if itag_is_audio:
                    is_audio = True
                elif itag_fmt.endswith('v'):
                    is_video_only = True
                # コンテナ判定
                if 'webm' in itag_fmt:
                    container = 'webm'
                elif 'mp4' in itag_fmt or itag_fmt == 'm4a':
                    container = 'mp4' if not itag_is_audio else 'm4a'
        # mime から is_audio / container を補完
        mime = params.get('mime', [''])[0]
        if mime:
            if mime.startswith('audio'):
                is_audio = True
            if 'webm' in mime:
                container = 'webm'
            elif 'mp4' in mime:
                container = 'mp4' if not is_audio else 'm4a'
    except Exception:
        pass

    if is_hls:
        return {
            'url': url, 'quality': 'Auto (HLS)', 'format': 'hls',
            'container': 'm3u8', 'hasAudio': True, 'hasVideo': True, 'isHLS': True
        }

    if is_audio:
        label = _xerox_build_label(url, quality, height, container or 'm4a', is_audio=True)
        return {
            'url': url, 'quality': label or 'M4A', 'format': 'audio',
            'container': container or 'm4a', 'hasAudio': True, 'hasVideo': False, 'isHLS': False
        }
    elif is_video_only:
        label = _xerox_build_label(url, quality, height, container, is_audio=False)
        return {
            'url': url, 'quality': label or 'Auto', 'format': 'video',
            'container': container, 'hasAudio': False, 'hasVideo': True, 'isHLS': False
        }
    else:
        label = _xerox_build_label(url, quality, height, container, is_audio=False)
        return {
            'url': url, 'quality': label or 'Auto', 'format': 'mp4',
            'container': container, 'hasAudio': True, 'hasVideo': True, 'isHLS': False
        }


def fetch_min2_tube_stream(api_url, video_id):
    """Fetch streams from a single min2-tube API. Supports various response formats."""
    try:
        response = requests.get(
            f"{api_url}/api/video/{video_id}",
            timeout=10
        )
        if response.status_code != 200:
            return None

        data = response.json()
        streams = []
        seen_urls = set()

        # --- formats[] 配列対応（xerox互換）---
        for fmt in data.get('formats', []):
            url = fmt.get('url') or fmt.get('stream_url') or fmt.get('streamingUrl')
            quality = fmt.get('quality', '') or fmt.get('qualityLabel', '')
            height = fmt.get('height', 0)
            container = fmt.get('container', 'mp4')
            # hasAudio/hasVideo フラグで判定
            has_audio = fmt.get('hasAudio', True)
            has_video = fmt.get('hasVideo', True)
            is_hls = fmt.get('isHLS', False) or (container in ('m3u8', 'hls'))
            is_audio = (not has_video) or fmt.get('audio_only', False)
            is_video_only = (not has_audio) and has_video
            entry = _min2_stream_entry(url, seen_urls, quality, height, container,
                                       is_audio, is_video_only, is_hls)
            if entry:
                streams.append(entry)

        # --- adaptiveFormats[] ---
        for fmt in data.get('adaptiveFormats', []):
            url = fmt.get('url') or fmt.get('stream_url')
            quality = fmt.get('qualityLabel', '') or fmt.get('quality', '')
            height = fmt.get('height', 0)
            container = fmt.get('container', 'mp4')
            mime = fmt.get('type', '') or fmt.get('mimeType', '')
            is_audio = mime.startswith('audio') if mime else False
            is_video_only = (mime.startswith('video') and not is_audio) if mime else False
            entry = _min2_stream_entry(url, seen_urls, quality, height, container,
                                       is_audio, is_video_only, False)
            if entry:
                streams.append(entry)

        # --- formatStreams[] ---
        for fmt in data.get('formatStreams', []):
            url = fmt.get('url', '')
            quality = fmt.get('qualityLabel', '') or fmt.get('quality', '')
            container = fmt.get('container', 'mp4')
            entry = _min2_stream_entry(url, seen_urls, quality, 0, container,
                                       False, False, False)
            if entry:
                streams.append(entry)

        # --- stream_url / streamingUrl / url（単一ストリーム）---
        main_url = data.get('stream_url') or data.get('streamingUrl') or data.get('url')
        entry = _min2_stream_entry(main_url, seen_urls, '', 0, 'mp4', False, False, False)
        if entry:
            streams.append(entry)

        # --- audioUrl ---
        entry = _min2_stream_entry(
            data.get('audioUrl') or data.get('audio_url'),
            seen_urls, '', 0, 'm4a', True, False, False
        )
        if entry:
            streams.append(entry)

        # --- videoUrl（映像のみ）---
        entry = _min2_stream_entry(
            data.get('videoUrl') or data.get('video_url'),
            seen_urls, '', 0, 'mp4', False, True, False
        )
        if entry:
            streams.append(entry)

        # --- hlsUrl ---
        entry = _min2_stream_entry(
            data.get('hlsUrl') or data.get('hls_url'),
            seen_urls, '', 0, 'm3u8', False, False, True
        )
        if entry:
            streams.append(entry)

        return streams if streams else None
    except Exception:
        pass
    return None


_invidious_working_cache = []  # 動作済みインスタンスのメモリキャッシュ

@app.route('/api/invidious-stream/<video_id>')
def invidious_stream(video_id):
    """Wista方式: 全ストリーム専用インスタンスに並行レースリクエストして最速レスポンスのストリームを返す"""
    global _invidious_working_cache
    # ?exclude=https://inst1.example.com,https://inst2.example.com で除外
    exclude_param = request.args.get('exclude', '')
    exclude_set = set(u.strip() for u in exclude_param.split(',') if u.strip())
    ERROR_KEYWORDS = ["shutdown", "<!DOCTYPE", "<html", "temporarily unavailable", "maintenance"]
    YOUTUBE_RESTRICT_KEYWORDS = ["protect our community", "Sign in to confirm", "age-restricted",
                                  "This video is unavailable", "not available in your country"]

    def fetch_from_instance(instance):
        try:
            url = f"{instance}/api/v1/videos/{video_id}"
            response = requests.get(url, timeout=6, headers=BROWSER_HEADERS, allow_redirects=True)
            if response.status_code not in (200, 500):
                return None

            text = response.text
            if any(kw.lower() in text.lower() for kw in ERROR_KEYWORDS):
                return None

            # YouTube制限エラーを検出して専用マーカーで返す
            if any(kw.lower() in text.lower() for kw in YOUTUBE_RESTRICT_KEYWORDS):
                return {'youtube_restricted': True}

            data = response.json()
            if not data.get('title'):
                # Invidious が error フィールドを返している場合
                if data.get('error'):
                    err = data['error']
                    if any(kw.lower() in err.lower() for kw in YOUTUBE_RESTRICT_KEYWORDS):
                        return {'youtube_restricted': True}
                return None

            streams = []

            if data.get('hlsUrl'):
                streams.append({
                    'url': data['hlsUrl'],
                    'quality': 'Auto (HLS)',
                    'format': 'hls',
                    'container': 'm3u8',
                    'hasAudio': True,
                    'hasVideo': True,
                    'isHLS': True,
                    'isLive': bool(data.get('liveNow')),
                })

            for fmt in data.get('formatStreams', []):
                url = fmt.get('url', '')
                if not url:
                    continue
                quality = fmt.get('qualityLabel') or fmt.get('quality') or 'Unknown'
                container = fmt.get('container', 'mp4')
                streams.append({
                    'url': url,
                    'quality': quality,
                    'format': 'mp4',
                    'container': container,
                    'hasAudio': True,
                    'hasVideo': True,
                    'isHLS': False,
                    'isLive': False,
                })

            for fmt in data.get('adaptiveFormats', []):
                url = fmt.get('url', '')
                if not url:
                    continue
                # codec フィールドが空の場合、type (MIMEタイプ) と encoding から判定する
                codec = fmt.get('codec', '') or fmt.get('encoding', '')
                mime_type = fmt.get('type', '')
                # type フィールドからコーデック文字列を補完
                if not codec and mime_type:
                    codec = mime_type
                codec_lower = codec.lower()
                mime_lower = mime_type.lower()
                quality = fmt.get('qualityLabel') or fmt.get('quality') or ''
                bitrate = fmt.get('bitrate', '')
                container = fmt.get('container', 'mp4')

                is_video_mime = mime_lower.startswith('video/')
                is_audio_mime = mime_lower.startswith('audio/')

                if is_video_mime or any(vc in codec_lower for vc in ['vp9', 'vp8', 'av1', 'h264', 'h265', 'avc1']):
                    if any(x in codec_lower for x in ['vp9', 'vp8', 'av1', 'vp09']):
                        codec_label = 'WebM'
                        container = container or 'webm'
                    else:
                        codec_label = 'H.264'
                        container = container or 'mp4'
                    q = quality.split(' ')[0] if quality else 'unknown'
                    streams.append({
                        'url': url,
                        'quality': f"{q} ({codec_label})",
                        'format': 'video',
                        'container': container,
                        'hasAudio': False,
                        'hasVideo': True,
                        'isHLS': False,
                        'isLive': False,
                    })
                elif is_audio_mime or any(ac in codec_lower for ac in ['opus', 'aac', 'mp4a', 'vorbis', 'mp3']):
                    br_raw = int(str(bitrate).split('.')[0]) if bitrate else 0
                    br = f"{round(br_raw / 1000)}" if br_raw > 1000 else str(br_raw)
                    if 'opus' in codec_lower:
                        label = f"{br} kbps (WebM)"
                    elif 'aac' in codec_lower or 'mp4a' in codec_lower:
                        label = f"{br} kbps (M4A)"
                    elif 'vorbis' in codec_lower:
                        label = f"{br} kbps (Vorbis)"
                    else:
                        enc = fmt.get('encoding', 'audio')
                        label = f"{br} kbps ({enc.upper() if enc else 'Audio'})"
                    streams.append({
                        'url': url,
                        'quality': label,
                        'format': 'audio',
                        'container': container,
                        'hasAudio': True,
                        'hasVideo': False,
                        'isHLS': False,
                        'isLive': False,
                    })

            if streams:
                return {
                    'streams': streams,
                    'hlsUrl': data.get('hlsUrl'),
                    'isLive': bool(data.get('liveNow')),
                    'title': data.get('title', ''),
                    'author': data.get('author', ''),
                    'instance': instance,
                }
        except Exception as e:
            logger.debug(f"Invidious stream error ({instance}): {e}")
        return None

    # 動作済みキャッシュを優先、残りをランダム順で追加（除外リストを除く）
    cached = [i for i in _invidious_working_cache if i in INVIDIOUS_STREAM_INSTANCES and i not in exclude_set]
    rest = [i for i in INVIDIOUS_STREAM_INSTANCES if i not in cached and i not in exclude_set]
    random.shuffle(rest)
    instances = cached + rest

    BATCH_SIZE = 7
    result = None
    youtube_restricted = False

    # 7個ずつバッチに分けて並列リクエスト、1件成功したら即終了
    for batch_start in range(0, len(instances), BATCH_SIZE):
        batch = instances[batch_start:batch_start + BATCH_SIZE]
        logger.debug(f"[Invidious] Batch {batch_start // BATCH_SIZE + 1}: trying {[b.split('//')[1] for b in batch]}")
        with ThreadPoolExecutor(max_workers=len(batch)) as executor:
            futures = {executor.submit(fetch_from_instance, inst): inst for inst in batch}
            try:
                for future in as_completed(futures, timeout=10):
                    try:
                        res = future.result(timeout=2)
                        if res:
                            if res.get('youtube_restricted'):
                                youtube_restricted = True
                                continue
                            if res.get('streams'):
                                result = res
                                inst_url = res['instance']
                                if inst_url not in _invidious_working_cache:
                                    _invidious_working_cache.insert(0, inst_url)
                                    _invidious_working_cache[:] = _invidious_working_cache[:8]
                                logger.info(f"[Invidious] Success from {inst_url} (batch {batch_start // BATCH_SIZE + 1})")
                                break
                    except Exception:
                        continue
            except TimeoutError:
                logger.warning(f"[Invidious] Batch {batch_start // BATCH_SIZE + 1} timed out")
        if result:
            break

    if result:
        return jsonify({
            'success': True,
            'streams': result['streams'],
            'hlsUrl': result.get('hlsUrl'),
            'isLive': result.get('isLive', False),
            'title': result.get('title', ''),
            'author': result.get('author', ''),
            'instance': result.get('instance', ''),
        })

    if youtube_restricted:
        return jsonify({'success': False, 'error': 'youtube_restricted',
                        'message': 'この動画はYouTubeの制限により再生できません（年齢制限・地域制限など）'}), 403

    return jsonify({'success': False, 'error': 'instance_unavailable',
                    'message': 'ストリームの取得に失敗しました。クライアント側で再試行します...'}), 503


@app.route('/api/stream/<video_id>')
def get_stream(video_id):
    """Fetch streams from xerox APIs in parallel; fall back to min2-tube API if all xerox fail.
    Query param: exclude=xerox,min2tube  (comma-separated API group names to skip)
    Response includes: source='xerox'|'min2tube'
    """
    exclude_raw = request.args.get('exclude', '')
    exclude_set = set(e.strip().lower() for e in exclude_raw.split(',') if e.strip())

    result_streams = None
    used_source = None

    # --- xerox API グループ ---
    if 'xerox' not in exclude_set:
        api_list = fetch_xerox_api_list()
        if api_list:
            with ThreadPoolExecutor(max_workers=len(api_list)) as executor:
                futures = {
                    executor.submit(fetch_xerox_stream, api, video_id): api
                    for api in api_list
                }
                for future in as_completed(futures):
                    try:
                        streams = future.result()
                        if streams:
                            result_streams = streams
                            used_source = 'xerox'
                            for f in futures:
                                f.cancel()
                            break
                    except Exception:
                        continue

    if result_streams:
        return jsonify({'streams': result_streams, 'source': used_source})

    # --- min2-tube API グループ（フォールバック）---
    if 'min2tube' not in exclude_set:
        min2_api_list = fetch_min2_tube_api_list()
        if min2_api_list:
            with ThreadPoolExecutor(max_workers=len(min2_api_list)) as executor:
                futures = {
                    executor.submit(fetch_min2_tube_stream, api, video_id): api
                    for api in min2_api_list
                }
                for future in as_completed(futures):
                    try:
                        streams = future.result()
                        if streams:
                            result_streams = streams
                            used_source = 'min2tube'
                            for f in futures:
                                f.cancel()
                            break
                    except Exception:
                        continue

    if result_streams:
        return jsonify({'streams': result_streams, 'source': used_source})
    else:
        return jsonify({'error': 'ストリームを取得できませんでした'}), 503



@app.route('/watch/<video_id>')
def watch(video_id):
    metadata = {
        'video_title': None,
        'view_count': None,
        'published_at': None,
        'channel_name': None,
        'subscriber_count': None,
        'channel_icon': None
    }

    for key in YOUTUBE_API_KEYS[:3]:
        try:
            url = (
                f"https://www.googleapis.com/youtube/v3/"
                f"videos?part=snippet,statistics&id={video_id}&key={key}"
            )
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                if items:
                    item = items[0]
                    metadata['video_title'] = item['snippet'].get('title')
                    metadata['published_at'] = (
                        item['snippet'].get('publishedAt', '').split('T')[0]
                    )

                    view_count = int(
                        item['statistics'].get('viewCount', 0)
                    )
                    if view_count >= 1000000:
                        metadata['view_count'] = (
                            f"{view_count/1000000:.1f}M"
                        )
                    elif view_count >= 1000:
                        metadata['view_count'] = f"{view_count/1000:.1f}K"
                    else:
                        metadata['view_count'] = str(view_count)

                    channel_id = item['snippet']['channelId']
                    channel_url = (
                        f"https://www.googleapis.com/youtube/v3/"
                        f"channels?part=snippet,statistics&id="
                        f"{channel_id}&key={key}"
                    )
                    channel_response = requests.get(
                        channel_url,
                        timeout=5
                    )
                    if channel_response.status_code == 200:
                        channel_data = channel_response.json()
                        channel_items = channel_data.get('items', [])
                        if channel_items:
                            ch = channel_items[0]
                            metadata['channel_name'] = (
                                ch['snippet'].get('title')
                            )

                            subs = int(
                                ch['statistics'].get('subscriberCount', 0)
                            )
                            if subs >= 1000000:
                                metadata['subscriber_count'] = (
                                    f"{subs/1000000:.1f}M"
                                )
                            elif subs >= 1000:
                                metadata['subscriber_count'] = (
                                    f"{subs/1000:.1f}K"
                                )
                            else:
                                metadata['subscriber_count'] = str(subs)

                            thumbnails = ch['snippet'].get('thumbnails', {})
                            metadata['channel_icon'] = (
                                thumbnails.get('high', {}).get('url')
                                or thumbnails.get('default', {}).get('url')
                            )
                    break
        except Exception:
            continue

    return render_template('watch.html', video_id=video_id, **metadata)

def format_view_count(count):
    if isinstance(count, str):
        try:
            count = int(count)
        except:
            return count
    if count >= 1000000:
        return f"{count/1000000:.1f}M"
    elif count >= 1000:
        return f"{count/1000:.1f}K"
    return str(count)

def parse_duration_to_seconds(duration_str):
    """Parse ISO 8601 duration to seconds"""
    if not duration_str:
        return 0
    try:
        import re
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0
            return hours * 3600 + minutes * 60 + seconds
        return 0
    except:
        return 0

def format_time_seconds(seconds):
    """Format seconds to MM:SS or H:MM:SS"""
    try:
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    except:
        return ""

def format_date_with_cookie(iso_date_str, date_format=None, is_invidious_text=False):
    """Format ISO 8601 date based on cookie preference or parameter

    Args:
        iso_date_str: ISO 8601 date string or Invidious publishedText
        date_format: 'ago' or 'date'
        is_invidious_text: True if the input is already formatted Invidious text
    """
    if not iso_date_str:
        return ""

    # If it's already Invidious formatted text (like "1 month ago"), return as-is
    if is_invidious_text:
        return iso_date_str

    try:
        from datetime import datetime
        # Parse ISO 8601 format
        if 'T' in iso_date_str:
            dt = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(iso_date_str)

        # If format not specified, default to 'ago'
        if date_format is None:
            date_format = 'ago'

        # YYYY-MM-DD format
        if date_format == 'date':
            return dt.strftime('%Y-%m-%d')

        # ~ago format (default)
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.utcnow()
        delta = now - dt
        days = delta.days
        seconds = delta.total_seconds()

        if seconds < 60:
            return "now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif days == 0:
            return "today"
        elif days == 1:
            return "1 day ago"
        elif days < 7:
            return f"{days} days ago"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    except:
        return iso_date_str

def format_relative_date(iso_date_str):
    """Format ISO 8601 date to relative time format (for backward compatibility)"""
    return format_date_with_cookie(iso_date_str, 'ago')

def get_video_details(video_id, key):
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails&id={video_id}&key={key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                item = data['items'][0]
                view_count = item.get('statistics', {}).get('viewCount', '0')
                duration = item.get('contentDetails', {}).get('duration', '')
                return {
                    'views': format_view_count(view_count),
                    'duration': duration
                }
    except:
        pass
    return {'views': '0', 'duration': ''}

@app.route('/channel/<channel_id>')
def channel(channel_id):
    channel = None
    all_videos = []
    videos = []
    shorts = []

    try:
        channel_data = None
        channel_source = None

        # Try YouTube API first
        for key in YOUTUBE_API_KEYS:
            try:
                url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={key}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('items'):
                        channel_data = data['items'][0]
                        channel_source = 'youtube'
                        break
            except Exception as e:
                logger.debug(f"Error fetching channel info: {e}")
                continue

        # Fallback to Invidious if YouTube API fails
        if not channel_data:
            instances = INVIDIOUS_INSTANCES.copy()
            random.shuffle(instances)
            for instance in instances:
                try:
                    url = f"{instance}/api/v1/channels/{channel_id}"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        channel_data = response.json()
                        channel_source = 'invidious'
                        break
                except Exception as e:
                    logger.debug(f"Invidious channel error: {e}")
                    continue

        # Fetch videos using uploads playlist
        uploads_playlist_id = None
        if channel_source == 'youtube' and channel_data:
            uploads_playlist_id = f"UU{channel_id[2:]}"

        for key in YOUTUBE_API_KEYS:
            try:
                if uploads_playlist_id:
                    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist_id}&maxResults=50&key={key}"
                else:
                    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&order=date&maxResults=50&key={key}"

                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    video_ids = []
                    for item in data.get('items', []):
                        try:
                            if 'playlistItems' in url:
                                v_id = item['snippet']['resourceId']['videoId']
                            else:
                                v_id = item['id']['videoId']
                            video_ids.append(v_id)
                            all_videos.append({
                                'id': v_id,
                                'title': item['snippet']['title'],
                                'published': item['snippet']['publishedAt'][:10] if 'publishedAt' in item['snippet'] else '',
                                'views': '0',
                                'length': '',
                                'is_short': False
                            })
                        except KeyError as e:
                            logger.debug(f"Error parsing video item: {e}")
                            continue

                    # Fetch video details to get duration and statistics
                    if video_ids:
                        try:
                            details_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics&id={','.join(video_ids)}&key={key}"
                            details_response = requests.get(details_url, timeout=5)
                            if details_response.status_code == 200:
                                details_data = details_response.json()
                                details_map = {item['id']: item for item in details_data.get('items', [])}
                                for video in all_videos:
                                    if video['id'] in details_map:
                                        duration_str = details_map[video['id']].get('contentDetails', {}).get('duration', '')
                                        video['length'] = parse_iso8601_duration(duration_str)
                                        # Check if it's a short (duration <= 60 seconds)
                                        duration = parse_duration_to_seconds(duration_str)
                                        video['is_short'] = duration <= 60
                                        # Get view count
                                        view_count = details_map[video['id']].get('statistics', {}).get('viewCount', '0')
                                        video['views'] = format_view_count(view_count)
                        except Exception as e:
                            logger.debug(f"Error fetching video details: {e}")
                    break
            except Exception as e:
                logger.debug(f"Error fetching channel videos: {e}")
                continue

        # If YouTube API videos fetch failed, try Invidious
        if not all_videos and channel_source:
            instances = INVIDIOUS_INSTANCES.copy()
            random.shuffle(instances)
            for instance in instances:
                try:
                    url = f"{instance}/api/v1/channels/{channel_id}/latest"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        for item in data:
                            try:
                                v_id = item.get('videoId')
                                if v_id:
                                    view_count = item.get('viewCount', 0)
                                    length = item.get('lengthSeconds', 0)
                                    all_videos.append({
                                        'id': v_id,
                                        'title': item.get('title', 'Unknown'),
                                        'published': item.get('published', ''),
                                        'views': format_view_count(view_count),
                                        'length': format_time_seconds(length),
                                        'is_short': int(length) <= 60
                                    })
                            except Exception as e:
                                logger.debug(f"Error parsing invidious video: {e}")
                                continue
                        break
                except Exception as e:
                    logger.debug(f"Invidious videos error: {e}")
                    continue

        # Separate videos and shorts
        for video in all_videos:
            if video['is_short']:
                shorts.append(video)
            else:
                videos.append(video)

        if channel_data:
            channel = {}
            if channel_source == 'youtube':
                try:
                    if 'snippet' in channel_data:
                        channel['channelName'] = channel_data['snippet'].get('title', 'Unknown')
                        channel['channelProfile'] = channel_data['snippet'].get('description', '')
                        thumbnails = channel_data['snippet'].get('thumbnails', {})
                        if thumbnails:
                            channel['channelIcon'] = thumbnails.get('high', {}).get('url') or thumbnails.get('default', {}).get('url')

                    if 'statistics' in channel_data:
                        sub_count = channel_data['statistics'].get('subscriberCount')
                        if sub_count:
                            channel['subscribers'] = int(sub_count)

                        view = channel_data['statistics'].get('viewCount')
                        if view:
                            channel['totalViews'] = int(view)
                except Exception as e:
                    logger.error(f"Error processing YouTube channel data: {e}")
            elif channel_source == 'invidious':
                try:
                    channel['channelName'] = channel_data.get('author', 'Unknown')
                    channel['channelProfile'] = channel_data.get('description', '')
                    thumbnails = channel_data.get('authorThumbnails', [])
                    if thumbnails:
                        channel['channelIcon'] = thumbnails[0].get('url')

                    sub_count = channel_data.get('subCount')
                    if sub_count:
                        channel['subscribers'] = int(sub_count)
                except Exception as e:
                    logger.error(f"Error processing Invidious channel data: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in channel route: {e}", exc_info=True)

    date_format = request.cookies.get('date_format', 'ago')
    return render_template('channel.html', channel=channel, videos=videos, shorts=shorts, date_format=date_format)

@app.route('/api/channel/<channel_id>/more')
def channel_more(channel_id):
    video_type = request.args.get('type', 'videos')
    offset = request.args.get('offset', 0, type=int)

    all_videos = []

    try:
        uploads_playlist_id = f"UU{channel_id[2:]}"

        for key in YOUTUBE_API_KEYS:
            try:
                url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist_id}&maxResults=50&startIndex={offset+1}&key={key}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    video_ids = []
                    for item in data.get('items', []):
                        try:
                            v_id = item['snippet']['resourceId']['videoId']
                            video_ids.append(v_id)
                            all_videos.append({
                                'id': v_id,
                                'title': item['snippet']['title'],
                                'published': item['snippet']['publishedAt'][:10] if 'publishedAt' in item['snippet'] else '',
                                'views': '0',
                                'length': '',
                                'is_short': False
                            })
                        except KeyError:
                            continue

                    if video_ids:
                        try:
                            details_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={','.join(video_ids)}&key={key}"
                            details_response = requests.get(details_url, timeout=5)
                            if details_response.status_code == 200:
                                details_data = details_response.json()
                                details_map = {item['id']: item for item in details_data.get('items', [])}
                                for video in all_videos:
                                    if video['id'] in details_map:
                                        duration_str = details_map[video['id']].get('contentDetails', {}).get('duration', '')
                                        video['length'] = parse_iso8601_duration(duration_str)
                                        duration = parse_duration_to_seconds(duration_str)
                                        video['is_short'] = duration <= 60
                        except:
                            pass
                    break
            except Exception as e:
                logger.debug(f"Error fetching more videos: {e}")
                continue

        # Filter by type
        result_videos = []
        for video in all_videos:
            if video_type == 'videos' and not video['is_short']:
                result_videos.append(video)
            elif video_type == 'shorts' and video['is_short']:
                result_videos.append(video)

        return jsonify({'videos': result_videos})
    except Exception as e:
        logger.error(f"Error in channel_more: {e}")
        return jsonify({'videos': []})

# Register Jinja2 filters
app.jinja_env.filters['format_relative_date'] = format_relative_date
app.jinja_env.filters['format_date'] = format_date_with_cookie

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
