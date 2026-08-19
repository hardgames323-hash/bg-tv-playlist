import re
import time
import requests

CHANNELS = {
    # National
    "bTV HD": ("National", "https://www.seirsanduk.online/btv"),
    "NOVA TV HD": ("National", "https://www.seirsanduk.online/nova"),
    "BNT 1 HD": ("National", "https://www.seirsanduk.online/bnt-1-hd"),
    "BNT 2": ("National", "https://www.seirsanduk.online/bnt-2"),
    "BNT 3 HD": ("National", "https://www.seirsanduk.online/bnt-3-hd"),
    "Bulgaria ON AIR": ("National", "https://www.seirsanduk.online/bulgaria-on-air"),
    # Sports
    "Diema Sport HD": ("Sports", "https://www.seirsanduk.online/diema-sport-hd"),
    "Diema Sport 2 HD": ("Sports", "https://www.seirsanduk.online/diema-sport-2-hd"),
    "Diema Sport 3 HD": ("Sports", "https://www.seirsanduk.online/diema-sport-3-hd"),
    "Max Sport 1 HD": ("Sports", "https://www.seirsanduk.online/max-sport-1-hd"),
    "Max Sport 2 HD": ("Sports", "https://www.seirsanduk.online/max-sport-2-hd"),
    "Max Sport 3 HD": ("Sports", "https://www.seirsanduk.online/max-sport-3-hd"),
    "Max Sport 4 HD": ("Sports", "https://www.seirsanduk.online/max-sport-4-hd"),
    "Nova Sport HD": ("Sports", "https://www.seirsanduk.online/nova-sport-hd"),
    "Ring BG HD": ("Sports", "https://www.seirsanduk.online/ring-bg-hd"),
    "Eurosport 1 HD": ("Sports", "https://www.seirsanduk.online/eurosport-1-hd"),
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.seirsanduk.online/"
}

entries = []
for name, (group, page_url) in CHANNELS.items():
    try:
        res = requests.get(page_url, headers=headers, timeout=10)
        clean_text = res.text.replace('\\/', '/')
        match = re.search(r'(https?://[^"\'\s<>]+\.m3u8\?e=\d+&hash=[^"\'\s<>]+)', clean_text)
        if match:
            entries.append(
                f'#EXTINF:-1 tvg-name="{name}" group-title="{group}", {name}\n'
                f'{match.group(1)}|Referer=https://www.seirsanduk.online/&User-Agent=Mozilla/5.0'
            )
            print(f"OK: {name}")
    except Exception as e:
        print(f"Fail: {name} -> {e}")
    time.sleep(1)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n" + "\n\n".join(entries))
