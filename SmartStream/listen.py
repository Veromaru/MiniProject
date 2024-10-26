import vosk
import pyaudio
import json
import pygame
import time

def play_sound(sound_file):
    """Play a sound using pygame."""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(-1)  # Play indefinitely

def stop_sound():
    """Stop the currently playing sound."""
    pygame.mixer.music.stop()

def recognize_text():
    """Performs speech recognition using Vosk and returns the recognized text.

    Returns:
        str: The recognized text, or an empty string if no speech is recognized.
    """
    try:
        # Specify the path to your downloaded Vosk model
        model_path = "vosk-model-small-en-us-0.15"

        # Create a Vosk Model object
        model = vosk.Model(model_path)

        # Initialize recognizer with the model
        rec = vosk.KaldiRecognizer(model, 16000)

        # Open audio stream from microphone
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

        # Play the listening sound
        #play_sound("soft-tone-001-9755.mp3") 
        #time.sleep(1)
        #stop_sound()


        print("Listening for speech. Say 'Terminate' to stop.")
        recognized_text = ""

       
        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                # Extract text from JSON result
                result = rec.Result()
                data = json.loads(result)
                text = data.get("text", "")
                recognized_text = text 
                
                # Stop sound when text is recognized
   
                
                
                return text

                if text.lower() == "terminate":  # Handle termination case insensitive
                    break

        # Close audio streams and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

        return recognized_text

    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return ""  # Return empty string on error

# Example usage
# text = recognize_text()
# print(text)