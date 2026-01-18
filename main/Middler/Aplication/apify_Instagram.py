from main.Middler.ports.libs import ApifyService
from main.models.interfaces.IInputUrl import IInputUrl
from main.models.IRequests.IRequest import Requisition
from main.models.IRequests.OutputComents import OutputComents
from main.caseUse.services.ApiRequest import InputUrl

import os
import csv
from datetime import datetime
from urllib.parse import urlparse


# Implementação da interface Requisition para Apify


class ApifyRequest(Requisition):
    def __init__(self, api_token: str, task_id: str, input_url: IInputUrl):
        self.client = ApifyService().create_A_Request(api_token)
        self.task_id = task_id
        self.input_url = input_url

    def fetch(self) -> list:
        try:
            request = {
                "directUrls": self.input_url.get_url(),
                "resultsLimit": 150,
                "isNewestComments": True,
            }
            run = self.client.actor(self.task_id).call(run_input=request)
            items = self.client.dataset(run.get("defaultDatasetId"))
            outputs = []
            for item in items.iterate_items():
                outputs.append(item)
            return outputs
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise Exception(f"Ator não encontrado. Verifique se o task_id '{self.task_id}' está correto no Apify. Erro: {e}")
            else:
                raise Exception(f"Erro ao fazer a requisição: {e}")


# Implementação da interface OutputComents
class CommentsParser(OutputComents):
    def _safe_get(self, d: dict, keys):
        for k in keys:
            if k in d:
                return d[k]
            low = k.lower()
            for dk in d.keys():
                if isinstance(dk, str) and dk.lower() == low:
                    return d[dk]
        return None

    def _to_int(self, v):
        try:
            return int(v)
        except Exception:
            return 0

    def parse_comments(self, data: list, source_hint: str | None = None) -> list:
        """
        Retorna lista de dicionários com as chaves:
        'text', 'timestamp', 'author', 'likes', 'replies', 'source'
        """
        comments: list[dict] = []

        def walk(node):
            if node is None:
                return
            if isinstance(node, dict):
                text = self._safe_get(node, ['text'])
                if isinstance(text, (str,)) or isinstance(text, list):
                    texts = [text] if isinstance(text, str) else text
                    for t in texts:
                        if not isinstance(t, str):
                            continue
                        t_str = t.strip()
                        if not t_str:
                            continue

                        timestamp = self._safe_get(node, ['createdAt', 'created_at', 'date', 'timestamp'])
                        author = self._safe_get(node, ['author', 'user', 'username', 'from', 'owner'])
                        if isinstance(author, dict):
                            author = self._safe_get(author, ['name', 'username', 'fullName']) or None
                        likes = self._safe_get(node, ['likeCount', 'likes', 'like_count', 'likes_count'])
                        replies = self._safe_get(node, ['replyCount', 'replies', 'replies_count'])

                        comment = {
                            'text': t_str,
                            'timestamp': timestamp,
                            'author': author,
                            'likes': self._to_int(likes),
                            'replies': self._to_int(replies),
                            'source': source_hint or self._safe_get(node, ['source', 'network']) or None,
                        }
                        comments.append(comment)
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)

        # deduplicar por texto+timestamp+author
        seen = set()
        unique: list[dict] = []
        for c in comments:
            key = (c.get('text'), str(c.get('timestamp')), str(c.get('author')))
            if key not in seen:
                seen.add(key)
                unique.append(c)

        return unique

    def save_comments_csv(self, comments: list[dict], task_id: str, urls: list[str]) -> str:
        os.makedirs('data', exist_ok=True)
        now = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"data/comments_{task_id}_{now}.csv"
        fields = ['text', 'timestamp', 'author', 'likes', 'replies', 'source']

        # determine source hint from urls if missing
        domains = set()
        for u in urls:
            try:
                p = urlparse(u)
                if p.netloc:
                    domains.add(p.netloc.lower())
            except Exception:
                continue
        source_hint = None
        if domains:
            dom = next(iter(domains))
            if 'instagram' in dom:
                source_hint = 'instagram'
            else:
                source_hint = dom

        for c in comments:
            if not c.get('source'):
                c['source'] = source_hint

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for c in comments:
                row = {k: c.get(k) for k in fields}
                writer.writerow(row)

        return filename


# Função principal para extrair comentários e salvar CSV
def extract_comments(api_token: str, task_id: str, url: list[str]) -> list:
    input_url = InputUrl(url)
    request = ApifyRequest(api_token, task_id, input_url)
    data = request.fetch()
    parser = CommentsParser()
    # passamos uma dica de origem com base nas URLs
    source_hint = None
    if url:
        try:
            dom = urlparse(url[0]).netloc.lower()
            if 'instagram' in dom:
                source_hint = 'instagram'
            elif 'facebook' in dom:
                source_hint = 'facebook'
            else:
                source_hint = dom
        except Exception:
            source_hint = None
    if(len(comments)<150):
        raise Exception("Limite de comentários não atingido, verifique se as URLs estão corretas ou se há comentários disponíveis.")
    comments = parser.parse_comments(data, source_hint=source_hint)
    csv_path = parser.save_comments_csv(comments, task_id, url)
    return comments

