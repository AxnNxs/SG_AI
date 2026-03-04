import requests
import ollama

def load_charm(file):
    """Legge il contenuto del Modelfile e lo pulisce per Python."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Opzionale: Se vuoi estrarre solo il testo dentro le virgolette di SYSTEM
            # ma per semplicità passiamo tutto il file come contesto iniziale
            return content
    except FileNotFoundError:
        print(f"Error: file {file} not found!")
        return "Online."

def promptGen():
    # L'IA locale risponde
    system_prompt = load_charm('characterStella.mf')
    req = [{'role': 'system', 'content': system_prompt}]
    print("\n--- Stella Online ---\n")

    while(True):
        user_input = input("\nTu: ")

        if not user_input: # Se premi invio senza scrivere nulla
            continue
        if user_input.lower() in ['exit', 'q', 'quit']:
            print("\nStella: Cya!\n")
            break

        req.append({'role': 'user', 'content': user_input})
    
        try:
            ans = ollama.chat(model='Stella', messages = req)
            #req.append(ans)
            textAI = ans.message.content
            print(f"\nStella: {textAI}")
            req.append({'role': 'assistant', 'content': textAI})

            if "Adios!" in textAI:
                break

        except Exception as e1:
            print(f"Error during generation: {e1}")

    #return req['message']['content']



def imageGen(visualPrompt):
    # Chiama l'interfaccia di Stable Diffusion (Forge)/Blue Dolphin via API
    payload = {"prompt": visualPrompt, "steps": 25}
    response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
    # Qui salveresti l'immagine su disco...
    print("Image generation complete!")




# Qui estrarresti il prompt e chiameresti image...
if __name__ == "__main__":
    promptGen()