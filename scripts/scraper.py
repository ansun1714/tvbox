import requests
import json
from datetime import datetime

VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
    "https://raw.githubusercontent.com/Dong-learn9/TVBox-zyjk/main/18.json",
    "https://raw.githubusercontent.com/shichuanenhui/TvBox/main/jav.json",
]

def fetch_json(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        return r.json()
    except:
        return None

def clean_site(site):
    """优化站点配置，减少 jar 加载失败"""
    if not isinstance(site, dict):
        return None
    
    api = site.get("api", "")
    name = site.get("name", "未知")
    
    # 添加常用兼容字段
    site.setdefault("searchable", 1)
    site.setdefault("quickSearch", 1)
    site.setdefault("filterable", 1)
    site.setdefault("playerType", 1)   # 1 = ijkplayer，比较稳定
    
    # 部分站点需要 type 调整
    if "api.php/provide/vod" in api:
        site["type"] = 0   # 普通点播
    
    return site

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    vod_sites = []
    
    print(f"开始抓取优化 - {timestamp}")

    for url in VOD_SOURCES:
        print(f"抓取: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data.get("sites", []):
                cleaned = clean_site(site)
                if cleaned and cleaned.get("api"):
                    vod_sites.append(cleaned)
    
    # 直播分组
    live_groups = [
        {"name": "亚洲成人直播", "type": 1, "url": "https://live.adultiptv.net/asian.m3u8"},
        {"name": "成人直播合集", "type": 1, "url": "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u"},
        {"name": "Live Cams", "type": 1, "url": "https://live.adultiptv.net/livecams.m3u8"}
    ]

    output = {
        "name": "我的亚洲性学接口（稳定优化版）",
        "update_time": timestamp,
        "vod_count": len(vod_sites),
        "live_count": len(live_groups),
        "sites": vod_sites,
        "lives": live_groups
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！点播站点: {len(vod_sites)} 个 | 直播: {len(live_groups)} 个")

if __name__ == "__main__":
    main()
