import requests
import json
from datetime import datetime

SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
]

def fetch_json(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"抓取失败: {url} - {str(e)[:100]}")
        return None

def main():
    all_sites = []
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    print(f"开始抓取 - {timestamp}")
    
    for url in SOURCES:
        print(f"正在处理: {url}")
        data = fetch_json(url)
        if data:
            # 尝试提取 sites
            if isinstance(data, dict):
                if "sites" in data:
                    all_sites.extend(data["sites"])
                else:
                    # 如果没有sites，包装成一个站点
                    all_sites.append({
                        "key": url.split("/")[-1].replace(".json", ""),
                        "name": url.split("/")[-1],
                        "type": 0,
                        "api": url,
                        "searchable": 1,
                        "quickSearch": 1,
                        "filterable": 1
                    })
    
    output = {
        "name": "我的亚洲私人TVBox接口",
        "update_time": timestamp,
        "total": len(all_sites),
        "sites": all_sites
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新完成！共 {len(all_sites)} 个站点")

if __name__ == "__main__":
    main()
