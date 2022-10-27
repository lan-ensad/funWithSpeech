#pip install paho-mqtt gTTS playsound deep-translator

from pickle import TRUE
import paho.mqtt.client as mqtt
import time
from gtts import gTTS
from playsound import playsound
from deep_translator import GoogleTranslator

langage = 'fr'
accent = 'fr'
doTranslate = False
doOriginal = False
mqttBroker ="192.168.0.102"

def speech_msg(msg, langa):
    print(msg)
    sound = gTTS(text=msg, lang=langage, slow=True)
    sound.save("sound.mp3")
    print(langage)
    playsound("sound.mp3")

def on_message(client, userdata, message):
    global doTranslate
    global doOriginal
    global accent
    thespeech = str(message.payload.decode("utf-8"))

    if(doTranslate):
        thespeech = GoogleTranslator(source='auto', target=langage).translate(thespeech)
    
    if(doOriginal):
        speech_msg(thespeech, accent)
    else:
        speech_msg(thespeech, langage)

def anylang(client, userdata, message):
    global langage
    strgen = str(message.payload.decode("utf-8"))
    langage = strgen
    print(strgen)

def set_translate(client, userdata, message):
    global doTranslate
    strgen = str(message.payload.decode("utf-8"))
    if(strgen == "true"):
        doTranslate = True
    else:
        doTranslate = False
    print(strgen)

def playMeme(client, userdata, message):
    toplay = str(message.payload.decode("utf-8"))
    print(toplay)
    #playsound(toplay)

#---------------------------------
#         Clients Setup
client = mqtt.Client("MainMacos")
client.connect(mqttBroker,1883)

client2 = mqtt.Client("anyl")
client2.connect(mqttBroker,1883)

client3 = mqtt.Client("transl")
client3.connect(mqttBroker,1883)

client4 = mqtt.Client("memes")
client4.connect(mqttBroker,1883)

#---------------------------------
#  Clients Connexion & Subscribe
client.loop_start()
client.subscribe("speech")
client.on_message=on_message

client2.loop_start()
client2.subscribe("anylangage")
client2.on_message=anylang

client3.loop_start()
client3.subscribe("translate")
client3.on_message=set_translate

client4.loop_start()
client4.subscribe("meme")
client4.on_message=playMeme

time.sleep(500000)