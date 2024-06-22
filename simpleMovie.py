import PySimpleGUI as sg
import pygame
from moviepy.editor import *     
import os
import csv
import hashlib
import sys
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
def play_video(VidandAudPath):
    if VidandAudPath is not None:
        video = VideoFileClip(VidandAudPath[0])
        pygame.mixer.music.load(VidandAudPath[1])
        
        
        # Update the screen size
        width, height = video.size
        scrn = pygame.display.set_mode([width+200, height+200])
        pygame.display.set_caption('LOOPY Video Player')
        
        #is video playing
        playing = False
        #is loop running
        run = True
        #is the next click a new press
        new_press = True
        
        # Main loop
        while run:
            #initialize buttons
            startLoop = Button(scrn, 'Start Loop', 10, 400, True)
            playB = Button(scrn, 'Play', 10, 440, True)
            pauseB = Button(scrn, 'Pause', 10, 480, True)
            stopLoop = Button(scrn, 'Stop Loop', 10, 520, True)
            
            if pygame.mouse.get_pressed()[0] and new_press:
                new_press = False
            
            if not pygame.mouse.get_pressed()[0] and not new_press:
                new_press = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if startLoop.check_click():
                pygame.mixer.music.play()
                playing = True
            if playB.check_click():
                pygame.mixer.music.unpause()
                playing = True
            if pauseB.check_click():
                pygame.mixer.music.pause()
                playing = False
            if stopLoop.check_click():
                pygame.mixer.music.stop()
                run = False
            
            pygame.display.flip()
            if playing:
                frame = update_frame(video, scrn)
        
        # Clean up
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.quit()
        video.close()
        #delete temp playlist
        os.remove(VidandAudPath[0])
        os.remove(VidandAudPath[1])
    else:
        print('Video or audio file not found for MD5 hash:', video_md5, audio_md5)


if __name__ == '__main__':
    #calling functions form the mergeVid class in mergeVid.py
    merge = mv.mergeVid()
    play_video(merge.build_playlist("John"))
    
