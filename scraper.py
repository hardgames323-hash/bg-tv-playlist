import time
from playwright.sync_api import sync_playwright

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

entries = []

def run():
    with sync_playwright() as p:
        # Launch an invisible Chromium browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        for name, (group, url) in CHANNELS.items():
            page = context.new_page()
            stream_url = None
            
            # This acts exactly like looking at the F12 Network tab
            def handle_response(response):
                nonlocal stream_url
                if ".m3u8" in response.url and not stream_url:
                    stream_url = response.url

            page.on("response", handle_response)
            
            try:
                # Go to the channel page and wait for the DOM to load
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                # Give the JavaScript player 4 seconds to generate the token and request the stream
                page.wait_for_timeout(4000) 
            except Exception as e:
                print(f"Warning on {name}: {e}")
                
            if stream_url:
                print(f"OK: {name}")
                entries.append(
                    f'#EXTINF:-1 tvg-name="{name}" group-title="{group}", {name}\n'
                    f'{stream_url}|Referer=https://www.seirsanduk.online/&User-Agent=Mozilla/5.0'
                )
            else:
                print(f"Fail: {name} (Could not intercept Javascript stream link)")
                
            page.close()
            
        browser.close()

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n" + "\n\n".join(entries))

if __name__ == "__main__":
    run()
