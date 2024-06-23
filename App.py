import openai
from pathlib import Path
import pygame
import speech_recognition as sr
import os
import warnings

warnings.filterwarnings('ignore')

# Definir a chave API diretamente no código

openai.api_key = "" # API DA OPENAI

# Iniciar Voz

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def transcribe(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcription.text

def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )
    output_path = Path(__file__).parent / "output.mp3"
    response.stream_to_file(output_path)
    play_audio(output_path)
    os.remove(output_path)

# Prompt Padrão com Informações

def get_completion(text):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
          {"role": "system", "content": "Vc e uma ia sem genero definido além de ser muito gente boa fala coisas pequenas"},
          {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela do console
        print("Olá, me chamo Carlinhos qualquer dúvida estou aqui para ajudar.")
        print()
        
        print("Por favor, Pergunte algo.")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Capturando voz...")
            audio = recognizer.listen(source)

        file = "input.wav"
        with open(file, "wb") as f:
            f.write(audio.get_wav_data())

        try:
            transcription = transcribe(file)
            print(f"Transcrição: {transcription}")

            completion = get_completion(transcription)
            print(f"Resposta: {completion}")

            text_to_speech(completion)

        except Exception as e:
            print(f"Erro ao transcrever o áudio: {e}")
        finally:
            os.remove(file)

        input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
