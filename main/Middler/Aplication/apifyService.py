from ...caseUse.services.ApiRequest import InputUrl


def extract_comments(api_token: str, task_id: str, url: list[str], api_name: str) -> list:
    input_url = InputUrl(url)

    if api_name.lower() == "instagram":
        from .apify_instagram import ApifyRequestInstagram as Requisition
        from .apify_instagram import CommentsParser as OutputComents
    elif api_name.lower() == "tiktok":
        from .apify_tiktok import ApifyRequestTiktok as Requisition
        from .apify_tiktok import CommentsParser as OutputComents
    request = Requisition(api_token, task_id, input_url)
    data = request.fetch()
    parser = OutputComents()
    # passamos uma dica de origem com base nas URLs
    source_hint = None
    if url:
        try:
            source_hint = api_name.lower()
        except Exception:
            source_hint = None
    # if(len(comments)<150):
    #     raise Exception("Limite de comentários não atingido, verifique se as URLs estão corretas ou se há comentários disponíveis.")
    comments = parser.parse_comments(data, source_hint=source_hint)
    csv_path = parser.save_comments_csv(comments, task_id, url)
    return comments
