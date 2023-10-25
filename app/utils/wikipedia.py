import requests
import json


BASE_URL = "https://fr.wikipedia.org/wiki/"


def get_random_wikipedia_title():
    endpoint = "https://fr.wikipedia.org/w/api.php"
    parameters = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 0,
        "rnlimit": 1,
        "rnfilterredir": "nonredirects",
    }

    response = requests.get(endpoint, params=parameters)
    data = response.json()

    if (
        "query" in data
        and "random" in data["query"]
        and len(data["query"]["random"]) > 0
    ):
        return data["query"]["random"][0]["title"]
    else:
        return None


def get_article_details(title):
    endpoint = "https://fr.wikipedia.org/w/api.php"

    parameters_excerpt = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "exsentences": 1,
    }

    parameters_categories = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "categories",
        "cllimit": 5,
    }

    excerpt_data = requests.get(endpoint, params=parameters_excerpt).json()
    categories_data = requests.get(endpoint, params=parameters_categories).json()

    page_id = list(excerpt_data["query"]["pages"].keys())[0]
    excerpt = excerpt_data["query"]["pages"][page_id]["extract"]

    categories = []
    if "categories" in categories_data["query"]["pages"][page_id]:
        for cat in categories_data["query"]["pages"][page_id]["categories"]:
            categories.append(cat["title"].replace("Catégorie:", ""))

    article_url = BASE_URL + title.replace(" ", "_")

    return {
        "title": title,
        "description": excerpt,
        "categories": categories,
        "url": article_url,
    }
