import json
import os

def parse_company_list(path: str, filename: str):
    abs_path = os.path.dirname(__file__).replace('/', '\\')
    abs_path = os.path.join(abs_path, path, filename)
    with open(abs_path, 'r', encoding='utf-8') as f:
        item_list = dict()
        for item in f.readlines():
            key = item.split()[1]
            value = item.split()[0]
            item_list[key] = value
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(item_list))


parse_company_list('Listed-company', 'comprehensive.txt')