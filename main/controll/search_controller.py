# main/controll/search_controller.py

from typing import List, Dict, Any, Optional
import logging

from main.useCases.search_use_case import SearchUseCase

logger = logging.getLogger(__name__)

class SearchController:
    """Controlador para operações de busca."""

    def __init__(self, search_use_case: SearchUseCase):
        self.search_use_case = search_use_case

    def request_pesquisa(self, post_url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Processa a requisição de pesquisa.

        Args:
            post_url: URL do post do Instagram

        Returns:
            Lista de comentários ou None se erro
        """
        try:
            logger.info(f"Processando requisição para: {post_url}")
            result = self.search_use_case.execute(post_url)
            return result
        except Exception as e:
            logger.error(f"Erro no controlador: {e}")
            return None