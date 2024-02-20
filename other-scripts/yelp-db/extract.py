import requests
import json
import boto3
from datetime import datetime


def get_response(locatoin, cuisine, offset):
    url = (
        f"https://api.yelp.com/v3/businesses/search?location={location}"
        "&categories=restaurant&categories={cuisine}&sort_by=best_match&limit=40&offset="
    )

    url += str(offset)

    headers = {
        "Authorization": "Bearer Pvu0UtMYTXeu7e7DBnPl8GW5tOoR76OWmxzpqbQJiyvKuqQxb1OggRCo7bXlvvCgTfrD2KRN_K-KMfdlDkFHbog-hN7xM7pKn0k31zcN5iyDZn30k5O5JCfzFtzKZXYx",
        "accept": "application/json",
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        return None


def extract_restaurants(response, cuisine):
    values = response["businesses"]
    restaurants = []
    for value in values:
        id = value.get("id", None)
        name = value.get("name", None)
        if id is not None and name is not None:
            resturant = {"id": id, "name": name}
            location = value.get("location", None)
            if location:
                address = location.get("display_address", None)
                zip_code = location.get("zip_code", None)
            rating = value.get("rating", None)
            review_count = value.get("review_count", None)
            coordinates = value.get("coordinates", None)
            categories = value.get("categories", None)

            if coordinates:
                longitude = coordinates.get("longitude", None)
                latitude = coordinates.get("latitude", None)
            if location:
                resturant["address"] = address
                resturant["zip_code"] = zip_code
            if coordinates:
                resturant["coordinates"] = {
                    "longitude": longitude,
                    "latitude": latitude,
                }
            if rating:
                resturant["rating"] = rating
            if review_count:
                resturant["review_count"] = review_count
            good_categories = False
            if categories:
                names = []
                for c in categories:
                    if c.get("title", None):
                        name = c["title"]
                        if cuisine.lower() in name.lower():
                            names.append(name)
                if len(names) > 0:
                    resturant["categories"] = names
                    restaurants.append(resturant)
    return restaurants


def put_items(client, resturants: list):
    log_file = open("yelp-db/insert-names.log", "a")
    for restaurant in resturants:
        # print(f"Constructing restaurant:\n{restaurant}")
        item = {
            "id": {"S": restaurant["id"]},
            "name": {"S": restaurant["name"]},
            "insertedAtTimestamp": {
                "S": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            },
        }
        if restaurant.get("address", None):
            item["address"] = {"L": []}
            for line in restaurant["address"]:
                item["address"]["L"].append({"S": line})
        if restaurant.get("zip_code", None):
            item["zip_code"] = {"S": restaurant["zip_code"]}
        if restaurant.get("coordinates"):
            item["coordinates"] = {
                "M": {
                    "longitude": {
                        "N": str(restaurant["coordinates"].get("longitude", None))
                    },
                    "latitude": {
                        "N": str(restaurant["coordinates"].get("latitude", None))
                    },
                }
            }
        if restaurant.get("review_count", None):
            item["review_count"] = {"N": str(restaurant["review_count"])}
        if restaurant.get("rating", None):
            item["rating"] = {"N": str(restaurant["rating"])}
        if restaurant.get("categories", None):
            item["categories"] = {"L": []}
            for c in restaurant["categories"]:
                item["categories"]["L"].append({"S": c})
        # print(f"Inserting item:\n {item}")
        try:
            client.put_item(
                TableName="yelp-restaurant",
                Item=item,
                ConditionExpression="attribute_not_exists(id)",
            )
            log_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": ")
            log_file.write(f"Inserted: {item['id']['S']}, {item['name']['S']}\n")
        except:
            log_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": ")
            log_file.write(
                f"Abandoned: {item['id']['S']}, {item['name']['S']}, already inserted\n"
            )


if __name__ == "__main__":
    location = "union square, new york"
    cuisines = ["Indian", "Japanese", "Chinese"]
    client = boto3.client("dynamodb")
    for cuisine in cuisines:
        # result = []
        offset = 0
        count = 0
        while count < 20:
            response = get_response(locatoin=location, cuisine=cuisine, offset=offset)
            if response:
                restaurants = extract_restaurants(response=response, cuisine=cuisine)
                count += len(restaurants)
                # result += restaurants
                put_items(client=client, resturants=restaurants)
                offset += 40
            else:
                print("No response")
        # print(result)
        print(f"Finished search for: {cuisine}")