import os
from playwright.sync_api import sync_playwright

CHANNELS = {
    "bTV HD": "https://www.seirsanduk.online/?id=hd-btv-hd&pass=&hash=",
    "NOVA TV HD": "https://www.seirsanduk.online/?id=hd-nova-tv-hd&pass=&hash=",
    "BNT 1 HD": "https://www.seirsanduk.online/?id=hd-bnt-1-hd&pass=&hash=",
    "BNT 2": "https://www.seirsanduk.online/?id=bnt-2&pass=&hash=",
    "BNT 3 HD": "https://www.seirsanduk.online/?id=hd-bnt-3-hd&pass=&hash=",
    "BNT 4": "https://www.seirsanduk.online/?player=12&id=bnt-4&pass=",
    "Bulgaria ON AIR": "https://www.seirsanduk.online/?id=bulgaria-on-air&pass=&hash=",
    "Kanal 3": "https://www.seirsanduk.online/?id=kanal-3&pass=&hash=",
    "Evrokom": "https://www.seirsanduk.online/?id=evrokom&pass=&hash=",
    "Nova News HD": "https://www.seirsanduk.online/?id=hd-nova-news-hd&pass=&hash=",
    "Euronews Bulgaria HD": "https://www.seirsanduk.online/?id=hd-euronews-bulgaria-hd&pass=&hash=",
    "7/8 TV HD": "https://www.seirsanduk.online/?id=hd-78-tv-hd&pass=&hash=",
    "SKAT": "https://www.seirsanduk.online/?id=skat&pass=&hash=",
    "VTK": "https://www.seirsanduk.online/?id=vtk&pass=&hash=",
    "Diema HD": "https://www.seirsanduk.online/?id=hd-diema-hd&pass=&hash=",
    "Diema Sport HD": "https://www.seirsanduk.online/?id=hd-diema-sport-hd&pass=&hash=",
    "Diema Sport 2 HD": "https://www.seirsanduk.online/?id=hd-diema-sport-2-hd&pass=&hash=",
    "Diema Sport 3 HD": "https://www.seirsanduk.online/?id=hd-diema-sport-3-hd&pass=&hash=",
    "Max Sport 1 HD": "https://www.seirsanduk.online/?id=hd-max-sport-1-hd&pass=&hash=",
    "Max Sport 2 HD": "https://www.seirsanduk.online/?id=hd-max-sport-2-hd&pass=&hash=",
    "Max Sport 3 HD": "https://www.seirsanduk.online/?id=hd-max-sport-3-hd&pass=&hash=",
    "Max Sport 4 HD": "https://www.seirsanduk.online/?id=hd-max-sport-4-hd&pass=&hash=",
    "Nova Sport HD": "https://www.seirsanduk.online/?id=hd-nova-sport-hd&pass=&hash=",
    "Ring BG HD": "https://www.seirsanduk.online/?id=hd-ring-bg-hd&pass=&hash=",
    "Eurosport 1 HD": "https://www.seirsanduk.online/?id=hd-eurosport-1-hd&pass=&hash=",
    "Eurosport 2 HD": "https://www.seirsanduk.online/?id=hd-eurosport-2-hd&pass=&hash=",
    "bTV Action HD": "https://www.seirsanduk.online/?id=hd-btv-action-hd&pass=&hash=",
    "bTV Cinema": "https://www.seirsanduk.online/?id=btv-cinema&pass=&hash=",
    "bTV Comedy HD": "https://www.seirsanduk.online/?id=hd-btv-comedy-hd&pass=&hash=",
    "bTV Story": "https://www.seirsanduk.online/?id=btv-story&pass=&hash=",
    "Kino Nova HD": "https://www.seirsanduk.online/?id=hd-kino-nova-hd&pass=&hash=",
    "Diema Family HD": "https://www.seirsanduk.online/?id=hd-diema-family-hd&pass=&hash=",
    "STAR Channel HD": "https://www.seirsanduk.online/?id=hd-star-channel-hd&pass=&hash=",
    "STAR Crime HD": "https://www.seirsanduk.online/?id=hd-star-crime-hd&pass=&hash=",
    "STAR Life HD": "https://www.seirsanduk.online/?id=hd-star-life-hd&pass=&hash=",
    "Epic Drama HD": "https://www.seirsanduk.online/?player=11&id=hd-epic-drama-hd&pass=",
    "Max One HD": "https://www.seirsanduk.online/?id=hd-max-one-hd&pass=&hash=",
    "AXN": "https://www.seirsanduk.online/?id=axn&pass=&hash=",
    "AXN Black": "https://www.seirsanduk.online/?id=axn-black&pass=&hash=",
    "AXN White": "https://www.seirsanduk.online/?id=axn-white&pass=&hash=",
    "Discovery Channel HD": "https://www.seirsanduk.online/?id=hd-discovery-channel-hd&pass=&hash=",
    "Nat Geo HD": "https://www.seirsanduk.online/?id=hd-nat-geo-hd&pass=&hash=",
    "Nat Geo Wild HD": "https://www.seirsanduk.online/?id=hd-nat-geo-wild-hd&pass=&hash=",
    "ID Xtra HD": "https://www.seirsanduk.online/?id=hd-id-xtra-hd&pass=&hash=",
    "Viasat Explore HD": "https://www.seirsanduk.online/?id=hd-viasat-explore-hd&pass=&hash=",
    "Travel Channel HD": "https://www.seirsanduk.online/?id=hd-travel-channel-hd&pass=&hash=",
    "Travel TV": "https://www.seirsanduk.online/?id=travel-tv&pass=&hash=",
    "24 Kitchen HD": "https://www.seirsanduk.online/?id=hd-24-kitchen-hd&pass=&hash=",
    "Food Network HD": "https://www.seirsanduk.online/?id=hd-food-network-hd&pass=&hash=",
    "TLC": "https://www.seirsanduk.online/?id=tlc&pass=&hash=",
    "Code Fashion TV HD": "https://www.seirsanduk.online/?id=hd-code-fashion-tv-hd&pass=&hash=",
    "City TV": "https://www.seirsanduk.online/?id=city-tv&pass=&hash=",
    "The Voice": "https://www.seirsanduk.online/?id=the-voice&pass=&hash=",
    "Planeta HD": "https://www.seirsanduk.online/?id=hd-planeta-hd&pass=&hash=",
    "DSTV": "https://www.seirsanduk.online/?id=dstv&pass=&hash=",
    "Bloomberg TV": "https://www.seirsanduk.online/?id=bloomberg-tv&pass=&hash=",
}

def update_and_push():
    entries = []
    print(f"Starting mobile playlist update for {len(CHANNELS)} channels...")
    
    with sync_playwright() as p:
        # Added autoplay bypass flag and anti-crash flags
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox", 
                "--disable-dev-shm-usage",
                "--autoplay-policy=no-user-gesture-required" 
            ]
        )
        
        # Forced 1080p desktop viewport so the layout doesn't break
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        for name, url in CHANNELS.items():
            page = context.new_page()
            stream_url = None

            def capture(response):
                nonlocal stream_url
                if ".m3u8" in response.url and not stream_url:
                    stream_url = response.url

            page.on("response", capture)
            
            try:
                # Extended timeouts for mobile connections
                page.goto(url, wait_until="domcontentloaded", timeout=35000)
                page.wait_for_timeout(4000)
                
                # Triple-click at the exact center of the 1080p screen to bypass ads
                for _ in range(3):
                    page.mouse.click(1920 / 2, 1080 / 2)
                    page.wait_for_timeout(1000)
                    
                page.wait_for_timeout(8000) 
            except Exception as e:
                # This will print exactly why it crashed if it fails again
                print(f"  ✗ {name} (Error: {type(e).__name__} - {e})")

            if stream_url:
                entries.append(
                    f'#EXTINF:-1 tvg-name="{name}", {name}\n'
                    f'{stream_url}|Referer=https://www.seirsanduk.online/'
                )
                print(f"  ✓ {name}")
            else:
                if not stream_url:
                    print(f"  ✗ {name} (Failed to capture .m3u8 stream)")
                
            page.close()
            
        browser.close()

    if entries:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n" + "\n\n".join(entries))

        print("\nUploading to GitHub from Phone...")
        os.system('git config user.name "TV Server Phone"')
        os.system('git config user.email "tvphone@server.local"')
        os.system("git add playlist.m3u")
        os.system('git commit -m "Auto-update tokens from Phone"')
        os.system("git push --force")
        print("Done! The playlist is live.")
    else:
        print("\nNo links captured. Exiting without uploading.")

if __name__ == "__main__":
    update_and_push()