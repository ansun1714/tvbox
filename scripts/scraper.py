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
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return None

def test_site(site):
    """真实测试：访问 api，看是否有有效数据"""
    api = site.get("api")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    
    try:
        time.sleep(0.8)  # 避免请求太快被封
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(api, headers=headers, timeout=8)
        
        if r.status_code != 200:
            return False
            
        content = r.text.lower()
        # 有以下关键词说明有数据
        if any(k in content for k in ["class", "vod", "list", "rss", "video", "movie", "xml"]):
            return True
    except:
        pass
    return False

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    valid_sites = []
    
    print(f"开始自动抓取 + 真实测试 - {timestamp}")
    
    for source_url in VOD_SOURCES:
        print(f"抓取主配置: {source_url}")
        data = fetch_json(source_url)
        if data and isinstance(data, dict) and "sites" in data:
            sites = data["sites"]
            print(f"  发现 {len(sites)} 个站点，开始测试...")
            
            for i, site in enumerate(sites):
                name = site.get("name", "未知")
                print(f"  测试 [{i+1}/{len(sites)}] {name}")
                
                if test_site(site):
                    # 添加兼容字段
                    site.setdefault("searchable", 1)
                    site.setdefault("quickSearch", 1)
                    site.setdefault("filterable", 1)
                    site.setdefault("playerType", 1)
                    valid_sites.append(site)
                    print(f"    ✓ 保留: {name}")
                else:
                    print(f"    ✗ 丢弃: {name}")
    
    # 直播
    live_groups = [
        {"name": "亚洲成人直播", "type": 1, "url": "https://live.adultiptv.net/asian.m3u8"},
        {"name": "成人直播合集", "type": 1, "url": "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u"},
        {"name": "Live Cams", "type": 1, "url": "https://live.adultiptv.net/livecams.m3u8"}
    ]

    output = {
        "name": "亚洲性学接口（真实测试版）",
        "update_time": timestamp,
        "vod_count": len(valid_sites),
        "live_count": len(live_groups),
        "sites": valid_sites,
        "lives": live_groups
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试完成！最终保留 {len(valid_sites)} 个可用点播站点")

if __name__ == "__main__":
    main()
