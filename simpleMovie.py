import PySimpleGUI as sg
import pygame
from moviepy.editor import VideoFileClip        #INSTALL USING --> pip install moviepy
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Define the layout of the GUI
layout = [
    [sg.Text('LOOPY Video Player')],
    [sg.Image(filename='', key='-IMAGE-')],
    [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop'), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Video Player', layout, finalize=True)

# Set up the video file using a dynamic path: Made by Jonah Dalton on 6/20/2024
# Get the current working directory
cwd = os.path.join(os.getcwd(), 'Video_Media')

# Define the file names
video_file_name = 'CarSysML.mp4'
audio_file_name = 'Car_SysML_audio.wav'

# Construct the full file paths
video_path = os.path.join(cwd, video_file_name)
audio_path = os.path.join(cwd, audio_file_name)

#run with the video file in the same directory as the script
video = VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

# Set up pygame screen
width, height = video.size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('LOOPY Video Player')

# Load and play the audio
pygame.mixer.music.load(audio_path)

# Define variables for video playback
playing = False

# Function to update video frame in the GUI
def update_frame():
    frame = video.get_frame(video.reader.pos / video.fps)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))
    pygame.display.flip()
    return frame

# Main loop
while True:
    event, values = window.read(timeout=10)
    
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Play':
        pygame.mixer.music.play()
        playing = True
    elif event == 'Pause':
        pygame.mixer.music.pause()
        playing = False
    elif event == 'Stop':
        pygame.mixer.music.stop()
        playing = False

    if playing:
        frame = update_frame()
       # imgbytes = pygame.image.tostring(frame, 'RGB')
       # window['-IMAGE-'].update(data=imgbytes)

# Clean up
window.close()
pygame.quit()
os.remove(audio_path)  # Optionally remove the temporary audio file