from pytube import YouTube
import hashlib
import pandas as pd
from moviepy.editor import VideoFileClip
import os
import shutil



class fileDownloader: 
    def __init__(self, video, source, playlist_name, output_path='Video_Media'):
        # Download the video and get the file path
        #video_url = 'https://www.youtube.com/watch?v=ucZl6vQ_8Uo'
        #video_url = 'https://www.youtube.com/watch?v=fMAK33FnaBE'
        
        if source == 'YouTube':
            video_path = self.download_youtube_video(video)
        else:
            video_path = self.download_local_video(video, output_path)
        #Break off the audio from the video
        audio_path = self.break_off_Audio(video_path)
        #Calculate the MD5 hash of the downloaded video
        md5HashVid = self.calculate_md5(video_path)
        md5HashAud = self.calculate_md5(audio_path)
        #add the video hash to the playlist
        self.add_video_hash_to_playlist(md5HashVid, md5HashAud, playlist_name)
        
    #downloads the video and puts it into the Video_Media folder
    def download_youtube_video(self, video, output_path='Video_Media'):
        try:
            # Create a YouTube object
            yt = YouTube(video)
            # Get the highest resolution stream available
            stream = yt.streams.get_highest_resolution()
            # Download the video
            video_path = stream.download(output_path)
            print(f'Download completed: {yt.title}')
            return video_path
        except Exception as e:
            print(f'An error occurred: {e}')

    def download_local_video(self, video_path, output_path='Video_Media'):
        try:
            # If path to video does not exist, make a path
            if not os.path.exists(output_path): 
                os.makedirs(output_path)
            # Then, join this path with the output_path
            destination_path = os.path.join(output_path, os.path.basename(video_path))
            # Then, copy this joined path and print out the joined path
            shutil.copy(video_path, destination_path)
            print(f'Local video copied to: {destination_path}')
            return destination_path
        except Exception as e:
            print(f'An error occurred while copying local video: {e}')
            return None
                    

    def break_off_Audio(self, video_path, output_dir='Audio_Media'):  
        print(f'Extracting audio from {video_path}')
        # Extract the base name without extension and append .mp3
        base_name = os.path.splitext(os.path.basename(video_path))[0] + '_audio.wav'
        output_path = os.path.join(output_dir, base_name)
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Load the video file for editing
        video = VideoFileClip(video_path)
        # Extract and save the audio file in the specified location
        video.audio.write_audiofile(output_path)
        return output_path

    def calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def add_video_hash_to_playlist(self, md5_hashVid, md5_hashAud, playlist_name):
        # Load the DataFrame from the CSV file
        df = pd.read_csv('playlists.csv')

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



