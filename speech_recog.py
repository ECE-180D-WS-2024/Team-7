import speech_recognition as sr

#Helper function to extract keywords from a list
#Takes in a list, the words to parse, and a list of keywords
#Outputs a list containing only the keywords in the original list
def extract_keywords(word_list, keywords):
    extracted_keywords = [word for word in word_list if any(keyword in word for keyword in keywords)]
    return extracted_keywords

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
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=2)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    #TODO: process the transcription, and remove anything that isnt a valid input
    #TODO: count the occurance of each valid commands, and return only a one word string of the most frequent command
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
        words_parsed = extract_keywords(raw_words.split(), available_commands)
        #take the mode of the commands, and replace transcription with the command
        if (words_parsed):
            response["transcription"] = max(set(words_parsed), key=words_parsed.count)
        else:
            #response["error"] = "Words detected, but no commands. Original input was:\n" + raw_words
            response["error"] = "Words detected, but no commands. Parsed input was:\n" + str(words_parsed)

    return response

if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #TODO: the speech recognizer accepts input indefinitely until you stop talking. we want to sample periodically, with predetermined limits.
    #DONE.
    #TODO: one word prompts don't work as well as short phrases. also, letters like "A" or "B" are not understood. also, "right" is not picked up very well.
    #Considering a different speech recognizer, or training our own classifier that classifies specifically into the predetermined commands ("right", "left", etc.)

    game_info = {
        "game": "Pokemon",
        "available_commands": ["right", "left", "up", "down"]
    }

    while True:
        print('Accepting new input:')
        guess = recognize_speech_from_mic(recognizer, microphone, game_info["available_commands"])

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
        else:
            print("You said: {}".format(guess["transcription"]))