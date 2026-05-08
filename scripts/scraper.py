import requests
import json
from datetime import datetime
import time
import re

# ==================== 点播源（增加到10个左右） ====================
VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
    "https://raw.githubusercontent.com/Dong-learn9/TVBox-zyjk/main/18.json",
    "https://raw.githubusercontent.com/shichuanenhui/TvBox/main/jav.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/18.json",
    "https://raw.githubusercontent.com/qirenzhidao/tvbox18/main/adult.json",
    "https://raw.githubusercontent.com/cliya/TVBox/main/18.json",
    "https://raw.githubusercontent.com/xiongjian83/TvBox/main/18CR.json",
    "https://gitlab.com/dokiss1/tvbox/-/raw/master/doki-18+.json",
]

def fetch_json(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return None

def test_vod_site(site):
    """严格测试，超时直接丢弃"""
    api = site.get("api")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    try:
        time.sleep(0.8)
        r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        if r.status_code != 200:
            return False
        content = r.text.lower()
        return any(k in content for k in ["class", "vod", "list", "rss", "xml", "video"])
    except:
        return False

# ==================== 直播解析函数 ====================
def parse_m3u(content, max_channels=40):
    channels = []
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            name_match = re.search(r',(.+)$', line)
            name = name_match.group(1).strip() if name_match else "未知频道"
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
    
    # ====================== 点播 ======================
    vod_sites = []
    for url in VOD_SOURCES:
        print(f"抓取点播源: {url}")
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

    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump({
            "name": "亚洲性学点播接口",
            "update_time": timestamp,
            "vod_count": len(final_vod),
            "sites": final_vod
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ 点播完成！保留 {len(final_vod)} 个有效站点")

    # ====================== 直播（30+来源，亚洲重点） ======================
    m3u_content = "#EXTM3U\n#EXT-X-VERSION:3\n\n"

    live_sources = [
        ("亚洲成人直播", "https://live.adultiptv.net/asian.m3u8"),
        ("Live Cams 全频道", "https://live.adultiptv.net/livecams.m3u8"),
        ("中国成人直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/xxx.m3u8"),
        ("台湾直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/TaiWan.m3u8"),
        ("香港澳门", "https://github.com/hujingguang/ChinaIPTV/raw/main/HongKong.m3u8"),
        ("韩国直播", "https://github.com/hujingguang/ChinaIPTV/raw/main/southKorea.m3u8"),
        ("日本直播", "https://raw.githubusercontent.com/luongz/iptv-jp/main/jp.m3u"),
        # 更多成人分类
        ("Anal", "https://cdn.adultiptv.net/anal.m3u8"),
        ("MILF", "https://cdn.adultiptv.net/milf.m3u8"),
        ("Teen", "https://cdn.adultiptv.net/teen.m3u8"),
        ("Lesbian", "https://cdn.adultiptv.net/lesbian.m3u8"),
        ("Fetish", "https://cdn.adultiptv.net/fetish.m3u8"),
        ("Pornstar", "https://cdn.adultiptv.net/pornstar.m3u8"),
        ("Big Ass", "https://cdn.adultiptv.net/bigass.m3u8"),
        ("Gay", "https://live.adultiptv.net/gay.m3u8"),
    ]

    for name, url in live_sources:
        print(f"处理直播: {name} - {url}")
        content = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text if "http" in url else None
        if content and "#EXTINF" in content:
            channels = parse_m3u(content, max_channels=35)
            for ch_name, ch_url in channels:
                m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{ch_name}\n{ch_url}\n'
        else:
            m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{name}\n{url}\n'

    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ 直播生成完成！共处理 {len(live_sources)} 个来源")

if __name__ == "__main__":
    main()
