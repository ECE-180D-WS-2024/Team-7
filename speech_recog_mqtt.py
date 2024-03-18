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


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect_async('mqtt.eclipseprojects.io')
client.connect("mqtt.eclipse.org")

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
    return None if max_val == 0 else keywords[count.index(max_val)][0]

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
        "transcription": None
    }

    #TODO: could try starting listening at a exact given time, instead of when the microphone energy passes the threshold
    #TODO: look into Snowboy to use a hotword instead of the recgonizer. since we only have one word commands, this may be a useful alternative.

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
        command = extract_command(raw_words.split(), available_commands)
        #take the mode of the commands, and replace transcription with the command
        if (command):
            response["transcription"] = command
        else:
            response["error"] = "Words detected, but no commands. Original input was:\n" + raw_words

    return response

if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #TODO: one word prompts don't work as well as short phrases. also, letters like "A" or "B" are not understood. also, "right" is not picked up very well.
    #Considering a different speech recognizer, or training our own classifier that classifies specifically into the predetermined commands ("right", "left", etc.)

    game_info = {
        "game": "Pokemon",
        "available_commands": [("right", "riot", "write"), ("left", ), ("up", "pop"), ("down",), ("enter",), ("back",)]
    }

    while True:
        input() #press enter in console to listen
        
        print('Accepting new input:')
        guess = recognize_speech_from_mic(recognizer, microphone, game_info["available_commands"])

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
        else:
            print("You said: {}".format(guess["transcription"]))
            print("Transmitting move to server...")

client.loop_stop()
client.disconnect()