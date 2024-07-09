import time
from cvplayerlocal import VideoPlayer     
import mergeVid as mv

def videoPlayer(playlistName):
    merge = mv.mergeVid()
    #make this selectable instead of a set playlist name later
    merge.build_playlist(playlistName)
    player = VideoPlayer("my_concatenation.mp4")

    while True:
        if player.state != 'eof':
            time.sleep(0)
    
        if player.state == 'eof':
            player.seek(0, relative = False)
            player.get_frame() 

if __name__ == "__main__":
    videoPlayer("Testing Playlist")
