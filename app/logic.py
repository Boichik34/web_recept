
def search_recipes_by_category(all_recipes, category):
    recipes = []

    for el in all_recipes:
        if category == el.category:
            recipes.append(el)

    return recipes


def search_recipes_by_keyword(all_recipes, keyword):
    recipes = []

    for el in all_recipes:
        if keyword in el.name:
            recipes.append(el)

    return recipes