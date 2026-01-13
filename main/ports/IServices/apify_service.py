# main/ports/IServices/apify_service.py

import os
import requests
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ApifyService:
    """Serviço para integração com a API do Apify."""

    def __init__(self, api_token: str, actor_id: str):
        self.api_token = api_token
        self.actor_id = actor_id
        self.base_url = "https://api.apify.com/v2"

    def _get_headers(self) -> Dict[str, str]:
        """Retorna os headers para requisições da API."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def run_actor(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Executa um actor no Apify.

        Args:
            input_data: Dados de entrada para o actor

        Returns:
            ID da execução ou None se erro
        """
        url = f"{self.base_url}/acts/{self.actor_id}/runs"
        try:
            response = requests.post(url, json=input_data, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            run_id = data.get("data", {}).get("id")
            logger.info(f"Actor executado com ID: {run_id}")
            return run_id
        except requests.RequestException as e:
            logger.error(f"Erro ao executar actor: {e}")
            return None

    def get_run_results(self, run_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Obtém os resultados de uma execução.

        Args:
            run_id: ID da execução

        Returns:
            Lista de resultados ou None se erro
        """
        url = f"{self.base_url}/actor-runs/{run_id}/dataset/items"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            logger.info(f"Obtidos {len(data)} itens do dataset")
            return data
        except requests.RequestException as e:
            logger.error(f"Erro ao obter resultados: {e}")
            return None

    def wait_for_completion(self, run_id: str, timeout: int = 300) -> bool:
        """
        Aguarda a conclusão da execução.

        Args:
            run_id: ID da execução
            timeout: Timeout em segundos

        Returns:
            True se concluído com sucesso
        """
        import time
        url = f"{self.base_url}/actor-runs/{run_id}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, headers=self._get_headers())
                response.raise_for_status()
                data = response.json()
                status = data.get("data", {}).get("status")

                if status == "SUCCEEDED":
                    logger.info("Execução concluída com sucesso")
                    return True
                elif status in ["FAILED", "ABORTED"]:
                    logger.error(f"Execução falhou com status: {status}")
                    return False

                time.sleep(5)  # Aguardar 5 segundos
            except requests.RequestException as e:
                logger.error(f"Erro ao verificar status: {e}")
                return False

        logger.error("Timeout ao aguardar conclusão")
        return False