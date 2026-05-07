import requests
import json
from datetime import datetime
import time

# 点播源 (VOD)
VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
    "https://raw.githubusercontent.com/Dong-learn9/TVBox-zyjk/main/18.json",
]

# 直播源 (Live)
LIVE_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u",
    "https://live.adultiptv.net/asian.m3u8",
    "https://live.adultiptv.net/livecams.m3u8",
    "https://raw.githubusercontent.com/hujingguang/ChinaIPTV/main/xxx.m3u8",
]

def fetch_json(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=12)
        r.raise_for_status()
        if url.endswith(('.m3u', '.m3u8')):
            return {"type": "m3u", "content": r.text}
        return r.json()
    except:
        return None

def is_valid_vod_site(site):
    """放宽测试条件，只要有 api 就基本保留"""
    api = site.get("api")
    if not api or not isinstance(api, str):
        return False
    # 只要有 api 地址就保留（让客户端自己加载）
    return api.startswith("http")

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    vod_sites = []
    live_groups = []
    
    print(f"开始抓取 - {timestamp}")

    # 抓取点播
    for url in VOD_SOURCES:
        print(f"抓取点播源: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data.get("sites", []):
                if is_valid_vod_site(site):
                    vod_sites.append(site)
    
    # 抓取直播（直接添加常用链接）
    live_groups = [
        {
            "name": "亚洲成人直播",
            "type": 1,
            "url": "https://live.adultiptv.net/asian.m3u8"
        },
        {
            "name": "成人直播合集",
            "type": 1,
            "url": "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u"
        },
        {
            "name": "Live Cams",
            "type": 1,
            "url": "https://live.adultiptv.net/livecams.m3u8"
        }
    ]

    output = {
        "name": "我的亚洲性学接口（优化版）",
        "update_time": timestamp,
        "vod_count": len(vod_sites),
        "live_count": len(live_groups),
        "sites": vod_sites,
        "lives": live_groups
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！点播站点: {len(vod_sites)} 个 | 直播分组: {len(live_groups)} 个")

if __name__ == "__main__":
    main()
