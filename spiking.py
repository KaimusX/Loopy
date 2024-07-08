import time
from cvplayerlocal import VideoPlayer

player = VideoPlayer("Video_Media/Audio Video Sync Test.mp4")

while True:
    if player.state != 'eof':
        time.sleep(0)
    
    if player.state == 'eof':
         player.seek(0, relative = False)
         player.get_frame() 
         #player.revive_player()
