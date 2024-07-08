import PySimpleGUI as sg
import pygame
from moviepy.editor import *     
import mergeVid as mv
import create_playlist_GUI
import Select_Playlist

# Initialize pygame
pygame.init()
pygame.mixer.init()

#Set font for buttons
font = pygame.font.Font('freesansbold.ttf', 18)
#Button class for buttons (DO NOT CHANGE ANYTHING INSIDE THIS WITHOUT TALKING TO KALEIGH)
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

#Update the frames  
def update_frame(video, scr):
    audio_pos = pygame.mixer.music.get_pos() / 1000.0
    frame = video.get_frame(audio_pos)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    scr.blit(frame, (0, 0))
    pygame.display.flip()
    return frame

# Function to play a video from the playlist
def Home():
    
        # Update the screen size
        width = 1000
        height = 500
        scrn = pygame.display.set_mode([width, height])
        pygame.display.set_caption('LOOPY Video Player')
        
        #is loop running
        run = True
        #is the next click a new press
        new_press = True
        
        # Main loop
        while run:
            #initialize buttons
            Create = Button(scrn, 'Create Playlist', 100, 200, True)
            Select = Button(scrn, 'Select Playlist', 700, 200, True)
            
            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
            
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if Create.check_click():
                create_playlist_GUI.create_playlist()
            if Select.check_click():
                Select_Playlist.Playlists()
                pygame.quit()
                
            pygame.display.flip()
        
        # Clean up
        pygame.quit()

Home()
    