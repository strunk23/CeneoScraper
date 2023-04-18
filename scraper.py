import json
import os
import requests
from bs4 import BeautifulSoup


def get_element(dom_tree, selector=None, attribute=None):
    try:
        if attribute:
            if selector:
                return dom_tree.select_one(selector)[attribute].text.strip()
            return dom_tree[attribute]
        return dom_tree.select_one(selector).text.strip()
    
    except (AttributeError, TypeError):
        return None

product_code = input("Please enter the product code: ")
# product_code = "129901214"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []

while url:
    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        page_done = BeautifulSoup(response.text, 'html.parser')
        print(get_element(page_done))
        opinions = page_done.select("div.js_product-review")
        
        if len(opinions) > 0:

            for opinion in opinions:

                opinion_id = opinion["data-entry-id"]
                author = get_element(opinion, "span.user-post__author-name")
                recommendation = get_element(opinion, "span.user-post__author-recommendation > em")
                score = get_element(opinion, "span.user-post__score-count")
                description = get_element(opinion, "div.user-post__text")
                pros = opinion.select("div.review-feature__col:has( > div.review-feature__title--positives) > div.review-feature__item")
                pros = [p.text.strip() for p in pros]
                cons = opinion.select("div.review-feature__col:has( > div.review-feature__title--negatives) > div.review-feature__item")
                cons = [c.text.strip() for c in cons]
                like = get_element(opinion, "button.vote-yes > span")
                dislike = get_element(opinion, "button.vote-yes > span")
                publish_date = get_element(opinion, "span.user-post__published > time:nth-child(1)", "datetime")
                purchase_date = get_element(opinion, "span.user-post__published > time:nth-child(2)", "datetime")

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
                url = "https://www.ceneo.pl" + get_element(page_done, "a.pagination__next", "href")
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