import requests
import json
from datetime import datetime
import time

# 多个源自动抓取
VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
    "https://raw.githubusercontent.com/Dong-learn9/TVBox-zyjk/main/18.json",
]

def fetch_json(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        r.raise_for_status()
        return r.json()
    except:
        return None

def is_likely_valid(site):
    """温和测试：只要有 api 地址就保留（减少误杀）"""
    api = site.get("api", "")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    name = site.get("name", "").lower()
    # 排除明显无效的
    if "测试" in name or "备用" in name or len(name) < 2:
        return False
    return True

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    all_vod = []
    
    print(f"开始自动抓取 - {timestamp}")
    
    for url in VOD_SOURCES:
        print(f"正在抓取: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data.get("sites", []):
                if is_likely_valid(site):
                    # 统一添加兼容字段
                    site.setdefault("searchable", 1)
                    site.setdefault("quickSearch", 1)
                    site.setdefault("filterable", 1)
                    site.setdefault("playerType", 1)
                    all_vod.append(site)
    
    # 去重（按 name + api）
    seen = {}
    vod_sites = []
    for site in all_vod:
        key = f"{site.get('name')}-{site.get('api')}"
        if key not in seen:
            seen[key] = True
            vod_sites.append(site)
    
    # 直播分组
    live_groups = [
        {"name": "亚洲成人直播", "type": 1, "url": "https://live.adultiptv.net/asian.m3u8"},
        {"name": "成人直播合集", "type": 1, "url": "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u"},
        {"name": "Live Cams", "type": 1, "url": "https://live.adultiptv.net/livecams.m3u8"}
    ]

    output = {
        "name": "亚洲性学接口（自动抓取版）",
        "update_time": timestamp,
        "vod_count": len(vod_sites),
        "live_count": len(live_groups),
        "sites": vod_sites,
        "lives": live_groups
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 自动抓取完成！保留点播站点: {len(vod_sites)} 个")

if __name__ == "__main__":
    main()
