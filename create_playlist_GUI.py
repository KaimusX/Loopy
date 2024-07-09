import PySimpleGUI as sg
import re 
import download_video as dv
import playlist as pl
import os

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
    MAX_INPUT_LENGTH = 2048

    # Defines the contents of the window

    layout = [
        [sg.Text('LOOPY Playlist Creator')],
        [sg.Text('Playlist Name:'), sg.InputText(key='-PLAYLIST_NAME-')],
        [sg.Text('Select Video Source (max 10 entries):')]
    ]
    
    # Defines more contents of the window (namely, the reocurring features)
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

    # Creates the window

    window = sg.Window('Video Playlist Creator', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break
            # The 'Cancel' button causes the program to break
        elif event == 'Submit':
            if values['-PLAYLIST_NAME-']:
                playlist_name = values['-PLAYLIST_NAME-']
                video_entries = []
                error = False
                for i in range(10): # 'For all ten possible entries in the playlist:'

                    # Defines the appropriate variables
                    youtube_url = values[f'-YOUTUBE_URL-{i}']
                    local_path = values[f'-LOCAL_PATH-{i}']
                    if values[f'-YOUTUBE-{i}'] and  youtube_url:

                        if len(youtube_url) > MAX_INPUT_LENGTH:
                            sg.popup_error(f'YouTube URL for Video {i+1} is too long. Please shorten it.')
                            error = True
                            break

                        # If a playlist entry is not empty and contains a YouTube URL:
                        if is_valid_youtube_url(youtube_url):
                            video_entries.append(('YouTube', youtube_url))
                            # If the YouTube URL is valid, append the entry to the Playlist list
                        else:
                            sg.popup_error(f'Invalid YouTube URL for Video {i+1}: {youtube_url}')
                            error = True
                            break
                            # If the YouTube URL is invalid, create a error pop-up and break 
                            # out of the create playlist window
                    elif values[f'-LOCAL-{i}'] and values[f'-LOCAL_PATH-{i}']:
                        # path = values[f'-LOCAL_PATH-{i}'].replace('/', '\\')
                        if len(local_path) > MAX_INPUT_LENGTH:
                            sg.popup_error(f'Local file path for Video {i+1} is too long. Please shorten it.')
                            error = True
                            break

                        if os.path.isfile(local_path):
                            # If a playlist entry is not empty and a directory pathway, append the entry
                            # Check if the local file is an MP4 file
                            if local_path.lower().endswith('.mp4'):
                                video_entries.append(('Local', local_path))
                            else:
                                sg.popup_error(f'File for Video {i+1} is not an MP4 file: {local_path}')
                                error = True
                                break

                        else:
                            sg.popup_error(f'Invalid local file path for Video {i+1}: {local_path}')
                            error = True
                            break
            else:
                sg.popup_error('Please provide a name for the playlist.')
                error = True
                continue


        if not video_entries:
            sg.popup_error('Please add at least one video to the playlist.')
            error = True
            continue


        if not error:
            # Handle the collected data here
            try:
                playlist_database = pl.Playlist()
                playlist_database.create_playlist(playlist_name)
                for entry in video_entries:
                    source, url_or_path = entry
                    dv.fileDownloader(url_or_path, source, playlist_name)
                sg.popup('Playlist created successfully!')
                window.close()
                break

            except Exception as e:
                sg.popup_error(f'An error occurred while creating the playlist: {e}')

    window.close() #tab this in 1 in case error
    
if __name__ == "__main__":
    create_playlist()