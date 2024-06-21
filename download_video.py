from pytube import YouTube
import hashlib
import pandas as pd
from moviepy.editor import VideoFileClip
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



#downloads the video and puts it into the Video_Media folder
def download_youtube_video(url, output_path='Video_Media'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()

        # Download the video
        video_path = stream.download(output_path)

        print(f'Download completed: {yt.title}')
        return video_path
    except Exception as e:
        print(f'An error occurred: {e}')
                

def break_off_Audio(irl, output_dir='Audio_Media'):  
    # Extract the base name without extension and append .mp3
    base_name = os.path.splitext(os.path.basename(irl))[0] + '_audio.wav'
    output_path = os.path.join(output_dir, base_name)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the video file for editing
    video = VideoFileClip(irl)
    # Extract and save the audio file in the specified location
    video.audio.write_audiofile(output_path)
    return output_path

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def add_video_hash_to_playlist(md5_hashVid, md5_hashAud):
    # Load the DataFrame from the CSV file
    df = pd.read_csv('playlists.csv')

    # Get the user's input for the playlist name
    playlist_name = input('Enter the name of the playlist: ')

    # Check if the playlist name is valid
    if playlist_name not in df['PlayList_Name'].values:
        print('Invalid playlist name.')
        return

    # Get the row for the selected playlist
    playlist_row = df.loc[df['PlayList_Name'] == playlist_name]

    # Iterate over the video slots and choose the first one that is empty
    for i in range(1, 11):
        video_slot = f'Video{i}'


        if pd.isnull(playlist_row[video_slot].values[0]):
            # Add the hash to the selected video slot
            df.loc[df['PlayList_Name'] == playlist_name, video_slot] = md5_hashVid
            print(f'Added video to {video_slot} in playlist {playlist_name}.')
            break
        
    for i in range(1, 11):
        audio_slot = f'Audio{i}'

        if pd.isnull(playlist_row[audio_slot].values[0]):
            # Add the hash to the selected audio slot
            df.loc[df['PlayList_Name'] == playlist_name, audio_slot] = md5_hashAud
            print(f'Added audio to {audio_slot} in playlist {playlist_name}.')
            break
    else:
        print('All video slots are full.')

    # Save the updated DataFrame to the CSV file
    df.to_csv('playlists.csv', index=False)

# Download the video and get the file path
#video_url = 'https://www.youtube.com/watch?v=ucZl6vQ_8Uo'
video_url = 'https://www.youtube.com/watch?v=fMAK33FnaBE'
video_path = download_youtube_video(video_url)

#Break off the audio from the video
audio_path = break_off_Audio(video_path)
#Calculate the MD5 hash of the downloaded video
md5HashVid = calculate_md5(video_path)
md5HashAud = calculate_md5(audio_path)


#add the video hash to the playlist
add_video_hash_to_playlist(md5HashVid, md5HashAud)



