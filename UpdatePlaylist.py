from pytube import YouTube
import PySimpleGUI as sg
import pygame
import csv
import re
from pytube import YouTube
import hashlib
import pandas as pd
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set font for buttons (assuming you are using PySimpleGUI for buttons)
font = pygame.font.Font('freesansbold.ttf', 18)

def create_user_list(user):
    playlist_names = []
    
    with open('playlists.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['User'] == user:
                playlist_names.append(row['PlayList_Name'])
    return playlist_names

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    return re.match(youtube_regex, url)


# Function to create PySimpleGUI layout for playlists and buttons
def create_layout(playlist_names):
    
    playlist_names = create_user_list("User1")
    
    layout = [
        [sg.Text('Select Playlist to Manage:')],
        [sg.Combo(playlist_names, key='-PLAYLISTS-')],
    ]

    layout.extend([
        [sg.Text(f'Video {1} Source:'), 
        sg.Radio('YouTube URL', f'RADIO{0}', key=f'-YOUTUBE-{0}', default=True), 
        sg.InputText(key=f'-YOUTUBE_URL-{0}', size=(15, 1)), 
        sg.Radio('Local File Path', f'RADIO{0}', key=f'-LOCAL-{0}'), 
        sg.InputText(key=f'-LOCAL_PATH-{0}', size=(15, 1)), sg.FileBrowse()],
        ])
    layout.append([sg.Button('Add to Playlist'), sg.Button('Back To Home')])

    return layout

# Function to handle adding a song to a playlist
def add_video_to_playlist(playlist_name, video_title):
    #downloading the video
    try:
        # Create a YouTube object
        yt = YouTube(video_title)
         # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        # Download the video
        video_path = stream.download('Video_Media')
        print(f'Download completed: {yt.title}')
    except Exception as e:
        print(f'An error occurred: {e}')
    print(playlist_name, video_title)  
    
    #hash the video
    hash_md5 = hashlib.md5()
    with open(video_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return(hash_md5.hexdigest())
    
#add MD5 hash to the playlist
def update_playlist_videos(md5Hash):
    df = pd.read_csv('playlists.csv')
    video_columns = [f'Video{i}' for i in range(1, 11)]
        
    for index, row in df.iterrows():
        updated = False
        for column in video_columns:
            if pd.isna(row[column]):
                # Generate and store MD5 hash
                df.at[index, column] = md5Hash
                print(f'Added MD5 hash to {column} in playlist "{row["PlayList_Name"]}".')
                sg.popup('Update Complete', 'Video Added To Playlist Successfully.')
                updated = True
                break  # Stop after updating the first empty video column
        if not updated:
            sg.popup_error(f'Error: No open space found in playlist "{row["PlayList_Name"]}" for new videos.')
        
    # Save the updated DataFrame back to the CSV file
    df.to_csv('playlists.csv', index=False)
    print("Playlist CSV file has been updated.")


# Function to handle PySimpleGUI event loop
def run_gui(playlist_names):
    sg.theme('LightGrey1')
    window = sg.Window('Playlist Manager', create_layout(playlist_names))
    Loop = True
    while Loop:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Quit':  # Add a 'Quit' button or handle window close
            break  # Exit the loop
        
        if event == 'Add to Playlist':
            playlist_name = values['-PLAYLISTS-']
            # Error handling for missing keys
            video_title = values[f'-YOUTUBE_URL-{0}']
            md5Hash = add_video_to_playlist(playlist_name, video_title)
            update_playlist_videos(md5Hash)
        
        if event == 'Back To Home':
            Loop = False
    window.close()


# Main function to run the GUI application
def main():
    playlist_names = create_user_list("User1")
    run_gui(playlist_names)

if __name__ == '__main__':
    main()
