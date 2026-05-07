import requests
import json
from datetime import datetime

def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 精选较稳定的亚洲成人站点
    vod_sites = [
        {"key": "msnii", "name": "美少女", "type": 0, "api": "https://www.msnii.com/api/xml.php", "searchable": 1, "quickSearch": 1, "filterable": 1, "playerType": 1},
        {"key": "xrbsp", "name": "淫水机", "type": 0, "api": "https://www.xrbsp.com/api/xml.php", "searchable": 1, "quickSearch": 1, "filterable": 1, "playerType": 1},
        {"key": "gdlsp", "name": "香奶儿", "type": 0, "api": "https://www.gdlsp.com/api/xml.php", "searchable": 1, "quickSearch": 1, "filterable": 1, "playerType": 1},
        {"key": "91md", "name": "91md", "type": 0, "api": "https://91md.me/api.php/provide/vod/from/mdm3u8/", "searchable": 1, "quickSearch": 1, "filterable": 1, "playerType": 1},
        {"key": "老鸭2", "name": "老鸭2", "type": 0, "api": "https://lbapi9.com/api.php/provide/vod/", "searchable": 1, "quickSearch": 1, "filterable": 1, "playerType": 1},
    ]
    
    live_groups = [
        {"name": "亚洲成人直播", "type": 1, "url": "https://live.adultiptv.net/asian.m3u8"},
        {"name": "成人直播合集", "type": 1, "url": "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u"},
        {"name": "Live Cams", "type": 1, "url": "https://live.adultiptv.net/livecams.m3u8"}
    ]

    output = {
        "name": "亚洲性学接口（精简稳定版）",
        "update_time": timestamp,
        "vod_count": len(vod_sites),
        "live_count": len(live_groups),
        "sites": vod_sites,
        "lives": live_groups
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 精简版生成完成！点播 {len(vod_sites)} 个 + 直播 {len(live_groups)} 个")

if __name__ == "__main__":
    main()
