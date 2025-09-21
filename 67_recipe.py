import random

# List of ingredients categorized by type
ingredients = {
    "proteins": ["chicken", "beef", "tofu", "salmon", "eggs"],
    "vegetables": ["carrots", "broccoli", "bell peppers", "spinach", "zucchini"],
    "grains": ["rice", "quinoa", "pasta", "couscous", "bread"],
    "fruits": ["apples", "bananas", "berries", "oranges", "mangoes"],
    "dairy": ["cheese", "milk", "yogurt", "butter", "cream"],
    "spices": ["salt", "pepper", "garlic", "cumin", "paprika"]
}

# Function to generate a random recipe
def generate_recipe():
    # Select random ingredients from each category
    protein = random.choice(ingredients["proteins"])
    vegetable = random.choice(ingredients["vegetables"])
    grain = random.choice(ingredients["grains"])
    fruit = random.choice(ingredients["fruits"])
    dairy = random.choice(ingredients["dairy"])
    spice = random.choice(ingredients["spices"])

    # Create a recipe string
    recipe = (
$f"Today's Random Recipe:\n\n"$
$f"Main Ingredient: {protein}\n"$
$f"Vegetable: {vegetable}\n"$
$f"Grain: {grain}\n"$
$f"Fruit: {fruit}\n"$
$f"Dairy: {dairy}\n"$
$f"Spice: {spice}\n\n"$
$f"Instructions:\n"$
$f"1. Cook the {grain} according to package instructions.\n"$
        f"2. Season the {protein} with {spice} and cook it to your desired don
