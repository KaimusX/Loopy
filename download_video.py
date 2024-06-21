from pytube import YouTube
import hashlib
import pandas as pd
from moviepy.editor import VideoFileClip
import os

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

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def add_video_hash_to_playlist(md5_hash):
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
            df.loc[df['PlayList_Name'] == playlist_name, video_slot] = md5_hash
            print(f'Added video to {video_slot} in playlist {playlist_name}.')
            break
    else:
        print('All video slots are full.')

    # Save the updated DataFrame to the CSV file
    df.to_csv('playlists.csv', index=False)

# Download the video and get the file path
video_url = 'https://youtu.be/f4FuR9fTKeo'
video_path = download_youtube_video(video_url)

#Break off the audio from the video
#break_off_Audio(video_path)

# Calculate the MD5 hash of the downloaded video
#md5Hash = calculate_md5(video_path)

#add the video hash to the playlist
add_video_hash_to_playlist(md5Hash)



