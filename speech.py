import speech_recognition as sr
import openai #importa la libreria openai per utilizzare l'API.
import os# importa la libreria os per interagire con il sistema operativo
from gtts import gTTS #importa la classe gTTS dalla libreria gtts per generare file audio a partire da testo.
import pygame# importa la libreria pygame per riprodurre file audio.
pygame.init()
openai.api_key = "INSERISCI API-KEY"
modelloEngine = "text-davinci-003" #  imposta il modello di intelligenza artificiale da utilizzare per generare la risposta.
nomeFile = "risposta.mp3"# il nome del file audio generato.
domanda = ""# domanda da passare al modello di openai
def main():
 
    r = sr.Recognizer()#oggetto Recognizer() che consentirà di rilevare e interpretare il parlato da un flusso audio (ad esempio, un file audio o un segnale in tempo reale da un microfono)
    print("""\nQuesta applicazione ti permette di tradurre le tue parole in tempo reale.
                   Per utilizzarla, seleziona la lingua desiderata e inizia a
                   parlare ad alta voce. Tutto ciò che dici verrà automaticamente
                   tradotto nella lingua selezionata.\n""")
    lingua = input("Inserisci la lingua di destinazione : ") # richiede all'utente di inserire la lingua di destinazione.
    print("\n\nPremi un tasto per iniziare a registrare...")
    input()
    with sr.Microphone() as source:# creo un oggetto microphone e lo assegno alla variabile source. microphone rappresenta il microfono del pc che registrerà.
        os.system("clear")
        r.adjust_for_ambient_noise(source) #adatta il rilevatore alla situazione acustica circostante.
        os.system("clear")
        audio = r.listen(source) # ascolta l'audio dal microfono e lo memorizza nella variabile audio.
        print("Sto traducendo .... ")
        try: #  tenta di riconoscere il parlato dell'utente e gestisce eventuali eccezioni.
            domanda = r.recognize_google(audio, language="it-IT") # utilizza l'API di Google per riconoscere il testo dell'audio.
            domandaTrad = "traduci questo testo in " + lingua + ": " + domanda# crea una stringa che indica la lingua di destinazione e la domanda dell'utente. da passare poi al modello di openai
            completion = openai.Completion.create(# chiama l'API OpenAI per generare una risposta
                    engine = modelloEngine,
                    prompt = domandaTrad,
                    max_tokens = 1024,
                    n= 1,
                    stop = None,
                    temperature = 0.5,#la temperatura influisce sulla coerenza della risposta: più è alta,p più varia ma meno accurata sarà la risposta all'input.
                )
            risposta = completion.choices[0].text #inseriamo la risposta generata in una variabile;
            os.system("clear")
             # Crea l'oggetto gTTS e salva il file audio
            tts = gTTS(text=risposta, lang='en') # viene creato un oggetto gTTS per convertire il testo della risposta in un file audio. Il parametro lang specifica la lingua del testo di origine.
            tts.save(nomeFile) # l'oggetto gTTS salva il file audio con il nome specificato nella variabile nomeFile.
            pygame.mixer.music.load(nomeFile) # questa riga carica il file audio nel mixer di pygame.
            pygame.mixer.music.play() # viene riprodotto il file audio appena caricato.
            while pygame.mixer.music.get_busy():#in questo ciclo while, il programma attende finché il file audio non viene riprodotto completamente.       
                                                #get_busy() restituisce True se il mixer sta riproducendo un suono.
                pygame.time.Clock().tick(10) # fa dormire il programma per 10 millisecondi per evitare di sovraccaricare la CPU.
            print(domanda)
            print(risposta)
 
        except Exception as e:# se si verifica un eccezzione restituisce la descrizione dell eccezione come una stringa
            print("Error :  " + str(e))# restituisce la descrizione dell eccezione come stringa

        with open("recorded.wav", "wb") as f:# apre il file binario recorderd.wav in modalità scrittura
            f.write(audio.get_wav_data())# scrive nel file richiamando il metodo get_wav_data() per ottenere i dati audio in formato wav
 
 
if __name__ == "__main__":
    main()