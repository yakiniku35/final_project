import math
import random
import time
import pygame
pygame.init()


# TODO-1: Set up the basic game window (林柏仲)
'''
Create a window of size 800x600 using Pygame.
Set the game window title to "Aim Trainer".
Define the background color (RGB value: (0, 25, 40)).
'''

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer") #建立視窗及標題
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TIME_LIMIT = 300
LIVES = 3
# TODO-2: Create the Target class (邱彥嘉)
'''
Define the Target class to represent each target.
Implement the __init__() method to initialize the target's position, size, and growth state.
Create the update() method to handle the growth and shrinkage of the target.
Implement the draw() method to display the target on the screen with multiple concentric circle effects.
Implement the collide() method to check if a click hits the target.
'''

class Target:
    Max_SIZE = 30
    GROWTH_RATE = 0.2 # how many pixels it grows per frame
    COLOR = "red" # the color of the target
    SECOND_COLOR = "white" # the color of the second circle
    
    def __init__(self,x,y): # seff means target it self, and x and y are the position of target
        self.x = x
        self.y = y
        self.size = 0 # radius of target
        self.grow = True # if it grows or not
        
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False # when target reaches the max size, it will stop growing
        if self.grow:
            self.size += self.GROWTH_RATE # grow the target
        else:
            self.size -= self.GROWTH_RATE # shrink the target
     
    def draw(self,win): # to have ring shape
        pygame.draw.circle(win,self.COLOR, (self.x,self.y),self.size) # draw a larger and larger target(circle)
        pygame.draw.circle(win,self.SECOND_COLORCOLOR, (self.x,self.y),self.size * 0.8) # draw a smaller and smaller target(circle)
        pygame.draw.circle(win,self.COLOR, (self.x,self.y),self.size * 0.6) 
        pygame.draw.circle(win,self.SECOND_COLORCOLOR, (self.x,self.y),self.size * 0.4) 
        
        
#上面             
# TODO-3: Set up the game drawing function (邱彥嘉)
'''
Create the draw() function to fill the background and draw all targets on the screen.
'''            



# TODO-4: Create the time formatting function (邱彥嘉)
'''
Define the format_time() function to format the elapsed time into "MM:SS.m" format.
Make sure the milliseconds display correctly for accurate time tracking.
'''

start_time = 0



# TODO-5: Draw the top bar
'''
Create the draw_top_bar() function to display the top bar showing time, speed, hits, and remaining lives.
Use the pygame.font.SysFont() to display text on the top bar.
'''
TOP_BAR_HEIGHT = 50
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

# TODO-6: Implement the end screen
'''
Create the end_screen() function to display the game statistics after the game ends (time, hits, accuracy).
Implement functionality for the end screen to wait for user input (e.g., key press or window close).
'''


# TODO-7: Handle mouse click detection
'''
Handle pygame.MOUSEBUTTONDOWN event to detect mouse clicks.
Check if the mouse click hits any target and remove it from the game if it does.
Increment the hits counter when a target is successfully clicked.
'''


# TODO-8: Handle missed targets and game over
'''
Track the number of missed targets (when target size reaches zero).
Set the number of lives to 3, and end the game if the number of misses exceeds this value.
'''




# TODO-9: Main game loop
'''
Set up the main game loop to:
Periodically generate new targets using pygame.time.set_timer().
Check for mouse clicks and collisions.
Update target sizes and remove targets when they shrink completely.
Draw the updated game state (targets, top bar, etc.) each frame.
'''


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        # 檢查是否超過時間限制
        if elapsed_time >= TIME_LIMIT:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

# TODO-10: Test and debug the game
'''
Test the game functionality:
Ensure targets are generated at random positions.
Ensure time and score are displayed correctly.
Verify mouse click detection works properly.
Handle edge cases (e.g., missing targets, clicking outside the game window).
Debug and fix any issues encountered during testing.
'''