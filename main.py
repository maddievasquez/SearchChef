from bs4 import BeautifulSoup
import requests
import json


def get_all_links():
    url = "https://www.allrecipes.com/recipes/17057/everyday-cooking/more-meal-ideas/5-ingredients/main-dishes/"
    # Request assist to access the website in which information would be extracted from
    request = requests.get(url)

    # Parse HTML content
    soup = BeautifulSoup(request.text, 'html.parser')

    # Extract tag from div
    div_tag = soup.find("div", {"id": "mntl-taxonomysc-article-list-group_1-0"})
    all_recipes = {}
    for div in div_tag.find_all("div"):
        a_tags = div.find_all("a")
        for a_tag in a_tags:
            all_recipes[(a_tag.find("span", {"class": "card__title"}).getText())] = (a_tag["href"])

    #  parses the information being extracted
    print(json.dumps(all_recipes, indent=4))
    return all_recipes


# Extracts the ingredients from
# def get_request():

def extract_ingredient(recipe_link, recipe_title):
    response = requests.get(recipe_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_ingredients = soup.find_all('li', class_='mntl-structured-ingredients__list-item')
    ingredients = []
    for ingredient in recipe_ingredients:
        ingredient = ingredient.getText().replace("\n", "").strip()
        ingredients.append(ingredient)
    print(recipe_title)
    print(ingredients)


def extract_recipe_steps(recipe_link):
    response = requests.get(recipe_link)
    soup = BeautifulSoup(response.content,'html.parser')
    recipe_steps = soup.find('ol', class_='comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup')
    steps = []
    recipe_step_list = recipe_steps.find_all('li')
    for step in recipe_step_list:

        step = step.getText().replace("\n", "").strip()
        steps.append(step)
    print(steps)


# return {'title': title, 'ingredients': ingredients, 'instructions': instructions}

if __name__ == "__main__":
    recipe_links = get_all_links()
    for k, v in recipe_links.items():
        title = k
        link = v
    #     extract_ingredient(link, title)
    #     print("\n")
        extract_recipe_steps(link)