import requests
import json
from datetime import datetime

# 要抓取的亚洲成人源列表（你可以继续添加更多）
SOURCES = [
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/video.json",
    "https://raw.githubusercontent.com/Nancy0308/TVbox-interface/main/tvbox-福利.json",
    "https://raw.githubusercontent.com/chinawiz/tvbox/main/adult-2.json",
    # 以后可以在这里继续添加其他JSON链接
]

def fetch_json(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"抓取失败: {url} - {e}")
        return None

def main():
    all_sites = []
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    print(f"开始每日抓取 - {timestamp}")
    
    for url in SOURCES:
        print(f"正在抓取: {url}")
        data = fetch_json(url)
        if data:
            if isinstance(data, dict) and "sites" in data:
                all_sites.extend(data.get("sites", []))
            elif isinstance(data, list):
                all_sites.extend(data)
            else:
                all_sites.append({"name": url.split("/")[-1], "url": url, "data": data})
    
    # 最终输出的私有接口文件
    output = {
        "name": "我的亚洲私人TVBox接口",
        "update_time": timestamp,
        "total_sources": len(all_sites),
        "sites": all_sites
    }
    
    with open("my-private-api.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"更新完成！共合并 {len(all_sites)} 个站点")

if __name__ == "__main__":
    main()
