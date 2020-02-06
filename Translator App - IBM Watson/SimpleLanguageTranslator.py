from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import LanguageTranslatorV3

import keys
import pyaudio #pyaudio module allows us to record audio from the microphone
import pydub #enables us to load and play audio files
import pydub.playback
import wave #enables us to save WAV format

def record_audio(filename):
    #This functions records audio from the mic and saves it in a wav file using pyaudio.
    #We set parameters to configure the stream for 5 seconds of audio.
    #refer to https://people.csail.mit.edu/hubert/pyaudio/docs/ for parameters
    FRAME_RATE=44100 #frames per second, common for CD quality audio
    CHANNELS=2
    FORMAT=pyaudio.paInt16
    CHUNK=1024
    SECONDS=5

    #create a pyaudio object using its default constructor.
    recorder = pyaudio.PyAudio()
    #Use the PyAudio's open method to open a stream for input. The method returns a Stream object.
    #The constructors parameters are given https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.__init__
    #The stream will record in CHUNK=1024 number of frames at a time
    audio_stream = recorder.open(rate=FRAME_RATE, channels=CHANNELS, format=FORMAT, input=True, frames_per_buffer=CHUNK)
    audio_frames = [] #the list of audio frames to store the chunks of frames recorded
    print("Recording audio...")

    for i in range(int(FRAME_RATE * SECONDS/CHUNK)): #we append 5 seconds worth of audio frames
        audio_frames.append(audio_stream.read(CHUNK))

    print("Finished recording.")
    audio_stream.stop_stream()
    audio_stream.close()
    recorder.terminate()

    #open a wave file and save the recorded data to it in binary
    with wave.open(filename, 'wb') as output:
        output.setnchannels(CHANNELS)
        output.setframerate(FRAME_RATE)
        output.setsampwidth(recorder.get_sample_size(FORMAT))
        output.writeframes(b''.join(audio_frames))

def speech_to_text(filename, model_id):
    #create a client
    stt = SpeechToTextV1(iam_apikey=keys.speech_to_text_key)

    #open file for transcribing.
    #the SpeechToTextV1 recognize() method returns a DetailedResponse object: https://cloud.ibm.com/apidocs/speech-to-text/speech-to-text?code=python#response-details
    #we get the JSON of the transcription result
    with open(filename, 'rb') as audio_file:
        response = stt.recognize(audio=audio_file, content_type='audio/wav', model=model_id).get_result()

    #get results
    transcript = response['results'][0]['alternatives'][0]['transcript']
    #return results
    return transcript

def translate_text(input_text, model):
    #create a Watson translator service object
    translatorV3 = LanguageTranslatorV3(iam_apikey=keys.translate_key, version='2018-05-31')

    response = translatorV3.translate(text=input_text, model_id=model).get_result()

    return response['translations'][0]['translation']

def text_to_speech(input_text, model, filename):

    tts = TextToSpeechV1(iam_apikey=keys.text_to_speech_key)

    #open a file for writing. send text to synthesize and result to file
    with open(filename, 'wb') as output_speech:
        output_speech.write(tts.synthesize(text=input_text, accept='audio/wav', voice=model).get_result().content)

def play_audio(filename):

    sound = pydub.AudioSegment.from_wav(filename)
    pydub.playback.play(sound)

def run_translator():
    #We break the program into steps. Each step calls a function that calls necessary Watson services
    #Step 1: Prompt for a question and record into an audio file
    input("Press Enter and asks a question in English")
    record_audio("english.wav")

    #Step 2: Transcribe English audio file into English text
    english_text = speech_to_text("english.wav", "en-US_BroadbandModel")
    ## Print to screen and save question to file for reference
    print(english_text)
    with open("english_transcript.txt", 'w') as output_handle:
        output_handle.write(english_text)

    #Step 3:
    spanish_text = translate_text(english_text, 'en-es')
    print("Spanish Translation of English text:")
    print(spanish_text)

    #Step 4: Synthesize Spanish text into Spanish speech
    text_to_speech(spanish_text, 'es-US_SofiaVoice', 'spanish_speech.wav')

    #Step 5: Play Audio
    play_audio('spanish_speech.wav')

if __name__ == '__main__':
    run_translator()
