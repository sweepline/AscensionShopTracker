#!/usr/bin/env python3

import json
import argparse
import requests

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-f", "--from_file", action="store_true")
# parser.add_argument("-b", "--branch", help="e.g. master", required=True)
parser.add_argument("username")
parser.add_argument("password")


def data_from_server(username, password):
    # LOGIN
    login_data = {"email": username, "password": password, "code": ""}
    r = requests.post(
        "https://api.ascension.gg/api/user/auth",
        data=json.dumps(login_data),
        headers={
            "Host": "api.ascension.gg",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://ascension.gg",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://ascension.gg/",
        },
    )
    if r.status_code != 200:
        print("Login failed")
        return None

    access_token = r.json()["access_token"]

    # GET BOOTSTRAP
    # Luckily the ascension server just send you the data for everything in a big json blob
    r = requests.get(
        "https://api.ascension.gg/api/bootstrap",
        headers={
            "Host": "api.ascension.gg",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "X-Socket-Id": "736141940.153696573",
            "Authorization": "Bearer " + access_token,
            "Origin": "https://ascension.gg",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://ascension.gg/",
        },
    )

    if r.status_code != 200:
        print("Fetching store data failed")
        return None

    return r.json()


# r = requests.post('https://httpbin.org/post', data={'key': 'value'})
def main() -> None:
    args = parser.parse_args()

    # Implement some kind of caching, we don't need new information until there is new discounts

    if args.from_file:
        print("Loading from data.json")
        f = open("data.json")
        data = json.load(f)
        f.close()
    else:
        print("Loading ascension servers")
        data = data_from_server(args.username, args.password)
    if data == None:
        print("Failed to get data from ascension servers")
        return

    # print(json.dumps(data["shop"]["item"]["items"], indent=2, sort_keys=False))
    items_list = data["shop"]["item"]["items"]
    items_dict = {item["id"]: item for item in items_list}

    # List discount prices
    for discount_item in data["shop"]["discount"][0]["items"]:
        if discount_item["id"] not in items_dict:
            print(f"Item {discount_item['id']} was not found")
            continue
        item = items_dict[discount_item["id"]]
        original_price = item["dp_price"]
        sale_price = discount_item["discount_price"]
        discount = ((original_price - sale_price) / original_price) * 100
        print(
            f"'{item['name']}' is on sale for {sale_price}dp ({discount:.1f}% discount)"
        )


if __name__ == "__main__":
    main()
