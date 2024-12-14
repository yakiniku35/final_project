import math
import random
import time
import pygame
pygame.init()


# TODO-1: Set up the basic game window
'''
Create a window of size 800x600 using Pygame.
Set the game window title to "Aim Trainer".
Define the background color (RGB value: (0, 25, 40)).
'''






# TODO-2: Create the Target class
'''
Define the Target class to represent each target.
Implement the __init__() method to initialize the target's position, size, and growth state.
Create the update() method to handle the growth and shrinkage of the target.
Implement the draw() method to display the target on the screen with multiple concentric circle effects.
Implement the collide() method to check if a click hits the target.
'''


# TODO-3: Set up the game drawing function
'''
Create the draw() function to fill the background and draw all targets on the screen.
'''


# TODO-4: Create the time formatting function
'''
Define the format_time() function to format the elapsed time into "MM:SS.m" format.
Make sure the milliseconds display correctly for accurate time tracking.
'''


# TODO-5: Draw the top bar
'''
Create the draw_top_bar() function to display the top bar showing time, speed, hits, and remaining lives.
Use the pygame.font.SysFont() to display text on the top bar.
'''


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


# TODO-10: Test and debug the game
'''
Test the game functionality:
Ensure targets are generated at random positions.
Ensure time and score are displayed correctly.
Verify mouse click detection works properly.
Handle edge cases (e.g., missing targets, clicking outside the game window).
Debug and fix any issues encountered during testing.
'''