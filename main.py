import openai
import asyncio
# Se vuoi usare le API di Forge per le immagini, tieni requests
import requests
from db_manager import AsyncSessionLocal  # Importa la factory che abbiamo creato
from db_manager import search_relevant_context  # Importa la factory che abbiamo creato
from db_manager import save_to_memory
from embedder import EmbedderService
import os
import logging
import transformers

# Imposta questa variabile prima di importare sentence_transformers o torch
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1" # Mettilo a "1" se non vuoi che cerchi aggiornamenti online
# Disabilita i log di avviso di HuggingFace
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
transformers.logging.set_verbosity_error()

# Configurazione vLLM (Il tuo container Docker
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="vllm-token" # Stringa casuale, vLLM non la controlla
)

def load_charm(file):
    """Legge il contenuto del Modelfile e lo pulisce."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Opzionale: Se vuoi estrarre solo il testo dentro le virgolette di SYSTEM
            # ma per semplicità passiamo tutto il file come contesto iniziale
            return content
    except FileNotFoundError:
        print(f"Error: file {file} not found!")
        return "Online."

async def promptGen():
    # L'IA locale risponde
    print("\n--- Stella Online ---\n")

    embedder = EmbedderService()

    while(True):
        system_prompt = load_charm('characterStella.mf')
        req = [{'role': 'system', 'content': system_prompt}]
        user_input = input("\nTu: ")
        if not user_input: # Se premi invio senza scrivere nulla
            continue
        if user_input.lower() in ['exit', 'q', 'quit']:
            print("\nStella: Cya!\n")
            break

        async with AsyncSessionLocal() as session:
            context = await search_relevant_context(user_input, session, embedder)
            augmented_prompt = f"Contesto: {context}\n\nDomanda: {user_input}"
            # 3. Inviamo solo l'input aumentato a Stella
            # Manteniamo req breve: solo system + ultime 2 coppie di messaggi
            if len(req) > 5:
                req = [req[0]] + req[-4:]

            # Costruisci il prompt con il contesto extra
            req.append({'role': 'user', 'content': augmented_prompt})
        
            try:
                # CORREZIONE: Usa il client OpenAI (che punta a vLLM) invece di ollama
                ans = client.chat.completions.create(
                    model="/app/model",  # Nome del modello definito nel Docker
                    messages=req
                )
                
                # Estrazione corretta della risposta dall'oggetto OpenAI
                textAI = ans.choices[0].message.content
                print(f"\nStella: {textAI}")
                memory_text = f"Utente: {user_input}\nStella: {textAI}"
                vector = embedder.generate_vector(memory_text)
                await save_to_memory(memory_text, vector, session)

                # Aggiorniamo req con la risposta (ma non col contesto RAG, per risparmiare token)
                req.append({'role': 'assistant', 'content': textAI})

                if not "Cya!" in textAI and "Cya" in textAI:
                    break

            except Exception as e1:
                print(f"Errore durante la generazione: {e1}")

    #return req['message']['content']



def imageGen(visualPrompt):
    # Chiama l'interfaccia di Stable Diffusion (Forge)/Blue Dolphin via API
    payload = {"prompt": visualPrompt, "steps": 25}
    response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
    # Qui salveresti l'immagine su disco...
    print("Image generation complete!")




# Qui estrarresti il prompt e chiameresti image...
if __name__ == "__main__":
    asyncio.run(promptGen())