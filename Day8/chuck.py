import pyjokes

# Récupère une blague aléatoire (catégorie "chuck")
joke = pyjokes.get_joke(category="chuck")

print("Here is a Chuck Norris fact:")
print(joke)
