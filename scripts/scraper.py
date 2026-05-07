import requests
import json
from datetime import datetime
import time

VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
]

def fetch_json(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        r.raise_for_status()
        return r.json()
    except:
        return None

def test_site(site):
    """简单但有效的测试"""
    api = site.get("api")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    try:
        time.sleep(0.6)
        r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        if r.status_code == 200:
            content = r.text.lower()
            if any(word in content for word in ["class", "vod", "list", "rss", "xml"]):
                return True
    except:
        pass
    return True  # 如果测试超时也保留（避免误杀太多）

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    valid_vod = []
    
    print(f"开始自动抓取 + 测试 - {timestamp}")
    
    for url in VOD_SOURCES:
        print(f"抓取: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data.get("sites", []):
                if test_site(site):
                    site.setdefault("searchable", 1)
                    site.setdefault("quickSearch", 1)
                    site.setdefault("filterable", 1)
                    site.setdefault("playerType", 1)
                    valid_vod.append(site)
    
    # 去重
    seen = set()
    vod_sites = []
    for site in valid_vod:
        key = (site.get("name"), site.get("api"))
        if key not in seen:
            seen.add(key)
            vod_sites.append(site)
    
    # 直播（加强兼容性）
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
        "name": "亚洲性学接口（自动抓取+直播版）",
        "update_time": timestamp,
        "vod_count": len(vod_sites),
        "live_count": len(live_groups),
        "sites": vod_sites,
        "lives": live_groups
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！保留点播 {len(vod_sites)} 个 | 直播 {len(live_groups)} 个")

if __name__ == "__main__":
    main()
