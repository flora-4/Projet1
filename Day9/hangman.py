import random
import sys
#from english_words import english_words_lower_set
def my_word():
    # Vérifier qu'on a bien donné un fichier
    if len(sys.argv) < 2:
       print("Error: missing argument (please provide a word list file)")
       sys.exit(1)

    script = sys.argv[1]

    # Lire les mots depuis le fichier
    with open(script, "r") as f:
         words = [line.strip() for line in f if line.strip().isalpha()]

    # Choisir un mot au hasard
    chosen_word = random.choice(words)
    return chosen_word

def game():
    #chosen_list=["morning","python","code","work"]
    #choose a random word from my list
    #chosen_word=random.choice(list(english_words_lower_set))
    chosen_word = my_word()
    # Masquer le mot avec des "_"
    hidden_word = ["_"] * len(chosen_word)

    penalty = 0
    max_penalty = 12

    print("You must guess the word:", " ".join(hidden_word))
    # Boucle principale
    while penalty <= max_penalty:
        input_chosen_word = input("Enter a letter or a word: ").lower()

        if not input_chosen_word.isalpha():
            print(" Just enter letters.")
            continue

        # Cas mot complet
        if len(input_chosen_word) > 1:
            if input_chosen_word == chosen_word:
                print(f"Congratulations, you found it: {chosen_word}")
                return
            else:
                penalty += 5
                print(f" Wrong word! Penalties: {penalty}/{max_penalty}")

        # Cas lettre
        else:
            if input_chosen_word in chosen_word:
                print(f" Letter '{input_chosen_word}' found!")

                # Remplacer toutes les occurrences de la lettre
                for i, letter in enumerate(chosen_word):
                    if letter == input_chosen_word:
                        hidden_word[i] = input_chosen_word

            else:
                penalty += 1
                print(f" Wrong letter! Penalties: {penalty}/{max_penalty}")

        # Afficher l'état actuel du mot
        print(" ".join(hidden_word))

        # Vérifier si le mot est complètement trouvé
        if "".join(hidden_word) == chosen_word:
            print(f"You win! The word was '{chosen_word}'.")
            return

    # Si trop de pénalités
    print(f"Game over! Too many penalties. The word was '{chosen_word}'.")
# Lancer le jeu

while True:
    game()
    again = input("Do you want to play again? (y/n): ").lower()
    if again != "y":
        print("Thanks for playing!")
        break
