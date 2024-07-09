import PySimpleGUI as sg
import pygame
import pandas as pd
import csv
import PySimpleGUI as sg
import re 
import download_video as dv
import playlist as pl
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set font for buttons (assuming you are using PySimpleGUI for buttons)
font = pygame.font.Font('freesansbold.ttf', 18)

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    return re.match(youtube_regex, url)




# Function to create PySimpleGUI layout for playlists and buttons
def create_layout(playlist_names):
    
    layout = [
        [sg.Text('Select Playlist to Manage:')],
        [sg.Listbox(values=playlist_names, size=(30, 6), key='-PLAYLISTS-', enable_events=True)],
        [sg.Button('Add Video to Playlist'), sg.Button('Rename Playlist')],
        [sg.Button('Close')]
    ]

    layout.extend([
        [sg.Text(f'Video {1} Source:'), 
        sg.Radio('YouTube URL', f'RADIO{0}', key=f'-YOUTUBE-{0}', default=True), 
        sg.InputText(key=f'-YOUTUBE_URL-{0}', size=(15, 1)), 
        sg.Radio('Local File Path', f'RADIO{0}', key=f'-LOCAL-{0}'), 
        sg.InputText(key=f'-LOCAL_PATH-{0}', size=(15, 1)), sg.FileBrowse()],
        ])

    layout.append([sg.Button('Submit'), sg.Button('Cancel')])

    return layout

# Function to handle adding a song to a playlist
def add_video_to_playlist(playlist_name, video_title):
    # Load the DataFrame from the CSV file
    df = pd.read_csv('playlists.csv')

    # Check if the playlist name exists
    if playlist_name not in df['PlayList_Name'].values:
        print(f'Playlist "{playlist_name}" does not exist.')
        return

    # Add the song to the playlist
    new_row = {'PlayList_Name': playlist_name, 'Video_Title': video_title}
    df = df._append(new_row, ignore_index=True)

    print(f'Video "{video_title}" added to playlist "{playlist_name}".')

    # Save the updated DataFrame to the CSV file
    df.to_csv('playlists.csv', index=False)

# Function to handle renaming a playlist
def rename_playlist(current_name, new_name):
    # Load the DataFrame from the CSV file
    df = pd.read_csv('playlists.csv')

    # Check if the current playlist name exists
    if current_name not in df['PlayList_Name'].values:
        print(f'Playlist "{current_name}" does not exist.')
        return

    # Rename the playlist
    df.loc[df['PlayList_Name'] == current_name, 'PlayList_Name'] = new_name
    print(f'Playlist "{current_name}" renamed to "{new_name}".')

    # Save the updated DataFrame to the CSV file
    df.to_csv('playlists.csv', index=False)

# Function to handle PySimpleGUI event loop
def run_gui(playlist_names):
    sg.theme('LightGrey1')
    window = sg.Window('Playlist Manager', create_layout(playlist_names))
    event, values = window.read()
    playlist_name = values['-PLAYLISTS-'] # keep this for code to run

    while True:
        event, values = window.read()
        video_entries = []
        #selected_playlist = values['-PLAYLISTS-']
        error = False

        youtube_url = values[f'-YOUTUBE_URL-{0}']
        local_path = values[f'-LOCAL_PATH-{0}']
        MAX_INPUT_LENGTH = 2048


        if event == sg.WINDOW_CLOSED or event == 'Close':
            break
        elif event == '-PLAYLISTS-':
            selected_playlist = values['-PLAYLISTS-'][0]
            # Handle selection of playlist
            # Example: You might want to update some UI elements or perform other actions

        elif event == 'Add Video to Playlist': #Changed from add video to playlist

            # Example: Prompt user for song details and add it to selected playlist
            playlist_name = values['-PLAYLISTS-'][0] if values['-PLAYLISTS-'] else None
            if playlist_name:

                if values[f'-YOUTUBE-{0}'] and  youtube_url:

                    if len(youtube_url) > MAX_INPUT_LENGTH:
                        sg.popup_error(f'YouTube URL for Video {1} is too long. Please shorten it.')
                        error = True
                        break

                        # If a playlist entry is not empty and contains a YouTube URL:
                    if is_valid_youtube_url(youtube_url):
                        video_entries.append(('YouTube', youtube_url))
                        # If the YouTube URL is valid, append the entry to the Playlist list
                    else:
                        sg.popup_error(f'Invalid YouTube URL for Video {1}: {youtube_url}')
                        error = True
                        break
                        # If the YouTube URL is invalid, create a error pop-up and break 
                        # out of the create playlist window
                elif values[f'-LOCAL-{0}'] and local_path:
                        # path = values[f'-LOCAL_PATH-{i}'].replace('/', '\\')
                    if len(local_path) > MAX_INPUT_LENGTH:
                        sg.popup_error(f'Local file path for Video {1} is too long. Please shorten it.')
                        error = True
                        break

                    if os.path.isfile(local_path):
                        # If a playlist entry is not empty and a directory pathway, append the entry
                        # Check if the local file is an MP4 file
                        if local_path.lower().endswith('.mp4'):
                            video_entries.append(('Local', local_path))
                        else:
                            sg.popup_error(f'File for Video {1} is not an MP4 file: {local_path}')
                            error = True
                            break

                    else:
                        sg.popup_error(f'Invalid local file path for Video {1}: {local_path}')
                        error = True
                        break
        if not error:
            # Handle the collected data here
            try:
                playlist_database = pl.Playlist()
                #playlist_database.add_video_to_playlist(playlist_name, video_title)
                #for entry in video_entries:
                    #source, url_or_path = entry
                    #dv.fileDownloader(url_or_path, source, playlist_name)
                sg.popup('Playlist changed successfully!')
                window.close()
                break

            except Exception as e:
                sg.popup_error(f'An error occurred while changing the playlist: {e}')


        elif event == 'Rename Playlist':
            # Example: Prompt user for new name and rename the selected playlist
            playlist_name = values['-PLAYLISTS-'][0] if values['-PLAYLISTS-'] else None
            if playlist_name:
                new_name = sg.popup_get_text('Enter New Playlist Name:')
                rename_playlist(playlist_name, new_name)

    window.close()

# Function to create a list of user-specific playlist names
def create_user_list():
    playlist_names = []
    
    with open('playlists.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['User'] == 'User1':
                playlist_names.append(row['PlayList_Name'])
    return playlist_names

# Main function to run the GUI application
def main():
    playlist_names = create_user_list()
    run_gui(playlist_names)

if __name__ == '__main__':
    main()
