import PySimpleGUI as sg
import pygame
from moviepy.editor import *     
import mergeVid as mv


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
def Playlists():
    
        # Update the screen size
        width = 900
        height = 450
        scrn = pygame.display.set_mode([width, height])
        pygame.display.set_caption('LOOPY Video Player')
        
        #is loop running
        run = True
        #is the next click a new press
        new_press = True
        
        # Main loop
        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.flip()
        
        # Clean up
        pygame.quit()

    