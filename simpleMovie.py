import PySimpleGUI as sg
import pygame
from moviepy.editor import *        #INSTALL USING --> pip install moviepy
import os
import csv
import hashlib
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Initialize sys and os
if not sys.stdout:
    sys.stdout = open(os.devnull, 'w')
if not sys.stderr:
    sys.stderr = open(os.devnull, 'w')

#reading the playlist and running the correct audio. By Jonah Dalton on 6/21/2024
# Read the playlist from the playlist.csv file
cwd = os.getcwd()
playlist_file = os.path.join(cwd, 'playlists.csv')
playlist = []
with open(playlist_file, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Extract the header row
    for row in reader:
        playlist.append(row)

# Convert the playlist into a 3D array with proper columns and rows, excluding the header
playlist_3d = [[row] for row in playlist]  # Wrap each data row in its own list

# Function to find the video file based on MD5 hash
def find_video_file(md5_hash):
    video_media_path = os.path.join(cwd, 'Video_Media')
    for root, dirs, files in os.walk(video_media_path):
        for file in files:
            if hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest() == md5_hash:
                return os.path.join(root, file)
    return None

# Function to find the audio file based on MD5 hash
def find_audio_file(md5_hash):
    audio_media_path = os.path.join(cwd, 'Audio_Media')
    for root, dirs, files in os.walk(audio_media_path):
        for file in files:
            if hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest() == md5_hash:
                return os.path.join(root, file)
    return None

font = pygame.font.Font('freesansbold.ttf', 18)
class Button():
    def __init__(self, scrn, text, x_pos, y_pos, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.draw(scrn)
    
    def draw(self, scrn):
        button_text = font.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150,25))
   
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        scrn.blit(button_text, (self.x_pos+3, self.y_pos+3))
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150,25))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False
    
def update_frame(video, scr):
    audio_pos = pygame.mixer.music.get_pos() / 1000.0
    frame = video.get_frame(audio_pos)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    scr.blit(frame, (0, 0))
    pygame.display.flip()
    return frame

# Function to play a video from the playlist
def play_video(audio_file, video_file):
    
    video_path = find_video_file(video_file)
    audio_path = find_audio_file(audio_file)
    
    if video_file is not None and audio_file is not None:
        video = VideoFileClip(video_path)
        pygame.mixer.music.load(audio_path)
        
        
        # Update the screen size
        width, height = video.size
        scrn = pygame.display.set_mode([width+200, height+200])
        pygame.display.set_caption('LOOPY Video Player')
        
        playing = False
        run = True
        new_press = True
        
        # Main loop
        while run:
            startLoop = Button(scrn, 'Start Loop', 10, 400, True)
            playB = Button(scrn, 'Play', 10, 440, True)
            pauseB = Button(scrn, 'Pause', 10, 480, True)
            stopLoop = Button(scrn, 'Stop Loop', 10, 520, True)

            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
            
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if startLoop.check_click():
                pygame.mixer.music.play()
                playing = True
            if playB.check_click():
                pygame.mixer.music.unpause()
                playing = True
            if pauseB.check_click():
                pygame.mixer.music.pause()
                playing = False
            if stopLoop.check_click():
                pygame.mixer.music.stop()
            
            pygame.display.flip()
            if playing:
                frame = update_frame(video, scrn)
        
        # Clean up
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.quit()
        video.close()
    else:
        print('Video or audio file not found for MD5 hash:', video_md5, audio_md5)



def play_playlist(playlist_name):
    # Find the playlist index based on the playlist name
    for playlist_row in playlist_3d:
        if playlist_row[0][0] == playlist_name:
            print('Playing playlist:', playlist_row[0][0])
            # Play each video in the selected playlist
            video_md5 = playlist_row[0][3]
            audio_md5 = playlist_row[0][13]
            play_video(audio_md5, video_md5)
    

if __name__ == '__main__':
    play_playlist('John')
