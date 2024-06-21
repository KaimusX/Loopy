import PySimpleGUI as sg
import pygame
from moviepy.editor import VideoFileClip        #INSTALL USING --> pip install moviepy
import os
import re #import using -> pip install regex
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

# Define the layout of the GUI
layout = [
    [sg.Text('LOOPY Video Player')],
    [sg.Image(filename='', key='-IMAGE-')],
    [sg.Button('Start Playlist'), sg.Button('Unpause'), sg.Button('Pause'), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Video Player', layout, finalize=True)

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


# Function to play a video from the playlist
def play_video(audio_file, video_file):
    
    video_path = find_video_file(video_file)
    audio_path = find_audio_file(audio_file)
    
    if video_file is not None and audio_file is not None:
        video = VideoFileClip(video_path)
        pygame.mixer.music.load(audio_path)
        
        
        # Update the screen size
        width, height = video.size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('LOOPY Video Player')
        
        playing = False
        
        def update_frame():
            audio_pos = pygame.mixer.music.get_pos() / 1000.0
            frame = video.get_frame(audio_pos)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame, (0, 0))
            pygame.display.flip()
            return frame
        
        # Main loop
        while True:
            event, values = window.read(timeout=int(1000/video.fps))
            
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            elif event == 'Start Playlist':
                pygame.mixer.music.play()
                playing = True
            elif event == 'Pause':
                pygame.mixer.music.pause()
                playing = False
            elif event == 'Unpause':
                pygame.mixer.music.unpause()
                playing = True
        
            if playing:
                frame = update_frame()
                #imgbytes = pygame.image.tostring(frame, 'RGB')
                #window['-IMAGE-'].update(data=imgbytes)
        
        # Clean up
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.quit()
        video.close()
    else:
        print('Video or audio file not found for MD5 hash:', video_md5, audio_md5)

# Authors: Shari Hoch and Luis Franco
# Timestamp: 06/21/2024 1:26PM
# Exp: Helper function for create_playlist, validates user input.
def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    return re.match(youtube_regex, url)

# Authors: Shari Hoch and Luis Franco
# Timestamp: 06/21/2024 1:26PM
# Exp: When called, creates a pop out gui that allows user to input youtube links or file paths. please see bottom for data.
def create_playlist():
    video_entries = []

    layout = [
        [sg.Text('LOOPY Playlist Creator')],
        [sg.Text('Playlist Name:'), sg.InputText(key='-PLAYLIST_NAME-')],
        [sg.Text('Select Video Source (max 10 entries):')]
    ]

    # Add input fields for up to 10 videos
    for i in range(10):
        layout.extend([
            [sg.Text(f'Video {i+1} Source:'), 
             sg.Radio('YouTube URL', f'RADIO{i}', key=f'-YOUTUBE-{i}', default=True), 
             sg.InputText(key=f'-YOUTUBE_URL-{i}', size=(30, 1)), 
             sg.Radio('Local File Path', f'RADIO{i}', key=f'-LOCAL-{i}'), 
             sg.InputText(key=f'-LOCAL_PATH-{i}', size=(30, 1)), sg.FileBrowse()],
        ])

    layout.append([sg.Button('Submit'), sg.Button('Cancel')])

    window = sg.Window('Video Playlist Creator', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break
        elif event == 'Submit':
            playlist_name = values['-PLAYLIST_NAME-']
            video_entries = []
            error = False
            for i in range(10):
                if values[f'-YOUTUBE-{i}'] and values[f'-YOUTUBE_URL-{i}']:
                    url = values[f'-YOUTUBE_URL-{i}']
                    if is_valid_youtube_url(url):
                        video_entries.append(('YouTube', url))
                    else:
                        sg.popup_error(f'Invalid YouTube URL for Video {i+1}: {url}')
                        error = True
                        break
                elif values[f'-LOCAL-{i}'] and values[f'-LOCAL_PATH-{i}']:
                    path = values[f'-LOCAL_PATH-{i}']
                    video_entries.append(('Local', path))

            if not error:
                # Handle the collected data here

                print()
                print(f'Playlist Name: {playlist_name}')
                print()
                print('Video Entries:')
                print()
                for entry in video_entries:
                    print(entry)
                break

    window.close()

def play_playlist(playlist_name):
    # Find the playlist index based on the playlist name
    for playlist_row in playlist_3d:
        if playlist_row[0][0] == playlist_name:
            print('Playing playlist:', playlist_row[0][0])
            # Play each video in the selected playlist
            for i in range(1, 11):
                video_md5 = playlist_row[0][i + 2]
                audio_md5 = playlist_row[0][i + 12]
                print(audio_md5, video_md5)
                if video_md5 and audio_md5:
                    play_video(audio_md5, video_md5)
                else:
                    break
    

if __name__ == '__main__':
    play_playlist('John')
