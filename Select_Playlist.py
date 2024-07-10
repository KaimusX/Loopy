import PySimpleGUI as sg
import pygame
from moviepy.editor import *     
import mergeVid as mv
import csv


# Initialize pygame
pygame.init()
pygame.mixer.init()

#Set font for buttons
font = pygame.font.Font('freesansbold.ttf', 18)
#Button class for buttons (DO NOT CHANGE ANYTHING INSIDE THIS WITHOUT TALKING TO KALEIGH)

# Dropdown class for displaying playlist names
class Button():
    def __init__(self, scrn, text, x_pos, y_pos, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.draw(scrn)
    
    def draw(self, scrn):
        button_text = font.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150,25))
   
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        pygame.draw.rect(scrn, 'white', button_rect, 0, 5)
        scrn.blit(button_text, (self.x_pos+3, self.y_pos+3))
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (150,25))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False

def create_buttons(scrn, x_pos, y_pos, playlist_names):
    buttons = []
    for i, name in enumerate(playlist_names):
        button = Button(scrn, name, x_pos, y_pos + i * 30, True)
        buttons.append(button)
    return buttons

def Dropdown(scrn, x_pos, y_pos, playlist_names):
    pygame.init()
    buttons = create_buttons(scrn, x_pos, y_pos, playlist_names)
    run = True
    while run:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                run = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.check_click():
                        pygame.display.quit()
                        run = False
                        #videoPlayer(button.text)
                        val = button.text
    return val

#Update the frames  
def update_frame(video, scr):
    audio_pos = pygame.mixer.music.get_pos() / 1000.0
    frame = video.get_frame(audio_pos)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    scr.blit(frame, (0, 0))
    pygame.display.flip()
    return frame

# Function to play a video from the playlist
def Playlists(username):
        # Update the screen size
        pygame.init()
        width = 900
        height = 450
        scrn = pygame.display.set_mode([width, height])
        pygame.display.set_caption('LOOPY Video Player')
        playlsit = Dropdown(scrn, 100, 100, create_user_list(username))
        return playlsit

def create_user_list(username):
    playlist_names = []
    
    with open('playlists.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['User'] == username:
                playlist_names.append(row['PlayList_Name'])
    print(playlist_names)
    return playlist_names