# main/useCases/search_use_case.py

from typing import List, Dict, Any, Optional
import logging

from main.ports.IServices.apify_service import ApifyService

logger = logging.getLogger(__name__)

class SearchUseCase:
    """Caso de uso para busca de comentários."""

    def __init__(self, apify_service: ApifyService):
        self.apify_service = apify_service

    def execute(self, post_url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Executa a busca de comentários para um post do Instagram.

        Args:
            post_url: URL do post

        Returns:
            Lista de comentários ou None se erro
        """
        # Preparar input para o actor
        input_data = {
            "postUrls": [post_url],
            "resultsLimit": 100  # Limite de resultados
        }

        # Executar actor
        run_id = self.apify_service.run_actor(input_data)
        if not run_id:
            return None

        # Aguardar conclusão
        if not self.apify_service.wait_for_completion(run_id):
            return None

        # Obter resultados
        results = self.apify_service.get_run_results(run_id)
        return results