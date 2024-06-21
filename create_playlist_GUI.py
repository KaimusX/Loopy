import PySimpleGUI as sg
import re #import using -> pip install regex

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
            playlist_name = values['-PLAYLIST_NAME-']
            video_entries = []
            error = False
            for i in range(10): # 'For all ten possible entries in the playlist:'
                if values[f'-YOUTUBE-{i}'] and values[f'-YOUTUBE_URL-{i}']:
                    # If a playlist entry is not empty and contains a YouTube URL:
                    url = values[f'-YOUTUBE_URL-{i}']
                    if is_valid_youtube_url(url):
                        video_entries.append(('YouTube', url))
                        # If the YouTube URL is valid, append the entry to the Playlist list
                    else:
                        sg.popup_error(f'Invalid YouTube URL for Video {i+1}: {url}')
                        error = True
                        break
                        # If the YouTube URL is invalid, create a error pop-up and break 
                        # out of the create playlist window
                elif values[f'-LOCAL-{i}'] and values[f'-LOCAL_PATH-{i}']:
                    path = values[f'-LOCAL_PATH-{i}']
                    video_entries.append(('Local', path))
                     # If a playlist entry is not empty and a directory pathway, append the entry


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
