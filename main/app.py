# Projeto: Extractor-Apify-Py
# Script principal para extração de comentários do Instagram usando Apify

import sys
import os
import argparse
import logging
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

# Adicionar o diretório pai ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main.controll.search_controller import SearchController
from main.useCases.search_use_case import SearchUseCase
from main.ports.IServices.apify_service import ApifyService

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Config:
    """Classe para gerenciar configurações da aplicação."""
    def __init__(self):
        self.api_token: Optional[str] = os.getenv('APIFY_API_TOKEN')
        self.actor_id: str = os.getenv('APIFY_ACTOR_ID', 'apify/instagram-comment-scraper')
        self.results_dir: str = os.getenv('RESULTS_DIR', 'results')

        # Validar configurações críticas
        if not self.api_token:
            raise ValueError("APIFY_API_TOKEN não definido. Configure a variável de ambiente.")

    def validate(self) -> None:
        """Valida as configurações."""
        if not self.api_token:
            raise ValueError("Token da API Apify é obrigatório.")
        if not self.actor_id:
            raise ValueError("ID do Actor Apify é obrigatório.")

class InstagramCommentExtractor:
    """Classe principal para extração de comentários do Instagram."""

    def __init__(self, config: Config):
        self.config = config
        self._setup_dependencies()

    def _setup_dependencies(self) -> None:
        """Configura as dependências usando injeção de dependência."""
        try:
            self.apify_service = ApifyService(self.config.api_token, self.config.actor_id)
            self.search_use_case = SearchUseCase(self.apify_service)
            self.controller = SearchController(self.search_use_case)
            logger.info("Dependências configuradas com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao configurar dependências: {e}")
            raise

    def extract_comments(self, post_url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extrai comentários de um post do Instagram.

        Args:
            post_url: URL do post do Instagram

        Returns:
            Lista de comentários ou None se erro
        """
        try:
            logger.info(f"Iniciando extração de comentários para: {post_url}")
            result = self.controller.request_pesquisa(post_url)
            if result:
                logger.info(f"Extraídos {len(result)} comentários.")
                return result
            else:
                logger.warning("Nenhum comentário encontrado.")
                return None
        except Exception as e:
            logger.error(f"Erro durante extração: {e}")
            return None

    def save_comments_to_file(self, comments: List[Dict[str, Any]], post_url: str) -> str:
        """
        Salva os comentários em um arquivo.

        Args:
            comments: Lista de comentários
            post_url: URL do post (usada para gerar nome único)

        Returns:
            Caminho do arquivo salvo
        """
        # Criar diretório se não existir
        os.makedirs(self.config.results_dir, exist_ok=True)

        # Gerar nome de arquivo único baseado na URL e timestamp
        hash_input = post_url + datetime.now().isoformat()
        hash_object = hashlib.sha256(hash_input.encode())
        filename = f"{hash_object.hexdigest()}.txt"
        filepath = os.path.join(self.config.results_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if comments:
                    for item in comments:
                        comment_text = item.get('text') or item.get('comment') or 'N/A'
                        author = item.get('ownerUsername') or item.get('username') or 'N/A'
                        timestamp = item.get('timestamp') or item.get('date') or 'N/A'

                        f.write(f"Comentário: {comment_text}\n")
                        f.write(f"Autor: {author}\n")
                        f.write(f"Data: {timestamp}\n")
                        f.write("-" * 50 + "\n")
                    logger.info(f"Comentários salvos em: {filepath}")
                else:
                    f.write("Nenhum comentário encontrado.\n")
                    logger.info("Arquivo criado com mensagem de nenhum resultado.")
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")
            raise

        return filepath

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Extrator de comentários do Instagram usando Apify')
    parser.add_argument('url', help='URL do post do Instagram')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Carregar configurações
        config = Config()
        config.validate()

        # Inicializar extrator
        extractor = InstagramCommentExtractor(config)

        # Extrair comentários
        comments = extractor.extract_comments(args.url)

        if comments:
            # Salvar em arquivo
            filepath = extractor.save_comments_to_file(comments, args.url)
            print(f"Sucesso! Resultados salvos em: {filepath}")
        else:
            print("Nenhum comentário encontrado.")
            sys.exit(1)

    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        print(f"Erro: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()