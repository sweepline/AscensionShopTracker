#!/usr/bin/env python3

import json
import argparse
import requests

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-f", "--from_file", action="store_true")
parser.add_argument("-o", "--output", action="store")
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
    items_id_dict = {item["items"][0]["item_id"]: item for item in items_list}
    discount_items = {
        ditem["id"]: ditem["discount_price"]
        for ditem in data["shop"]["discount"][0]["items"]
    }
    # List discount prices

    indent = 0

    output = "data.lua"
    if args.output is not None:
        output = args.output
    with open(output, "w") as f:
        f.write("local N, NS = ...\n")
        f.write("\n")
        f.write("local data = {\n")
        indent += 1
        for item in items_id_dict.values():
            id = item["id"]
            name = item["name"]
            item_id = item["items"][0]["item_id"]
            item_price = item["dp_price"]
            f.write(indent * "\t")
            f.write(f"[{item_id}]={{")
            f.write(f"id={id}, ")
            f.write(f'name="{name}", ')
            f.write(f"item_id={item_id}, ")
            f.write(f"item_price={item_price}, ")
            if id in discount_items:
                f.write(f"discount_price={discount_items[id]}, ")
            f.write("},\n")
        indent -= 1
        f.write("}\n")
        f.write("\n")
        f.write("NS.data = data")

if __name__ == "__main__":
    main()
