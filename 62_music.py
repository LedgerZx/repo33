import pygame
import time

# Initialize the mixer module
pygame.mixer.init()

def play_music(file_path):
    # Load the music file
    pygame.mixer.music.load(file_path)
    # Play the music
    pygame.mixer.music.play()
    print(f"Playing music: {file_path}")

def pause_music():
    # Pause the music
    pygame.mixer.music.pause()
    print("Music paused")

def unpause_music():
    # Unpause the music
    pygame.mixer.music.unpause()
    print("Music unpaused")

def stop_music():
    # Stop the music
    pygame.mixer.music.stop()
    print("Music stopped")

def main():
    # Path to the music file
    music_file = "path/to/your/music/file.mp3"

    play_music(music_file)

    # Wait for 5 seconds
    time.sleep(5)

    pause_music()

    # Wait for 5 seconds
    time.sleep(5)

    unpause_music()

    # Wait for 5 seconds
    time.sleep(5)

    stop_music()

if __name__ == "__main__":
    main()
