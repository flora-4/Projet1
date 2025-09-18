# hangman_pygame.py
# Pendu graphique complet (pygame)
# Usage:
#   python3 hangman_pygame.py [words.txt]
# If no file provided, the program will try to use english_words package (if installed),
# else will fall back to a built-in small list.

import pygame
import sys
import os
import random
from datetime import datetime

# ---------- Configuration ----------
WINDOW_SIZE = (1000, 600)
FPS = 30
BEST_FILE = "best_scores"
DEFAULT_WORDS = ["python","hangman","computer","programming","challenge","apple","banana","developer","keyboard","mouse"]
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# Hints / AI cost in attempts (you can tune)
HINT_PENALTY = 2

# ---------- Utilities ----------
def load_wordlist_from_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip().isalpha()]
    return [w.lower() for w in words]

def load_words_from_args_or_default():
    if len(sys.argv) == 2:
        try:
            words = load_wordlist_from_file(sys.argv[1])
            if not words:
                raise ValueError("File contains no valid words")
            return words
        except Exception as e:
            print("Error reading word file:", e)
            sys.exit(1)
    else:
        # try english_words if available
        try:
            from english_words import english_words_lower_set
            words = [w for w in english_words_lower_set if w.isalpha() and w.islower() and 3 <= len(w) <= 12]
            return list(words)
        except Exception:
            return DEFAULT_WORDS

def get_best_score():
    if not os.path.exists(BEST_FILE):
        return None
    with open(BEST_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return None
    # parse attempts from last line or best line - we'll take minimal attempts in file
    attempts = []
    for line in lines:
        if "attempts:" in line:
            try:
                n = int(line.split("attempts:")[-1].strip())
                attempts.append(n)
            except:
                pass
    return min(attempts) if attempts else None

def save_best_score(word, attempts):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BEST_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date} - word: {word} - attempts: {attempts}\n")

# ---------- Pygame UI helpers ----------
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pendu - Hangman")
clock = pygame.time.Clock()

# fonts
FONT = pygame.font.SysFont("arial", 20)
BIG = pygame.font.SysFont("arial", 34, bold=True)
SMALL = pygame.font.SysFont("arial", 16)

def draw_text(surface, text, pos, font=FONT, color=(255,255,255)):
    r = font.render(text, True, color)
    surface.blit(r, pos)

# ---------- Game logic classes ----------
class Button:
    def __init__(self, rect, label, callback=None, color=(150,120,50)):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.cb = callback
        self.color = color
        self.disabled = False
    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=6)
        draw_text(surf, self.label, (self.rect.x + 8, self.rect.y + 6), font=SMALL)
    def handle_event(self, ev):
        if self.disabled: return
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos) and self.cb:
                self.cb()

class HangmanGame:
    def __init__(self, words, difficulty="medium", time_limit=None):
        self.words = words
        self.difficulty = difficulty
        self.time_limit = time_limit  # seconds or None
        self.reset_round()

    def reset_round(self):
        # choose word according to difficulty
        if self.difficulty == "easy":
            pool = [w for w in self.words if len(w) <= 5]
        elif self.difficulty == "hard":
            pool = [w for w in self.words if len(w) >= 7]
        else:
            pool = self.words
        if not pool:
            pool = self.words
        self.secret = random.choice(pool).lower()
        self.hidden = ["_"] * len(self.secret)
        self.penalty = 0
        self.max_penalty = 12
        self.attempts = 0
        self.used_letters = set()
        self.last_message = ""
        self.start_time = pygame.time.get_ticks()
        self.finished = False
        self.won = False

    def guess(self, text):
        if self.finished:
            return
        text = text.lower().strip()
        if not text or not text.isalpha():
            self.last_message = "Please enter letters only."
            return
        if len(text) > 1:
            # word guess
            self.attempts += 1
            if text == self.secret:
                self.hidden = list(self.secret)
                self.finish(win=True)
            else:
                self.penalty += 5
                self.last_message = f"Wrong word! Penalties: {self.penalty}/{self.max_penalty}"
        else:
            # single letter
            letter = text
            if letter in self.used_letters:
                self.last_message = f"You already tried '{letter}'."
                return
            self.used_letters.add(letter)
            self.attempts += 1
            if letter in self.secret:
                for i,c in enumerate(self.secret):
                    if c == letter:
                        self.hidden[i] = letter
                self.last_message = f"Found letter '{letter}'!"
                if "".join(self.hidden) == self.secret:
                    self.finish(win=True)
            else:
                self.penalty += 1
                self.last_message = f"Wrong letter! Penalties: {self.penalty}/{self.max_penalty}"
        if self.penalty >= self.max_penalty:
            self.finish(win=False)

    def finish(self, win):
        self.finished = True
        self.won = win
        if win:
            # record if best
            best = get_best_score()
            if best is None or self.attempts < best:
                save_best_score(self.secret, self.attempts)
        else:
            # losing: do nothing
            pass

    def time_left(self):
        if self.time_limit is None:
            return None
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
        return max(0, self.time_limit - elapsed)

# ---------- Visuals ----------
def draw_hangman(surface, x, y, wrong):
    # draw gallows
    # base
    pygame.draw.line(surface, (100,60,20), (x-60,y+140), (x+120,y+140), 8)
    pygame.draw.line(surface, (100,60,20), (x-20,y+140), (x-20,y-120), 8)
    pygame.draw.line(surface, (100,60,20), (x-20,y-120), (x+60,y-120), 8)
    pygame.draw.line(surface, (100,60,20), (x+60,y-120), (x+60,y-90), 6)

    # body parts progressive by wrong count
    # 1 head, 2 neck, 3 body, 4 left arm, 5 right arm, 6 left leg, 7 right leg, etc - we have up to 12
    if wrong >= 1:
        pygame.draw.circle(surface, (200,200,200), (x+60,y-60), 20, 3)  # head
    if wrong >= 2:
        pygame.draw.line(surface, (200,200,200), (x+60,y-40), (x+60,y), 3)  # neck
    if wrong >= 3:
        pygame.draw.line(surface, (200,200,200), (x+60,y), (x+60,y+50), 3)  # body
    if wrong >= 4:
        pygame.draw.line(surface, (200,200,200), (x+60,y+10), (x+30,y+30), 3)  # left arm
    if wrong >= 5:
        pygame.draw.line(surface, (200,200,200), (x+60,y+10), (x+90,y+30), 3)  # right arm
    if wrong >= 6:
        pygame.draw.line(surface, (200,200,200), (x+60,y+50), (x+30,y+90), 3)  # left leg
    if wrong >= 7:
        pygame.draw.line(surface, (200,200,200), (x+60,y+50), (x+90,y+90), 3)  # right leg
    if wrong >= 8:
        # eyes cross
        pygame.draw.line(surface, (255,0,0), (x+54,y-66),(x+58,y-62),2)
        pygame.draw.line(surface, (255,0,0), (x+58,y-66),(x+54,y-62),2)
        pygame.draw.line(surface, (255,0,0), (x+62,y-66),(x+66,y-62),2)
        pygame.draw.line(surface, (255,0,0), (x+66,y-66),(x+62,y-62),2)
    if wrong >= 9:
        pygame.draw.line(surface, (100,100,100), (x+60,y-80),(x+60,y-40),2)  # rope
    # optional decorations up to 12
    if wrong >= 10:
        pygame.draw.rect(surface, (120,120,120), (x-80,y+140,40,8))
    if wrong >= 11:
        pygame.draw.rect(surface, (120,120,120), (x+120,y+140,40,8))
    if wrong >= 12:
        pygame.draw.line(surface, (255,0,0), (x-100,y+140),(x+200,y-40),2)

def draw_alphabet(surface, pos, used):
    x0,y0 = pos
    w = 36; h = 34; gapx = 6; gapy = 6
    cols = 7
    buttons = []
    for i,ch in enumerate(ALPHABET):
        col = i % cols
        row = i // cols
        rect = pygame.Rect(x0 + col*(w+gapx), y0 + row*(h+gapy), w, h)
        color = (70,120,70) if ch not in used else (80,80,80)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        draw_text(surface, ch.upper(), (rect.x + 10, rect.y + 6), font=BIG, color=(255,255,255))
        buttons.append((rect,ch))
    return buttons

# ---------- Main UI flow ----------
def main():
    words = load_words_from_args_or_default()
    # start menu options
    difficulty = "medium"
    use_timer = False
    time_limit = None

    # menu loop
    in_menu = True
    while in_menu:
        screen.fill((25,25,60))
        draw_text(screen, "PENDU - Hangman (Pygame)", (20,20), font=BIG)
        draw_text(screen, "Choose difficulty:", (20,90))
        easy_btn = Button((20,120,120,36), "Easy", callback=lambda: None, color=(100,160,100))
        med_btn = Button((150,120,120,36), "Medium", callback=lambda: None, color=(160,120,100))
        hard_btn = Button((280,120,120,36), "Hard", callback=lambda: None, color=(200,80,80))
        timer_btn = Button((20,180,200,36), f"Timer: {'On' if use_timer else 'Off'}", callback=lambda: None, color=(100,100,160))
        start_btn = Button((20,240,160,42), "Start Game", callback=lambda: None, color=(60,140,200))
        quit_btn = Button((200,240,100,42), "Quit", callback=lambda: None, color=(140,60,60))

        # draw buttons (we'll just detect clicks manually)
        for b in (easy_btn,med_btn,hard_btn,timer_btn,start_btn,quit_btn):
            b.draw(screen)

        # show current settings
        draw_text(screen, f"Difficulty: {difficulty}", (420,120))
        draw_text(screen, f"Timer: {'Yes' if use_timer else 'No'}", (420,150))
        draw_text(screen, "Controls:", (20,320))
        draw_text(screen, "- Click letters on the right or type on keyboard", (20,350))
        draw_text(screen, "- Press H for hint (costs attempts)", (20,380))
        draw_text(screen, "- Press ENTER to submit typed word", (20,410))

        pygame.display.flip()
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit(0)
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit(0)
            if ev.key == pygame.K_1:
                difficulty = "easy"
            if ev.key == pygame.K_2:
                difficulty = "medium"
            if ev.key == pygame.K_3:
                difficulty = "hard"
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx,my = ev.pos
            # easy
            if pygame.Rect(20,120,120,36).collidepoint(ev.pos):
                difficulty = "easy"
            if pygame.Rect(150,120,120,36).collidepoint(ev.pos):
                difficulty = "medium"
            if pygame.Rect(280,120,120,36).collidepoint(ev.pos):
                difficulty = "hard"
            if pygame.Rect(20,180,200,36).collidepoint(ev.pos):
                use_timer = not use_timer
                if use_timer:
                    time_limit = 60  # default 60s
                else:
                    time_limit = None
            if pygame.Rect(20,240,160,42).collidepoint(ev.pos):
                in_menu = False
            if pygame.Rect(200,240,100,42).collidepoint(ev.pos):
                pygame.quit(); sys.exit(0)

    # create game object
    game = HangmanGame(words, difficulty=difficulty, time_limit=time_limit)
    typed_buffer = ""
    alpha_buttons = []  # store rects
    message_timer = 0

    # main game loop
    while True:
        screen.fill((12,40,80))
        # events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit(0)
                if game.finished:
                    if ev.key == pygame.K_RETURN:
                        game.reset_round()
                        typed_buffer = ""
                else:
                    if ev.key == pygame.K_BACKSPACE:
                        typed_buffer = typed_buffer[:-1]
                    elif ev.key == pygame.K_RETURN:
                        if typed_buffer:
                            game.guess(typed_buffer)
                            typed_buffer = ""
                    elif ev.key == pygame.K_h:
                        # hint: reveal one unseen letter (cost attempts)
                        unrevealed = [c for c,h in zip(game.secret, game.hidden) if h == "_"]
                        if unrevealed:
                            letter = random.choice(unrevealed)
                            # apply as if the user guessed letter
                            if letter not in game.used_letters:
                                game.used_letters.add(letter)
                            # reveal occurrences but apply penalty
                            for i,c in enumerate(game.secret):
                                if c == letter:
                                    game.hidden[i] = c
                            game.attempts += HINT_PENALTY
                            game.last_message = f"Hint revealed '{letter}' (-{HINT_PENALTY} attempts)."
                            if "".join(game.hidden) == game.secret:
                                game.finish(win=True)
                    else:
                        ch = ev.unicode
                        if ch and ch.isalpha():
                            typed_buffer += ch.lower()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if not game.finished:
                    # check alphabet clicks
                    for rect,ch in alpha_buttons:
                        if rect.collidepoint(ev.pos):
                            game.guess(ch)
                            break
                else:
                    # finished -> clicking resets round
                    game.reset_round()
                    typed_buffer = ""

        # draw hangman and UI
        draw_hangman(screen, 180, 220, game.penalty)

        # word display
        word_display = " ".join(game.hidden)
        draw_text(screen, word_display, (20,420), font=BIG)
        draw_text(screen, f"Attempts: {game.attempts}", (20,480))
        best = get_best_score()
        draw_text(screen, f"Record (best): {best if best is not None else '-'} attempts", (20,510))
        draw_text(screen, f"Difficulty: {game.difficulty}", (20,540))

        # typed buffer
        pygame.draw.rect(screen, (255,255,255), (400,420,320,36), border_radius=6)
        draw_text(screen, typed_buffer, (408,427), font=BIG, color=(0,0,0))
        draw_text(screen, "Type a letter or a word (ENTER to submit). Press H for hint.", (400,460))

        # alphabet block
        alpha_buttons = draw_alphabet(screen, (620,80), game.used_letters)

        # draw life bar
        life_pct = max(0, 1 - (game.penalty / game.max_penalty))
        pygame.draw.rect(screen, (180,180,180), (400,20,300,24), border_radius=8)
        pygame.draw.rect(screen, (60,200,80), (400,20, int(300*life_pct),24), border_radius=8)
        draw_text(screen, f"Lives: {game.max_penalty - game.penalty}/{game.max_penalty}", (710,20))

        # timer
        if game.time_limit:
            left = game.time_left()
            draw_text(screen, f"Time left: {int(left)}s", (400,60))
            if left <= 0 and not game.finished:
                game.finish(win=False)

        # messages
        if game.last_message:
            draw_text(screen, game.last_message, (400, 500), font=SMALL, color=(255,220,0))

        # finished overlay
        if game.finished:
            if game.won:
                txt = f"YOU WIN! The word was '{game.secret}'. Attempts: {game.attempts}"
                draw_text(screen, txt, (320, 320), font=BIG, color=(255,230,160))
                # best message
                best_now = get_best_score()
                if best_now is None or game.attempts <= best_now:
                    draw_text(screen, "🏆 Best ever!!!", (320,360), font=SMALL, color=(255,250,200))
            else:
                draw_text(screen, f"GAME OVER! The word was '{game.secret}'.", (320,320), font=BIG, color=(255,100,100))
            draw_text(screen, "Click anywhere or press ENTER to start a new round.", (320,360))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
