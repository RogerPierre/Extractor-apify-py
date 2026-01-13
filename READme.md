# Extractor-Apify-Py

Um projeto Python para extração de comentários de posts do Instagram utilizando a plataforma Apify, seguindo os princípios da Clean Architecture.

## Funcionalidades

- **Extração de Comentários do Instagram**: Utiliza o actor `apify/instagram-comment-scraper` para coletar comentários de posts públicos do Instagram.
- **Arquitetura Limpa**: Implementado com separação de responsabilidades em camadas (Controller, UseCase, Ports/Adapters).
- **Salvamento Seguro**: Os resultados são salvos em arquivos TXT com nomes criptografados (SHA256) para proteger a privacidade.
- **Organização de Arquivos**: Todos os resultados ficam na pasta `results/`, que é ignorada pelo Git.
- **Flexibilidade**: Suporte a múltiplas execuções com nomes de arquivos únicos baseados em URL e timestamp.

## Estrutura do Projeto

```
Extractor-Apify-Py/
├── main/
│   ├── __init__.py
│   ├── app.py                    # Ponto de entrada principal
│   ├── controll/
│   │   ├── __init__.py
│   │   └── search_controller.py  # Controlador da aplicação
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   └── search_interfaces.py  # Interfaces abstratas
│   │   └── IServices/
│   │       ├── __init__.py
│   │       └── apify_service.py   # Adaptador para Apify
│   └── useCases/
│       ├── __init__.py
│       └── search_use_case.py     # Caso de uso para busca
├── Docs/
│   └── diagrams/
│       └── Request.puml           # Diagrama da arquitetura
├── results/                       # Pasta para arquivos de saída (ignorada pelo Git)
├── requirements.txt               # Dependências Python
├── .gitignore                     # Arquivos ignorados pelo Git
└── README.md                      # Este arquivo
```

## Pré-requisitos

- Python 3.8 ou superior
- Conta no Apify com API Token válida
- Acesso a posts públicos do Instagram

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Extractor-Apify-Py.git
   cd Extractor-Apify-Py
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Obtenha seu API Token do Apify em [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations).

2. No arquivo `main/app.py`, substitua `'your_apify_api_token'` pelo seu token real:
   ```python
   API_TOKEN = 'seu_token_aqui'
   ```

## Uso

1. Execute o script principal:
   ```bash
   python main/app.py
   ```

2. O script irá:
   - Solicitar ou usar uma URL de post do Instagram (atualmente configurada para um exemplo).
   - Executar o actor do Apify para extrair comentários.
   - Salvar os comentários em um arquivo TXT criptografado na pasta `results/`.

### Exemplo de Saída

Os comentários são salvos em um arquivo como `results/abc123def456.txt` com o seguinte formato:

```
Comentário: Texto do comentário aqui
Autor: nome_do_usuario
Data: 2026-01-03T22:43:43.000Z
--------------------------------------------------
```

## Arquitetura

O projeto segue a Clean Architecture:

- **Entities**: Interfaces e modelos de dados.
- **Use Cases**: Lógica de negócio (SearchUseCase).
- **Interface Adapters**: Adaptadores para serviços externos (ApifyService).
- **Frameworks & Drivers**: Camada externa (Controller, Apify Client).

### Diagrama

Consulte o diagrama em `Docs/diagrams/Request.puml` para visualizar o fluxo de dados.

## Segurança

- Nomes de arquivos criptografados com SHA256 para evitar identificação fácil.
- Pasta `results/` ignorada pelo Git para não expor dados sensíveis.
- Uso de tokens de API para autenticação segura.

## Limitações

- Funciona apenas com posts públicos do Instagram.
- Requer conta paga no Apify para uso extensivo.
- Limitação de 100 comentários por execução (configurável).

## Contribuição

1. Fork o projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Para dúvidas ou problemas, abra uma issue no GitHub ou entre em contato com o mantenedor.
