import requests
import json
from datetime import datetime
import time

# 点播源 (VOD)
VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
]

# 直播源 (Live) - 新增亚洲/成人直播
LIVE_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u",  # wwb521 直播
    "https://live.adultiptv.net/asian.m3u8",           # Asian cams
    "https://live.adultiptv.net/livecams.m3u8",        # Live Cams
    "https://raw.githubusercontent.com/hujingguang/ChinaIPTV/main/xxx.m3u8",  # 成人直播合集
]

def fetch_json(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        if url.endswith('.m3u') or url.endswith('.m3u8'):
            return {"type": "m3u", "content": r.text}
        return r.json()
    except:
        return None

def test_vod_site(site):
    """测试点播站点"""
    api = site.get("api")
    if not api:
        return False
    try:
        time.sleep(0.3)
        r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        if r.status_code != 200:
            return False
        data = r.json()
        return bool(data.get("class") or data.get("list") or "vod" in str(data).lower())
    except:
        return False

def test_live_url(url):
    """测试直播链接"""
    if not url or not isinstance(url, str):
        return False
    try:
        time.sleep(0.3)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6, stream=True)
        return r.status_code == 200 and len(r.content) > 1000
    except:
        return False

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    vod_sites = []
    live_sites = []
    
    print(f"开始抓取并测试 - {timestamp}")

    # 处理点播
    for url in VOD_SOURCES:
        print(f"抓取点播: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data["sites"]:
                if test_vod_site(site):
                    vod_sites.append(site)
    
    # 处理直播
    for url in LIVE_SOURCES:
        print(f"抓取直播: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "type" == "m3u":
            # 简单解析 m3u 添加为直播组
            live_sites.append({
                "key": "live_adult",
                "name": "亚洲成人直播",
                "type": 1,          # 1 表示直播
                "url": url,
                "playerType": 1
            })
        elif isinstance(data, dict):  # 其他 JSON 直播
            live_sites.append({
                "key": "live_group",
                "name": "成人直播合集",
                "type": 1,
                "url": url
            })
    
    # 输出最终结构（TVBox 支持多分组）
    output = {
        "name": "我的亚洲性学接口（已测试）",
        "update_time": timestamp,
        "vod_count": len(vod_sites),
        "live_count": len(live_sites),
        "sites": vod_sites,           # 点播站点
        "lives": [                    # 直播分组
            {
                "name": "亚洲成人直播",
                "type": 1,
                "url": "https://live.adultiptv.net/asian.m3u8"   # 可扩展
            }
        ] + live_sites
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！点播: {len(vod_sites)} | 直播: {len(live_sites)}")

if __name__ == "__main__":
    main()
