import json
import os
import requests
from bs4 import BeautifulSoup


def get_something(dom_tree, selector, attribute=None):
    try:
        if attribute:
            return dom_tree.select_one(selector).text.strip()
        
        return dom_tree.select_one(selector).text.strip()
    
    except AttributeError:
        return None

product_code = input("Please enter the product code: ")
# product_code = "129901214"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []

while url:
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        page_done = BeautifulSoup(response.text, 'html.parser')
        opinions = page_done.select("div.js_product-review")
        
        if len(opinions) > 0:

            for opinion in opinions:

                opinion_id = opinion["data-entry-id"]
                author = opinion.select_one("span.user-post__author-name").text.strip()

                try:
                    recommendation = opinion.select_one("span.user-post__author-recommendation > em").text.strip()
                except AttributeError:
                    recommendation = None

                score = opinion.select_one("span.user-post__score-count").text.strip()
                description = opinion.select_one("div.user-post__text").text.strip()
                pros = opinion.select("div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item")
                pros = [p.text.strip() for p in pros]
                cons = opinion.select("div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item")
                cons = [c.text.strip() for c in cons]
                like = opinion.select_one("button.vote-yes > span").text.strip()
                dislike = opinion.select_one("button.vote-yes > span").text.strip()
                publish_date = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"].strip()

                try:
                    purchase_date = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"].strip()
                except AttributeError:
                    purchase_date = None

                single_opinion = {
                    "opinion_id": opinion_id,
                    "author": author,
                    "recommendation": recommendation,
                    "score": score,
                    "description": description,
                    "pros": pros,
                    "cons": cons,
                    "like": like,
                    "dislike": dislike,
                    "publish_date": publish_date,
                    "purchase_date": purchase_date
                }

                all_opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl" + page_done.select_one("a.pagination__next")["href"]
            except TypeError:
                url = None
            print(url)

        else:
            print(f"There are no opinions about product with code {product_code}")
            url = None

if not os.path.exists("opinions"):
    os.mkdir("opinions")
with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)

print(response.status_code)