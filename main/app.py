# Projeto: Extractor-Apify-Py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import hashlib
from datetime import datetime

from main.controll.search_controller import SearchController
from main.useCases.search_use_case import SearchUseCase
from main.ports.IServices.apify_service import ApifyService

# Configurações (substitua com suas credenciais)
API_TOKEN = os.getenv('APIFY_API_TOKEN')  # Token Apify via variável de ambiente
ACTOR_ID = 'apify/instagram-comment-scraper'  # Actor para comentários do Instagram

# Instanciar dependências
apify_service = ApifyService(API_TOKEN, ACTOR_ID)
search_use_case = SearchUseCase(apify_service)
controller = SearchController(search_use_case)

# Exemplo de uso
if __name__ == '__main__':
    termo = 'https://www.instagram.com/p/DTB1sMDDYzC/'  # Substitua por uma URL real de post do Instagram
    resultado = controller.request_pesquisa(termo)
    
    print(f"Resultado obtido: {resultado}")  # Debug: imprimir o resultado
    
    # Gerar nome de arquivo criptografado
    hash_input = termo + datetime.now().isoformat()
    hash_object = hashlib.sha256(hash_input.encode())
    nome_arquivo = hash_object.hexdigest() + '.txt'
    caminho_arquivo = f'results/{nome_arquivo}'
    
    # Salvar os dados em um arquivo txt
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        if resultado:
            for item in resultado:
                comentario = item.get('text', item.get('comment', 'N/A'))  # Tentar 'comment' se 'text' não existir
                f.write(f"Comentário: {comentario}\n")
                f.write(f"Autor: {item.get('ownerUsername', item.get('username', 'N/A'))}\n")
                f.write(f"Data: {item.get('timestamp', item.get('date', 'N/A'))}\n")
                f.write("-" * 50 + "\n")
            print(f"Comentários salvos em '{caminho_arquivo}'")
        else:
            f.write("Nenhum comentário encontrado ou erro na busca.\n")
            print("Nenhum resultado encontrado.")