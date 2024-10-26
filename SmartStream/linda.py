import tkinter as tk
import threading
import pyttsx3
import os
import random
import wikipedia
import listen  # Assuming 'listen' is a custom module for audio input
import cohere
import time
import json
import webbrowser
import re
import sys

def run_linda_voice_assistant():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('Rate', 7)
    engine.setProperty('voice', voices[1].id)

    def speak(text):
        # Display Linda's response in the GUI in yellow (#fdc346)
        add_message("Linda: " + text, "#fdc346")
        engine.say(text)
        engine.runAndWait()
        
    def check_web_app(command2):
        # Load the JSON data
        with open('web_apps.json', 'r') as file:
            web_apps = json.load(file)

        # Convert keys to lowercase for case-insensitive matching
        web_apps_lower = {key.lower(): value for key, value in web_apps.items()}

        # Prompt for the command
        user_input = command2.strip().lower()

        # Check if the input matches the required format
        match = re.match(r'linda open (\w+)', user_input)
        if match:
            app_name = match.group(1)  # Extract the app name
            link = web_apps_lower.get(app_name)

            if link:
                response = f"Opening link for {app_name.capitalize()}"
                print(response)
                speak(response)  # Speak the response
                webbrowser.open(link)  # Open the link in the default web browser
            else:
                response = f"No link found for '{app_name.capitalize()}'."
                print(response)
                speak(response)  # Speak the response
            
                # Get the first letter of the input app name
                first_letter = app_name[0]
            
                # Filter available web apps by the same first letter
                available_apps = [app for app in web_apps_lower.keys() if app.startswith(first_letter)]
            
                if available_apps:
                    print("Available web apps starting with '{}':".format(first_letter))
                    speak("Available web apps starting with '{}':".format(first_letter))
                    for i, app in enumerate(available_apps, start=1):
                        app_name = app.capitalize()
                        print(f"{number_to_word(i)}. {app_name}")
                        speak(f"select {number_to_word(i)} for {app_name}")  # Speak each app name

                    # Allow the user to select an app by word
                    speak("select your option")
                    listen.play_sound("00ad0b6b04e9c50c53d2c2a8da552a37.wav")
                    time.sleep(0.5)
                    listen.stop_sound()
                    choice = listen.recognize_text().strip().lower()
                    word_to_number = {
                    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
                    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
                    'nineteen': 19, 'twenty': 20, 'twenty-one': 21, 'twenty-two': 22,
                    'twenty-three': 23, 'twenty-four': 24, 'twenty-five': 25,
                    'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28,
                    'twenty-nine': 29, 'thirty': 30, 'thirty-one': 31, 'thirty-two': 32,
                    'thirty-three': 33, 'thirty-four': 34, 'thirty-five': 35,
                    'thirty-six': 36, 'thirty-seven': 37, 'thirty-eight': 38,
                    'thirty-nine': 39, 'forty': 40, 'forty-one': 41, 'forty-two': 42,
                    'forty-three': 43, 'forty-four': 44, 'forty-five': 45,
                    'forty-six': 46, 'forty-seven': 47, 'forty-eight': 48,
                    'forty-nine': 49, 'fifty': 50
                    }
    
                    if choice in word_to_number:
                        index = word_to_number[choice] - 1
                        if 0 <= index < len(available_apps):
                            selected_app = available_apps[index]
                            response = f"Opening link for {selected_app.capitalize()}"
                            print(response)
                            speak(response)  # Speak the response
                            webbrowser.open(web_apps_lower[selected_app])
                        else:
                            response = "Invalid selection. Please try again."
                            print(response)
                            speak(response)  # Speak the response
                    else:
                        response = "Invalid choice. Please select a valid app word."
                        print(response)
                        speak(response)  # Speak the response
                else:
                    response = "No available web apps start with that letter."
                    print(response)
                    speak(response)  # Speak the response
        else:
            response = "Please enter a command in the format 'linda open [app name]'."
            print(response)
            speak(response)  # Speak the response

    def number_to_word(num):
        """Convert a number to its corresponding word representation (1-50)."""
        words = [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
        "eighteen", "nineteen", "twenty", "twenty-one", "twenty-two", "twenty-three",
        "twenty-four", "twenty-five", "twenty-six", "twenty-seven", "twenty-eight",
        "twenty-nine", "thirty", "thirty-one", "thirty-two", "thirty-three", "thirty-four",
        "thirty-five", "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine",
        "forty", "forty-one", "forty-two", "forty-three", "forty-four", "forty-five",
        "forty-six", "forty-seven", "forty-eight", "forty-nine", "fifty"
        ]
        return words[num - 1] if 1 <= num <= 50 else None

    def update_command(command):
        # Display the user command in the GUI in white
        add_message("You: " + command, "white")

    def add_message(message, color):
        # Add message to the GUI
        text_display.config(state=tk.NORMAL)
        text_display.insert(tk.END, message + "\n", ("color", color))
        text_display.tag_configure("color", foreground=color)
        text_display.config(state=tk.DISABLED)
        text_display.see(tk.END)  # Auto scroll to the bottom

    def listen_commands():
        while True:
            listen.play_sound("00ad0b6b04e9c50c53d2c2a8da552a37.wav")
            time.sleep(0.5)
            listen.stop_sound() 
            command = listen.recognize_text()  # Replace with your actual command recognition logic
            if command:
                print("Command:", command)
                update_command(command)

                if not command.lower().startswith("linda"):
                    continue

                # Handle different commands here
                if command.lower() in ["linda hello", "linda hi", "linda hey", "linda"]:
                    greetings = ["Hello!, how are you!", "Hi there", "Hey there!"]
                    speak(random.choice(greetings))

                elif 'linda guide' in command.lower() or 'linda tutorial' in command.lower():
                    speak("Certainly, to open files simply say open and FILENAME. To create written text from voice simply say create.")
                    speak("To delete text files say delete and filename. And remember to say linda before every request. Thank you for listening.")

                elif 'linda search' in command.lower():
                    search_words = command.lower().split()[2:]  # Split the command after "linda search"
                    search_topic = ' '.join(search_words)
                    if search_topic:
                        try:
                            wikipedia_summary = wikipedia.summary(search_topic, sentences=2)
                            speak("According to Wikipedia, " + wikipedia_summary)
                        except wikipedia.exceptions.DisambiguationError:
                            speak("There are multiple possible results for that search. Please be more specific.")
                        except wikipedia.exceptions.PageError:
                            speak("I'm sorry, I couldn't find any information about that on Wikipedia.")
                    else:
                        speak("Please specify what you would like to search for after 'linda search'.")

                elif 'linda list' in command.lower() or 'linda least files' in command.lower() or 'linda list files' in command.lower():
                    speak("Your files are :")
                    list_files('files')

                elif 'linda open' in command.lower():
                    check_web_app(command)

                elif 'linda read' in command.lower():
                    read_text_file('files')

                elif 'linda create' in command.lower():
                    speak("What would you like your filename to be?")
                    file_name = listen.recognize_text()
                    file_path = "files/" + file_name + ".txt"
                    with open(file_path, 'a') as file:
                        speak("Now, let's fill it with content. Say 'stop' when you are done.")
                        while True:
                            content = listen.recognize_text()
                            if content.lower() == "stop":
                                speak("Stopping")
                                break
                            else:
                                file.write(content + "\n")
                                listen.play_sound("soft-tone-001-9755.mp3")
                                time.sleep(0.5)
                                listen.stop_sound() 
                    speak("File with name, " + file_name + " created successfully.")
                    
                elif 'linda stop' in command.lower():
                    speak("Stopping Linda. Goodbye!")
                    root.quit() 
                    sys.exit()

                elif 'linda delete' in command.lower():
                    speak("What is the file you want to delete?")
                    fname = listen.recognize_text()
                    file_path = "files/" + fname + ".txt"
                    if delete_file(file_path):
                        speak("File deletion successful!")
                    else:
                        speak("File deletion failed.")

                elif 'linda update' in command.lower():
                    speak("What is the file you would like to update?")
                    filename = listen.recognize_text()
                    file_path = "files/" + filename + ".txt"
                    speak("What text would you like to add?")
                    text_to_append = listen.recognize_text()
                    if append_to_file(file_path, text_to_append):
                        speak("Successfully added text to the file.")
                    else:
                        speak("Failed to append text to the file.")
                
                else:
                    addition = "You are an AI named Linda, respond only when 'linda' is invoked and do not keep saying you are linda unless asked"
                    response = generate_response(addition + command)
                    speak(response)

    def list_files(directory):
        try:
            files = os.listdir(directory)
            txt_files = [os.path.splitext(f)[0] for f in files if f.endswith('.txt')]
            for file in txt_files:
                speak(file)
        except Exception as e:
            print(f"An error occurred: {e}")

    # def read_text_file(directory):
    #     try:
    #         files = os.listdir(directory)
    #         txt_files = [os.path.splitext(f)[0] for f in files if f.endswith('.txt')]
    #         speak("What is the file name?")
    #         selected_name = listen.recognize_text()
    #         if selected_name in txt_files:
    #             file_path = os.path.join(directory, selected_name + '.txt')
    #             with open(file_path, 'r') as f:
    #                 content = f.read()
    #                 speak("File content:")
    #                 speak(content)
    #         else:
    #             speak("File not found.")
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    
    def read_text_file(directory):
        try:
            # List all files in the directory
            files = os.listdir(directory)
            # Filter for .txt files and remove the extension
            txt_files = [os.path.splitext(f)[0] for f in files if f.endswith('.txt')]
        
            # Prompt the user for a file name (without extension)
            speak("what is the file name?")
            selected_name = listen.recognize_text().strip()
        
            # Check if the selected file is in the list
            if selected_name in txt_files:
                file_path = os.path.join(directory, selected_name + '.txt')
                # Open and read the file
                with open(file_path, 'r') as f:
                    content = f.read()
                    print("\nFile content:")
                    speak("reading file content. "+content)
            else:
                speak("File not found. Here are the available files:")
                # Print the list of available files with words
                for i, file in enumerate(txt_files, start=1):
                    print(f"{number_to_word(i)}. {file}")
                    speak(f"select {number_to_word(i)} for {file}")
                
                # Allow the user to select a file by word
                listen.play_sound("00ad0b6b04e9c50c53d2c2a8da552a37.wav")
                time.sleep(0.5)
                listen.stop_sound()
                choice = listen.recognize_text().strip().lower()
                word_to_number = {
                'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
                'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
                'nineteen': 19, 'twenty': 20, 'twenty-one': 21, 'twenty-two': 22,
                'twenty-three': 23, 'twenty-four': 24, 'twenty-five': 25,
                'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28,
                'twenty-nine': 29, 'thirty': 30, 'thirty-one': 31, 'thirty-two': 32,
                'thirty-three': 33, 'thirty-four': 34, 'thirty-five': 35,
                'thirty-six': 36, 'thirty-seven': 37, 'thirty-eight': 38,
                'thirty-nine': 39, 'forty': 40, 'forty-one': 41, 'forty-two': 42,
                'forty-three': 43, 'forty-four': 44, 'forty-five': 45,
                'forty-six': 46, 'forty-seven': 47, 'forty-eight': 48,
                'forty-nine': 49, 'fifty': 50
                }
            
                if choice in word_to_number:
                    index = word_to_number[choice] - 1
                    if 0 <= index < len(txt_files):
                        selected_file = txt_files[index]
                        file_path = os.path.join(directory, selected_file + '.txt')
                        # Open and read the selected file
                        with open(file_path, 'r') as f:
                            content = f.read()
                            print("\nFile content:")
                            speak("file content. "+content)
                    else:
                        speak("Invalid selection. Please try again.")
                else:
                    speak("Invalid choice. Please select a valid file word.")
    
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def number_to_word(num):
        """Convert a number to its corresponding word representation (1-50)."""
        words = [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
        "eighteen", "nineteen", "twenty", "twenty-one", "twenty-two", "twenty-three",
        "twenty-four", "twenty-five", "twenty-six", "twenty-seven", "twenty-eight",
        "twenty-nine", "thirty", "thirty-one", "thirty-two", "thirty-three", "thirty-four",
        "thirty-five", "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine",
        "forty", "forty-one", "forty-two", "forty-three", "forty-four", "forty-five",
        "forty-six", "forty-seven", "forty-eight", "forty-nine", "fifty"
        ]
        return words[num - 1] if 1 <= num <= 50 else None

    def delete_file(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting file '{file_path}': {e}")
            return False

    def append_to_file(file_path, text_to_append):
        try:
            with open(file_path, "a") as file:
                file.write(text_to_append)
            return True
        except Exception as e:
            print(f"Error appending text to file '{file_path}': {e}")
            return False

    # def generate_response(prompt):
    #     co = cohere.Client('06VmiYLbJrwIF5NVDbfltjdQzmXMbYAWyb2wU232')
    #     response = co.generate(
    #         model='command-xlarge-nightly',
    #         prompt=prompt,
    #         max_tokens=100
    #     )
    #     return response.generations[0].text.strip()
    
    def generate_response(prompt):
        try:
            # Initialize the Cohere client
            co = cohere.Client('06VmiYLbJrwIF5NVDbfltjdQzmXMbYAWyb2wU232')
        
            # Generate a response from the Cohere API
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=100
            )
        
            # Return the generated text
            return response.generations[0].text.strip()
    
        except Exception as e:
            # If an error occurs, return a custom error message
            return "Could not respond to request"



    def run_gui():
        global root
        root = tk.Tk()
        root.title("Linda Voice Assistant")
        root.attributes('-topmost', True)
        root.geometry("600x400")

        # Set background and top bar color
        root.configure(bg='#333333')
        root.option_add("*TFrame*Background", "#333333")
        root.option_add("*TLabel*Foreground", "white")

        # Create a text box for displaying the conversation
        global text_display
        text_display = tk.Text(root, bg='#333333', fg='white', font=("Helvetica", 14), wrap=tk.WORD, state=tk.DISABLED)
        text_display.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Make the window icon and topbar black with white text (if supported by OS)
        icon_image = tk.PhotoImage(file='3378034.png')
        root.iconphoto(False, icon_image)

        # Start listening for commands
        threading.Thread(target=listen_commands, daemon=True).start()
        speak("Hello, my name is Linda, your voice assistant. What would you like me to do?")
        root.mainloop()

    
    run_gui()  # Ensure GUI is set up before speaking
    

# Call the function to run the assistant
#run_linda_voice_assistant()
