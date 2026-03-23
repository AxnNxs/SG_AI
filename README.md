# SG_AI
Experimental personality AI focused on cloud systems scalability

Steps:
Execute in this order for first sturtup:
- download IA model from https://huggingface.co/hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4/tree/main and put all files inside your local project in the sequent folder:
"SG_AI/.ai/
- docker-compose up -d <- avvia ambiente ia
- init_db.py <- crea tabelle
- db_manager.py <- popola tabelle da file txt
- docker logs -f ia_vllm <- avvia ia
- main.py <- avvia chat con ia

For further restarts:
- docker-compose up -d <- avvia ambiente ia
- docker logs -f ia_vllm <- avvia ia
- .\cloudflared-windows-amd64.exe tunnel --protocol http2  --url http://localhost:8501 <- apertura indirizzo web temporaneo
- streamlit run web_app.py <- avvia chat con ia con interfaccia web

for customization:
- modify .mf file in runtime
- modify background before docker compose up

Requirements:
Python
Docker
