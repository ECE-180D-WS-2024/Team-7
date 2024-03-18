import speech_recognition as sr
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/pokemon/test/#", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print("Received message")

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')

client.loop_start()

#Helper function to extract command using keywords from a list
#Takes in a list of tuples, the words to parse, and a list of keywords
#Outputs the command, or None if no keywords are found
def extract_command(word_list, keywords):
    count = [0] * len(keywords)
    for word_said in word_list:
        for i, keyword_tuple in enumerate(keywords):
            for keyword in keyword_tuple:
                if (keyword in word_said.lower()):
                    count[i] += 1
    max_val = max(count)

    if max_val == 0:
        return None
    else:
        return (keywords[count.index(max_val)][0], count.index(max_val))

#Takes in a recognizer and microphone object, and a list of strings of valid commands
#Returns a response dictionary
#If the transcription was successful, detect whether it is a valid commmand
def recognize_speech_from_mic(recognizer, microphone, available_commands):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.energy_threshold = 0
        #recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=2)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None,
        "command_index": 0
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    raw_words = None
    try:
        raw_words = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    #process the transcription
    if (raw_words):
        #remove all words except keyword commands
        command, command_index = extract_command(raw_words.split(), available_commands)
        #take the mode of the commands, and replace transcription with the command
        if (command):
            response["transcription"] = command
            response["command_index"] = command_index
        else:
            response["error"] = "Words detected, but no commands. Original input was:\n" + raw_words


    return response

if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    game_info_pokemon = {
        "name": "pokemon",
        "available_commands": [("right", "riot", "write"), ("left", ), ("up", "pop"), ("down",), ("enter",), ("back",), ("select",)],
        "send_commands": ("Right", "Left", "Up", "Down", "Enter", "Back", "Select")
    }

    game_info_rps = {
        "name": "rps",
        "available_commands": [("rock",), ("paper",), ("scissors",)]
    }

    game_info_list = [game_info_pokemon, game_info_rps]

    mode = "pokemon"

    for game in game_info_list:
        if (game["name"] == mode):
            commands = game["available_commands"]
            send_commands = game["send_commands"]

    while True:
        #recognize_speech function waits 2 seconds while listening
        
        print('Accepting new input:')
        response = recognize_speech_from_mic(recognizer, microphone, commands)

        if response["error"]:
            print("ERROR: {}".format(response["error"]))
        else:
            print("You said: {}".format(response["transcription"]))

            print("Transmitting move to server...\n")
            #client.publish("ece180d/test/turner", send_commands[response["command_index"]], qos=1)

client.loop_stop()
client.disconnect()