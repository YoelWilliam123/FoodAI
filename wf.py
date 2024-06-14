import streamlit as st
import requests

# Function to fetch recipes
def fetch_recipes(ingredients, diet=None, health=None, cuisineType=None, mealType=None, dishType=None, calories=None, time=None, fiber=None, carbohydrates=None):
    # API parameters
    app_id = "903653a3"
    app_key = "bc27882e315d7266b451c6fbd3dbea7e"
    base_url = "https://api.edamam.com/search"
    query = " ".join(ingredients)

    # Construct the parameters dictionary
    params = {
        "q": query,
        "app_id": app_id,
        "app_key": app_key,
    }

    # Add filters if they are provided
    if diet:
        params["diet"] = diet
    if health:
        params["health"] = health
    if cuisineType:
        params["cuisineType"] = cuisineType
    if mealType:
        params["mealType"] = mealType
    if dishType:
        params["dishType"] = dishType
    if calories:
        params["calories"] = calories
    if time:
        params["time"] = time
    if fiber:
        params["nutrients[FIBTG]"] = fiber
    if carbohydrates:
        params["nutrients[CHOCDF]"] = carbohydrates

    response = requests.get(base_url, params=params)
    data = response.json()

    return data.get("hits", [])

def main():
    # Custom CSS for background image and app icon
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url("");
            background-size: cover;
        }
        .stApp {
            background: url("https://img.freepik.com/premium-photo/healthy-food-heart-dietary-food-black-stone-background-top-view-free-copy-space_187166-48068.jpg?w=740");
            background-size: cover;
        }
        header .icon {
            display: flex;
            align-items: center;
        }
        header .icon img {
            height: 40px;
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set the app icon
    st.markdown(
        """
        <head>
            <link rel="icon" type="image/png" href="https://cdn-icons-png.flaticon.com/512/706/706195.png">
        </head>
        """,
        unsafe_allow_html=True
    )

    st.title("NutRiG")
    st.subheader("Your one stop solution for customized food recommendation")

    with st.expander("Filters"):
        ingredients = st.text_input("Enter ingredients separated by commas (e.g., chicken, rice, tomato)")

        diet_options = [None, "balanced", "high-protein", "high-fiber", "low-fat", "low-carb", "low-sodium"]
        diet = st.selectbox("Select diet type", diet_options)

        health_options = [
            None, "alcohol-free", "celery-free", "crustacean-free", "dairy-free", "egg-free",
            "fish-free", "gluten-free", "kidney-friendly", "kosher", "low-potassium",
            "lupine-free", "mustard-free", "no-oil-added", "low-sugar", "paleo",
            "peanut-free", "pescatarian", "pork-free", "red-meat-free", "sesame-free",
            "shellfish-free", "soy-free", "sugar-conscious", "tree-nut-free", "vegan", "vegetarian",
            "wheat-free"
        ]
        health = st.selectbox("Select health label", health_options)

        cuisine_options = [None, "American", "Asian", "British", "Caribbean", "Central Europe", "Chinese", "Eastern Europe", "French", "Indian", "Italian", "Japanese", "Kosher", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "South American", "South East Asian"]
        cuisineType = st.selectbox("Select cuisine type", cuisine_options)

        meal_options = [None, "Breakfast", "Lunch", "Dinner", "Snack", "Teatime"]
        mealType = st.selectbox("Select meal type", meal_options)

        dish_options = [None, "Alcohol-cocktail", "Biscuits and cookies", "Bread", "Cereals", "Condiments and sauces", "Desserts", "Drinks", "Main course", "Pancake", "Preps", "Preserve", "Salad", "Sandwiches", "Side dish", "Soup", "Starter", "Sweets"]
        dishType = st.selectbox("Select dish type", dish_options)

        calories = st.slider("Select calorie range", 0, 2000, (200, 400))
        time = st.slider("Select cooking time range (minutes)", 0, 120, (10, 30))
        fiber = st.slider("Select fiber range (grams)", 0, 100, (5, 10))
        carbohydrates = st.slider("Select carbohydrate range (grams)", 0, 300, (50, 100))

    if st.button("Find Recipes"):
        if ingredients:
            ingredients_list = [ingredient.strip() for ingredient in ingredients.split(",")]
            recipes = fetch_recipes(ingredients_list, diet, health, cuisineType, mealType, dishType, f"{calories[0]}-{calories[1]}", f"{time[0]}-{time[1]}", f"{fiber[0]}-{fiber[1]}", f"{carbohydrates[0]}-{carbohydrates[1]}")

            if recipes:
                st.write(f"Found {len(recipes)} recipes:")

                for i, recipe in enumerate(recipes):
                    col1, col2 = st.columns(2) if i % 2 == 0 else (st.columns(2)[::-1])
                    with col1:
                        st.image(recipe['recipe']['image'], caption=recipe['recipe']['label'], use_column_width=True)
                    with col2:
                        st.write(recipe['recipe']['label'])
                        st.write(recipe['recipe']['url'])
                        st.write(f"Calories: {recipe['recipe']['calories']:.2f}")
                        st.write(f"Time: {recipe['recipe']['totalTime']} mins")
            else:
                st.write("No recipes found.")
        else:
            st.write("Please enter ingredients.")

if __name__ == "__main__":
    main()
