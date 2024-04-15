import requests
import json
from datetime import datetime

user_liq = 10000
result = []

headers = {
    'accept': 'application/json'
}


def check_and_strip_prefix(s):
    if s.startswith("ton_"):
        return s[4:]
    return s


for page in range(1, 11):
    url = f'https://api.geckoterminal.com/api/v2/networks/ton/new_pools?page={page}'
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    for item in data['data']:
        pool_name = item["attributes"]["name"]
        dex_id = item["relationships"]["dex"]["data"]["id"]
        contract = item["relationships"]["base_token"]["data"]["id"]
        contract = check_and_strip_prefix(contract)
        pool_created_at = item["attributes"]["pool_created_at"]
        readable_date = datetime.fromisoformat(pool_created_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        reserve_in_usd = int(float(item["attributes"]["reserve_in_usd"]))
        if reserve_in_usd > user_liq:
            result.append((pool_name, dex_id, readable_date, reserve_in_usd, contract))

for name, dex, readable_date, reserve_in_usd, contract in result:
    print(f'Jetton: {name}, DEX: {dex}, Date: {readable_date}, Liquidity: {reserve_in_usd}, contract: {contract}')
