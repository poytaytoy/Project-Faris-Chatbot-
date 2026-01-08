import azure.cognitiveservices.speech as speechsdk
from secrets import token_hex
import wave 
from dotenv import load_dotenv
import os 

load_dotenv()

client = os.environ.get("AZURE_SPEECH_KEY")
region = os.environ.get("AZURE_REGION")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audioResult")

def processCode(text):
    currentText:str = text
    locations = []
    index = currentText.find('```')
    coordinates = []
    while index != -1:
        if len(coordinates) == 0: 
            coordinates.append(index + (len(text) - len(currentText)))
        else:
            coordinates.append(index + (len(text) - len(currentText) + 2))
            locations.append((coordinates[0], coordinates[1]))
            coordinates = []
        currentText = currentText[index + 1:]
        index = currentText.find('```')
    textLocations = []
    previousEnd = 0
    if len(locations) == 0:
        return text
    else:
        for i1, i2 in locations:
            textLocations.append(text[previousEnd:i1])
            previousEnd = i2 + 1
        textLocations.append(text[previousEnd: ])
    return ''.join(textLocations)

def generateVoice(text, sentiment = None):
    speech_config = speechsdk.SpeechConfig(subscription=client, region=region)
    
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
    )

    token = token_hex(16)
    file_path = os.path.join(AUDIO_DIR, f"{token}.wav")
    
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
    ssml_string = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='en-US-AshleyNeural'><prosody pitch='+13%' rate='+6%'>{text}</prosody></voice></speak>"
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    try:
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()
        
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            if result.reason == speechsdk.ResultReason.Canceled:
                print(f"Azure Error: {result.cancellation_details.error_details}")
            return None, 0
            
    finally:
        del speech_synthesizer
        
    with wave.open(file_path, 'rb') as wave_file:
        length = wave_file.getnframes() / float(wave_file.getframerate())
    
    return token, length