import PySimpleGUI as sg
import pygame
from moviepy.editor import *     
import os
import csv
import hashlib
import sys

class mergeVid:
    """
    This class represents a video merger that can concat videos from a given playlist to play with the video player
    """
    def __init__(self):
        self.cwd = os.getcwd()
        self.playlist_file = os.path.join(self.cwd, 'playlists.csv')
        self.playlist = []
        self.playlist_3d = []

        # Read the playlist CSV and convert the CSV playlist into a 3D array with proper columns and rows,
        # excluding the header.
        try:
            with open(self.playlist_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                self.playlist = [row for row in reader]
                self.playlist_3d = [[row] for row in self.playlist]
        except FileNotFoundError:
            print(f"Error: {self.playlist_file} not found.")
        except Exception as e:
            print(f"An error occurred while reading {self.playlist_file}: {e}")

    #this class finds the playlist by name in the playlist
    def build_playlist(self, playlist_name):
        # FInd the playlist based on the name to a array, 
        # validating their MD5 hash as they are saved as file paths
        video_audio_pairs = []
        #find the playlist
        for playlist_row in self.playlist_3d:
            if playlist_row[0][0] == playlist_name:
                print('Building ', playlist_row[0][0], " playlist")
                # validate and add each video in the playlist
                for i in range(3, 13, 2):
                    video_md5 = playlist_row[0][i]
                    audio_md5 = playlist_row[0][i+10]
                    video_path = self.find_video_file(video_md5)
                    audio_path = self.find_audio_file(audio_md5)
                    if video_path is not None and audio_path is not None:
                        video_audio_pairs.append((video_path, audio_path))
                    else:
                        print('Video or audio file not found for MD5 hash:', video_md5, audio_md5)
                    if video_path is None or audio_path is None:
                        break
        self.concat_videos(video_audio_pairs)
        return os.path.join(self.cwd, "my_concatenation.mp4"), os.path.join(self.cwd, "my_concatenation_audio.mp3")
    
    def concat_videos(self, video_audio_pairs):
        video_clips = []
        audio_clips = []
        for video_path, audio_path in video_audio_pairs:
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            video_clips.append(video_clip)
            audio_clips.append(audio_clip)

        # Concatenate all video clips into one
        if video_clips:  # Check if the list is not empty
            final_clip = concatenate_videoclips(video_clips)
            final_clip.write_videofile("my_concatenation.mp4")
        else:
            print("No video clips to concatenate.")

        # Concatenate all audio clips into one
        if audio_clips:  # Check if the list is not empty
            final_audio = concatenate_audioclips(audio_clips)
            final_audio.write_audiofile("my_concatenation_audio.mp3")
        else:
            print("No audio clips to concatenate.")
                
    # Function to find the video file based on MD5 hash
    def find_video_file(self, md5_hash):
        video_media_path = os.path.join(self.cwd, 'Video_Media')
        for root, dirs, files in os.walk(video_media_path):
            for file in files:
                if hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest() == md5_hash:
                    return os.path.join(root, file)
        return None
    
    # Function to find the audio file based on MD5 hash
    def find_audio_file(self, md5_hash):
        audio_media_path = os.path.join(self.cwd, 'Audio_Media')
        for root, dirs, files in os.walk(audio_media_path):
            for file in files:
                if hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest() == md5_hash:
                    return os.path.join(root, file)
        return None
                
                
    