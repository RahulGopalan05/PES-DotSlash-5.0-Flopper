# Python
import os
import pygame
from pygame.locals import *
import speech_recognition as sr
import keyboard
import threading

# Get a list of all files in the "alphabet" directory
image_files = os.listdir("alphabet")

# Create a dictionary mapping each letter to its corresponding file
image_files = {file[0]: os.path.join("alphabet", file) for file in image_files}

def load_image(file, size):
    image = pygame.image.load(file)
    return pygame.transform.scale(image, size)

def draw_image(image, screen):
    screen.blit(image, (0, 0))

def interpret_text(text, size):
    text = text.lower()
    image_sequence = []
    for char in text:
        if char in image_files:
            image = load_image(image_files[char], size)
            image_sequence.append(image)
    return image_sequence

stop_recording = False

def listen_for_stop_key():
    global stop_recording
    keyboard.wait('s')
    stop_recording = True

def get_input():
    global stop_recording
    choice = input("Do you want to type or speak the text? (type/speak): ")
    if choice.lower() == "type":
        text = input("Enter the text: ")
    elif choice.lower() == "speak":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak now... Press 's' to stop recording.")
            stop_recording = False
            stop_key_thread = threading.Thread(target=listen_for_stop_key)
            stop_key_thread.start()
            audio = None
            while True:
                try:
                    audio = recognizer.record(source, duration=5)  # Record audio for 5 seconds
                    if stop_recording:  # If 's' key is pressed, stop recording
                        print("Recording stopped.")
                        break
                except:
                    break
            if audio is not None:
                try:
                    text = recognizer.recognize_google(audio)
                    print("You said: " + text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                    text = ""
    else:
        print("Invalid choice. Please choose 'type' or 'speak'.")
        text = get_input()
    return text

def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF)

    text = get_input()  # Get input from the user
    image_sequence = interpret_text(text, display)

    image_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))  # Clear the screen with black

        # Draw the current image
        draw_image(image_sequence[image_index], screen)

        pygame.display.flip()

        # Wait for 2 seconds
        pygame.time.wait(1000)

        # Move to the next image
        image_index += 1
        if image_index >= len(image_sequence):
            break  # Exit the loop when all images have been shown

if __name__ == "__main__":
    main()
