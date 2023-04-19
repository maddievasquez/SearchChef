from bs4 import BeautifulSoup
import requests
import json
import mysql.connector
from recipeApp import DATABASES


# This function allows us to extra the links that hold the different recipes that we need to extract
# the information from, as well as taking the tittle from the recipe.
def get_all_links():
    url = "https://www.allrecipes.com/recipes/17057/everyday-cooking/more-meal-ideas/5-ingredients/main-dishes/"
    # Request assist to access the website in which information would be extracted from
    request = requests.get(url)

    # Parse HTML content
    soup = BeautifulSoup(request.text, 'html.parser')

    # Extract tag from div and goes through every single link to extract the title
    div_tag = soup.find("div", {"id": "mntl-taxonomysc-article-list-group_1-0"})
    all_recipes = {}
    for div in div_tag.find_all("div"):
        a_tags = div.find_all("a")
        for a_tag in a_tags:
            all_recipes[(a_tag.find("span", {"class": "card__title"}).getText())] = (a_tag["href"])

    #  parses the information being extracted
    print(json.dumps(all_recipes, indent=4))
    return all_recipes


"""
This function extracts the ingredient list from the link extracted in the get_all_links function
and parses it in a 

"""

def extract_ingredient(recipe_link, recipe_title):
    response = requests.get(recipe_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_ingredients = soup.find_all('li', class_='mntl-structured-ingredients__list-item')
    ingredients = []
    for ingredient in recipe_ingredients:
        ingredient = ingredient.getText().replace("\n", "").strip()
        ingredients.append(ingredient)
    # print(recipe_title)
    return ingredients


def extract_recipe_steps(recipe_link):
    response = requests.get(recipe_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_steps = soup.find('ol', class_='comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup')
    steps = []
    recipe_step_list = recipe_steps.find_all('li')

    for step in recipe_step_list:
        step = step.getText().replace("\n", "").strip()
        steps.append(step)
    for unwanted_tag in recipe_steps:
        remove_tag = soup.find('span')
        remove_tag.decompose()

    # for un_tag in unwanted_tag:
    #     un_tag.figure.decompose()
    return steps


# return {'title': title, 'ingredients': ingredients, 'instructions': instructions}


# mongosh "mongodb+srv://cluster0.hegk7fp.mongodb.net/Cluster0" --apiVersion 1 --username maddie


'''
This block of code was able to store the recipes into mongo bd database however, in order to make 
the requests with Django was a much more complicated process than using MySQL
  client = pymongo.MongoClient(
    "mongodb+srv://maddie:Tymtym272018!@cluster0.hegk7fp.mongodb.net/?retryWrites=true&w=majority")
    db = client.recipe_db
'''

'''
The inserting_recipes function accepts three parameters: title, ingredients, and steps.
 It then establishes a connection to a MySQL database using the credentials specified in the DATABASES dictionary. 
A cursor object is created to execute SQL commands on the database.
'''


def inserting_recipes(title, ingredients, steps):
    mydb = mysql.connector.connect(
        host=DATABASES['default']['HOST'],
        user=DATABASES['default']['USER'],
        database=DATABASES['default']['NAME'],
        password=DATABASES['default']['PASSWORD'],
        consume_results=True
    )
# The function creates a dictionary myrecipedict with the title, ingredients, and steps parameters.
#  This dictionary is likely used to populate a MySQL table with recipe information.

    cursor = mydb.cursor()
    myrecipedict = {
        "title": title,
        "ingredients": ingredients,
        "steps": steps
    }
    recipe_sql = "INSERT ignore INTO recipe (title, image_url) VALUES (%s, %s);"
    val = myrecipedict["title"], ''
    cursor.execute(recipe_sql, val)
    mydb.commit()
    cursor.execute(f'SELECT recipeID from recipe where title = "{title}"')
    recipe_id = cursor.fetchall()[0][0]

    print(recipe_id)
    for ingredient in ingredients:
        ingredient_cursor = mydb.cursor()
        ingredient_sql = "INSERT INTO ingredient (ingredients_text, recipeID) VALUES (%s, %s);"
        val_2 = ingredient, recipe_id
        ingredient_cursor.execute(ingredient_sql, val_2)
        mydb.commit()
        ingredient_cursor.close()

    for step in steps:
        step_cursor = mydb.cursor()
        step_sql = "INSERT INTO STEP (steps_text, recipeID) VALUES (%s, %s);"
        val_3 = step, recipe_id
        step_cursor.execute(step_sql, val_3)
        mydb.commit()
        step_cursor.close()

    cursor.close()


if __name__ == "__main__":
    print(len(""))
    recipe_links = get_all_links()
    for k, v in recipe_links.items():
        title = k
        link = v
        ingredients = extract_ingredient(link, title)
        print("\n")
        steps = extract_recipe_steps(link)
        inserting_recipes(title, ingredients, steps)

# mongodb+srv://maddie:<Tymtym272018!>@cluster0.hegk7fp.mongodb.net/?retryWrites=true&w=majority
