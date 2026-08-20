Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\PATH\TO\YOUR\bg-tv-playlist" 
WshShell.Run "python scraper.py", 0, False