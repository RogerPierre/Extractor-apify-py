from main import *
from main.Middler.Aplication.apify import extract_comments


request= extract_comments("Token_apify", "Task_id", ["url1", "url2"])
print(request)