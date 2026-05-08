import requests
import json
from datetime import datetime
import time
import re

# 点播源（保持原样）
VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
]

def fetch_text(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return r.text
    except:
        return None

def fetch_json(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return None

def test_vod_site(site):
    api = site.get("api")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    try:
        time.sleep(0.7)
        r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}, timeout=7)
        if r.status_code != 200:
            return False
        content = r.text.lower()
        return any(k in content for k in ["class", "vod", "list", "rss", "xml", "video"])
    except:
        return False

def parse_m3u(content, max_channels=50):
    channels = []
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            name_match = re.search(r',(.+)$', line)
            name = name_match.group(1).strip() if name_match else "未知"
            i += 1
            if i < len(lines):
                url = lines[i].strip()
                if url.startswith("http"):
                    channels.append((name, url))
                    if len(channels) >= max_channels:
                        break
        i += 1
    return channels

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 点播（严格测试）
    vod_sites = []
    for url in VOD_SOURCES:
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
    final_vod = [s for s in vod_sites if (s.get("name"), s.get("api")) not in seen and not seen.add((s.get("name"), s.get("api")))]

    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump({
            "name": "亚洲性学点播接口",
            "update_time": timestamp,
            "vod_count": len(final_vod),
            "sites": final_vod
        }, f, ensure_ascii=False, indent=2)

    # ====================== 亚洲直播（中日韩台港重点） ======================
    m3u_content = "#EXTM3U\n#EXT-X-VERSION:3\n\n"

    live_sources = [
        ("亚洲成人直播", "https://live.adultiptv.net/asian.m3u8"),
        ("Live Cams", "https://live.adultiptv.net/livecams.m3u8"),
        ("中国成人直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/xxx.m3u8"),
        ("日本成人/直播", "https://raw.githubusercontent.com/luongz/iptv-jp/main/jp.m3u"),   # 含部分 NSFW
        ("台湾/香港直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/TaiWan.m3u8"),
        ("韩国直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/southKorea.m3u8"),
    ]

    for name, url in live_sources:
        print(f"处理直播: {name}")
        content = fetch_text(url)
        if content:
            if "#EXTINF" in content:   # 合集文件
                channels = parse_m3u(content, max_channels=40)
                for ch_name, ch_url in channels:
                    m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{ch_name}\n{ch_url}\n'
            else:
                m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{name}\n{url}\n'

    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print("✅ 直播 M3U 生成完成（亚洲重点）")

if __name__ == "__main__":
    main()
