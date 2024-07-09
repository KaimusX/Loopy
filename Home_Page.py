import PySimpleGUI as sg
import pygame
from moviepy.editor import *     
import mergeVid as mv
import create_playlist_GUI
import Select_Playlist
import UpdatePlaylist
import time
from cvplayerlocal import VideoPlayer
import Instructions_GUI
import threading

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

def videoPlayer(playlistName):
    merge = mv.mergeVid()
    #make this selectable instead of a set playlist name later
    merge.build_playlist(playlistName)
    player = VideoPlayer("my_concatenation.mp4")

    while True:
        if player.state != 'eof':
            time.sleep(0)
    
        if player.state == 'eof':
            player.seek(0, relative = False)
            player.get_frame() 
        
        if player.state == 'quit':
            pygame.init()
            Home()
def RunGUI():
    gui = Instructions_GUI.InstructionsGUI()
    # Call the create_gui method to create the instructions GUI
    gui.create_gui()
# Function to play a video from the playlist
def Home():
    # Initialize pygame
    # Update the screen size
    run = True
    width = 1000
    height = 500
    scrn = pygame.display.set_mode([width, height])
    pygame.display.set_caption('LOOPY Video Player')   
    #is loop running
    #is the next click a new press
    new_press = True
        
    # Main loop
    while run:
        #initialize buttons
        Create = Button(scrn, 'Create Playlist', 100, 200, True)
        Edit = Button(scrn, 'Edit Playlist', 400, 200, True)
        Select = Button(scrn, 'Select Playlist', 700, 200, True)
            
        if pygame.mouse.get_pressed()[0] and new_press:
            new_press = False
            
        if not pygame.mouse.get_pressed()[0] and not new_press:
            new_press = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
        if Create.check_click():
            create_playlist_GUI.create_playlist()
        if Edit.check_click():
            UpdatePlaylist.main()
        if Select.check_click():
            name = Select_Playlist.Playlists()
            run = False
            # Create an instance of the InstructionsGUI class
            gui_thread = threading.Thread(target=RunGUI)
            gui_thread.start()
            #pygame.quit()
            videoPlayer(name)
                
        pygame.display.flip()
        
    # Clean up
    pygame.display.quit()

if __name__ == "__main__":
    pygame.display.init()
    Home()