import myfitnesspal

client = myfitnesspal.Client()

food_items = client.get_food_search_results("bacon cheeseburger")
food_items
# >> [<Bacon Cheeseburger -- Sodexo Campus>,
# <Junior Bacon Cheeseburger -- Wendy's>,
# <Bacon Cheeseburger -- Continental Café>,
# <Bacon Cheddar Cheeseburger -- Applebees>,
# <Bacon Cheeseburger - Plain -- Homemade>,
# <Jr. Bacon Cheeseburger -- Wendys>,
# ...

print("{} ({}), {}, cals={}, mfp_id={}".format(
    food_items[0].name,
    food_items[0].brand,
    food_items[0].serving,
    food_items[0].calories,
    food_items[0].mfp_id
))
# > Bacon Cheeseburger (Sodexo Campus), 1 Sandwich, cals = 420.0