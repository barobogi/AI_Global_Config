# -*- coding: utf-8 -*-
import urllib.request
import re
import json

def parse_yt_initial_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
            if not match:
                match = re.search(r'window\["ytInitialData"\] = (\{.*?\});</script>', html)
            if match:
                data = json.loads(match.group(1))
                return data, html
            else:
                return None, html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, ""

def find_titles(obj, titles):
    if isinstance(obj, dict):
        if 'videoRenderer' in obj:
            vr = obj['videoRenderer']
            title = vr.get('title', {}).get('runs', [{}])[0].get('text', '')
            vid = vr.get('videoId', '')
            if title:
                titles.append(f"[본편/동영상] {title} (https://youtu.be/{vid})")
        elif 'reelItemRenderer' in obj:
            rr = obj['reelItemRenderer']
            title = rr.get('headline', {}).get('simpleText', '') or rr.get('title', {}).get('runs', [{}])[0].get('text', '')
            vid = rr.get('videoId', '')
            if title:
                titles.append(f"[쇼츠] {title} (https://youtu.be/{vid})")
        for v in obj.values():
            find_titles(v, titles)
    elif isinstance(obj, list):
        for item in obj:
            find_titles(item, titles)

def main():
    for page in ["videos", "shorts"]:
        url = f"https://www.youtube.com/@3ai-lab/{page}"
        data, html = parse_yt_initial_data(url)
        titles = []
        if data:
            find_titles(data, titles)
        print(f"\n=== {page.upper()} 페이지 파싱 결과 ===")
        unique_titles = list(dict.fromkeys(titles))
        if unique_titles:
            for t in unique_titles:
                print(t)
        else:
            print("파싱된 항목 없음. Regex 검색:")
            matches = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\]', html)
            for m in set(matches):
                print(f"- {m}")

if __name__ == "__main__":
    main()
