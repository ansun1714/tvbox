import requests
import json
from datetime import datetime
import time
import re

# ==================== 精选可靠点播源（亚洲/JAV重点） ====================
VOD_SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",   # 美少女、香奶儿等
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/shichuanenhui/TvBox/main/jav.json",        # JAV专源
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
    "https://raw.githubusercontent.com/Dong-learn9/TVBox-zyjk/main/18.json",
]

def fetch_json(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return None

def test_vod_site(site):
    """严格测试，只保留能正常返回数据的"""
    api = site.get("api")
    if not api or not isinstance(api, str) or not api.startswith("http"):
        return False
    try:
        time.sleep(1.0)  # 增加间隔
        r = requests.get(api, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        if r.status_code != 200:
            return False
        content = r.text.lower()
        # 必须有明显数据特征
        if any(k in content for k in ["class", "vod", "list", "rss", "xml", "video", "movie"]):
            return True
    except:
        return False
    return False

# ==================== 直播解析 ====================
def parse_m3u(content, max_channels=40):
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
    
    # ====================== 点播 ======================
    vod_sites = []
    for url in VOD_SOURCES:
        print(f"抓取: {url}")
        data = fetch_json(url)
        if data and isinstance(data, dict) and "sites" in data:
            for site in data.get("sites", []):
                name = site.get("name", "")
                if any(k in name for k in ["美少女", "香奶儿", "淫水机", "91md", "老鸭", "JAV", "麻豆", "亚洲成人"]):
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
            "name": "亚洲性学点播接口（精选可靠版）",
            "update_time": timestamp,
            "vod_count": len(final_vod),
            "sites": final_vod
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ 点播完成！保留 {len(final_vod)} 个可靠站点")

    # ====================== 直播（亚洲成人重点） ======================
    m3u_content = "#EXTM3U\n#EXT-X-VERSION:3\n\n"

    live_sources = [
        ("亚洲成人直播", "https://live.adultiptv.net/asian.m3u8"),
        ("Live Cams", "https://live.adultiptv.net/livecams.m3u8"),
        ("中国成人", "https://github.com/hujingguang/ChinaIPTV/raw/main/xxx.m3u8"),
        ("台湾香港", "https://github.com/hujingguang/ChinaIPTV/raw/main/TaiWan.m3u8"),
    ]

    for name, url in live_sources:
        print(f"处理直播: {name}")
        try:
            content = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
            if "#EXTINF" in content:
                channels = parse_m3u(content, max_channels=35)
                for ch_name, ch_url in channels:
                    if any(k in ch_name.lower() for k in ["adult", "sex", "porn", "cam", "直播", "av", "jap", "korea", "asia"]):
                        m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{ch_name}\n{ch_url}\n'
            else:
                m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{name}\n{url}\n'
        except:
            m3u_content += f'#EXTINF:-1 group-title="亚洲成人直播",{name}\n{url}\n'

    with open("live.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print("✅ 直播生成完成（亚洲成人重点）")

if __name__ == "__main__":
    main()
