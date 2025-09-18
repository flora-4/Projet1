import random
import sys
import os
from datetime import datetime

BEST_FILE = "best_scores"

def my_word():
    # Vérifier qu'on a bien donné un fichier
    if len(sys.argv) < 2:
        print("Error: missing argument (please provide a word list file)")
        sys.exit(1)

    script = sys.argv[1]

    # Vérifier que le fichier existe
    if not os.path.exists(script):
        print(f"Error: file '{script}' not found")
        sys.exit(1)

    # Lire les mots depuis le fichier
    with open(script, "r") as f:
        words = [line.strip() for line in f if line.strip().isalpha()]

    if not words:
        print("Error: no valid words in the file")
        sys.exit(1)

    # Choisir un mot au hasard
    chosen_word = random.choice(words)
    return chosen_word.lower()

def get_best_score():
    if not os.path.exists(BEST_FILE):
        return None
    with open(BEST_FILE, "r") as f:
        lines = f.readlines()
        if not lines:
            return None
        # Récupérer le dernier score enregistré
        last_line = lines[-1].strip()
        try:
            parts = last_line.split("attempts: ")
            return int(parts[1])
        except:
            return None

def save_best_score(word, attempts):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BEST_FILE, "a") as f:
        f.write(f"{date} - word: {word} - attempts: {attempts}\n")

def end_game(word, attempts):
    best = get_best_score()
    if best is None or attempts < best:
        save_best_score(word, attempts)
        print(f"Best ever!!! You've guessed \"{word}\" in {attempts} attempts.")
    else:
        print(f"You've guessed \"{word}\" in {attempts} attempts. The record is {best} attempts.")

def game():
    chosen_word = my_word()
    hidden_word = ["_"] * len(chosen_word)

    penalty = 0
    max_penalty = 12
    attempts = 0   # compteur de tentatives

    print("You must guess the word:", " ".join(hidden_word))

    # Boucle principale
    while penalty <= max_penalty:
        input_chosen_word = input("Enter a letter or a word: ").lower()
        attempts += 1  # chaque entrée est une tentative

        if not input_chosen_word.isalpha():
            print(" Just enter letters.")
            continue

        # Cas mot complet
        if len(input_chosen_word) > 1:
            if input_chosen_word == chosen_word:
                print(f"Congratulations, you found it: {chosen_word}")
                end_game(chosen_word, attempts)
                return
            else:
                penalty += 5
                print(f" Wrong word! Penalties: {penalty}/{max_penalty}")

        # Cas lettre
        else:
            if input_chosen_word in chosen_word:
                print(f" Letter '{input_chosen_word}' found!")
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
            end_game(chosen_word, attempts)
            return

    # Si trop de pénalités
    print(f"Game over! Too many penalties. The word was '{chosen_word}'.")
    # Pas de score enregistré si on perd

# Lancer le jeu
while True:
    game()
    again = input("Do you want to play again? (y/n): ").lower()
    if again != "y":
        print("Thanks for playing!")
        break
