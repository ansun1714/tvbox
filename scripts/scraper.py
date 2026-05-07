import requests
import json
from datetime import datetime
import time

# ==================== 点播源 ====================
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

def test_vod_site(site):
    api = site.get("api")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    try:
        time.sleep(0.5)
        r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        if r.status_code == 200:
            content = r.text.lower()
            return any(k in content for k in ["class", "vod", "list", "rss", "xml"])
    except:
        pass
    return True

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ====================== 点播部分 ======================
    vod_sites = []
    for url in VOD_SOURCES:
        print(f"抓取点播: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data.get("sites", []):
                if test_vod_site(site):
                    site.setdefault("searchable", 1)
                    site.setdefault("quickSearch", 1)
                    site.setdefault("filterable", 1)
                    site.setdefault("playerType", 1)
                    vod_sites.append(site)
    
    # 去重
    seen = set()
    final_vod = []
    for s in vod_sites:
        key = (s.get("name"), s.get("api"))
        if key not in seen:
            seen.add(key)
            final_vod.append(s)

    vod_output = {
        "name": "亚洲性学点播接口",
        "update_time": timestamp,
        "vod_count": len(final_vod),
        "sites": final_vod
    }

    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(vod_output, f, ensure_ascii=False, indent=2)
    print(f"✅ 点播生成完成！共 {len(final_vod)} 个站点")

    # ====================== 直播 M3U（大幅增加频道） ======================
    m3u_content = "#EXTM3U\n#EXT-X-VERSION:3\n\n"

    channels = [
        ("亚洲成人直播", "https://live.adultiptv.net/asian.m3u8"),
        ("Live Cams 全频道", "https://live.adultiptv.net/livecams.m3u8"),
        ("Anal 直播", "https://cdn.adultiptv.net/anal.m3u8"),
        ("Big Ass 直播", "https://cdn.adultiptv.net/bigass.m3u8"),
        ("Big Dick 直播", "https://cdn.adultiptv.net/bigdick.m3u8"),
        ("MILF 直播", "https://cdn.adultiptv.net/milf.m3u8"),
        ("Lesbian 直播", "https://cdn.adultiptv.net/lesbian.m3u8"),
        ("Teen 直播", "https://cdn.adultiptv.net/teen.m3u8"),
        ("成人直播合集", "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u"),
        ("中国成人直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/xxx.m3u8"),
    ]

    for name, url in channels:
        m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{name}\n{url}\n'

    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ 直播 M3U 生成完成！共 {len(channels)} 个直播源")

if __name__ == "__main__":
    main()
