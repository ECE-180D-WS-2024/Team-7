import speech_recognition as sr

#Takes in a recognizer and microphone object, and a list of strings of valid commands
#Returns a response dictionary
#If the transcription was successful, detect whether it is a valid commmand
def recognize_speech_from_mic(recognizer, microphone):
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
        audio = recognizer.listen(source, phrase_time_limit=1)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    #TODO: process the transcription, and remove anything that isnt a valid input
    #TODO: count the occurance of each valid commands, and return only a one word string of the most frequent command

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #TODO: the speech recognizer accepts input indefinitely until you stop talking. we want to sample periodically, with predetermined limits.
    #DONE.
    #TODO: one word prompts don't work as well as short phrases. also, letters like "A" or "B" are not understood. also, "right" is not picked up very well.
    #Considering a different speech recognizer, or training our own classifier that classifies specifically into the predetermined commands ("right", "left", etc.)

    while True:
        print('Accepting new input:')
        guess = recognize_speech_from_mic(recognizer, microphone)

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
        else:
            print("You said: {}".format(guess["transcription"]))