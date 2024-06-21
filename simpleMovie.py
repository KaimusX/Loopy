import PySimpleGUI as sg
import pygame
from moviepy.editor import VideoFileClip        #INSTALL USING --> pip install -r requirements.txt
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

# Get the current working directory and look for the video file in the 'Video_Media' folder
cwdV = os.path.join(os.getcwd(), 'Video_Media')
cwdA = os.path.join(os.getcwd(), 'Audio_Media')

# Define the file names
video_file_name = 'Car SysML.mp4'
audio_file_name = 'Car_SysML_audio.wav'

# Construct the full file paths
video_path = os.path.join(cwdV, video_file_name)
audio_path = os.path.join(cwdA, audio_file_name)

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

#added this code in order to ensure the video does not unessarily speed up past its set FPS
# Calculate the frame update interval in milliseconds
frame_update_interval = 1000 / video.fps  # video.fps gives the frames per second

# Initialize a variable to track the time of the last frame update
last_frame_update_time = pygame.time.get_ticks()

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
    
    # Get the current time in milliseconds since pygame was initialized    
    current_time = pygame.time.get_ticks()
    
    # Check if the video is currently playing and if the time elapsed since the last frame update
    # is equal to or greater than the frame update interval calculated based on the video's FPS
    if playing and (current_time - last_frame_update_time >= frame_update_interval):
        frame = update_frame()
        last_frame_update_time = current_time
       # imgbytes = pygame.image.tostring(frame, 'RGB')
       # window['-IMAGE-'].update(data=imgbytes)

# Clean up
window.close()
pygame.quit()
#os.remove(audio_path)  # Optionally remove the temporary audio file