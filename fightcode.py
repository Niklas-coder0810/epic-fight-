# app.py
import streamlit as st
import pygame
import threading
import time

# -----------------------------
# Streamlit Seite
# -----------------------------
st.set_page_config(page_title="Jump Battle", layout="centered")

st.title("🎮 Jump Battle")
st.markdown("""
## Steuerung

### Spieler 1
- W → Springen
- A → Links
- D → Rechts

### Spieler 2
- ↑ → Springen
- ← → Links
- → → Rechts

Ziel:
- Springe auf den Kopf des Gegners
- Wer zuerst 3 Punkte hat, gewinnt
""")

run_game = st.button("Spiel starten")


# -----------------------------
# Spiel starten
# -----------------------------
def start_game():

    pygame.init()

    WIDTH = 1000
    HEIGHT = 700

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jump Battle")

    clock = pygame.time.Clock()

    # Farben
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 50, 50)
    BLUE = (50, 100, 255)
    GREEN = (50, 200, 100)

    GRAVITY = 0.7
    MOVE_SPEED = 6
    JUMP_POWER = -14

    font = pygame.font.SysFont("Arial", 36)
    big_font = pygame.font.SysFont("Arial", 60)

    # Plattformen
    platforms = [
        pygame.Rect(0, 650, 1000, 50),

        pygame.Rect(150, 520, 250, 20),
        pygame.Rect(600, 520, 250, 20),

        pygame.Rect(350, 390, 300, 20),

        pygame.Rect(150, 250, 250, 20),
        pygame.Rect(600, 250, 250, 20),
    ]

    class Player:
        def __init__(self, x, y, color, controls):
            self.rect = pygame.Rect(x, y, 50, 60)
            self.color = color
            self.vel_y = 0
            self.on_ground = False
            self.score = 0
            self.controls = controls

        def move(self, keys):

            dx = 0

            if keys[self.controls["left"]]:
                dx -= MOVE_SPEED

            if keys[self.controls["right"]]:
                dx += MOVE_SPEED

            self.rect.x += dx

            # Bildschirmbegrenzung
            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

            # Springen
            if keys[self.controls["jump"]] and self.on_ground:
                self.vel_y = JUMP_POWER
                self.on_ground = False

        def apply_gravity(self):

            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            self.on_ground = False

            for platform in platforms:
                if self.rect.colliderect(platform):

                    if self.vel_y > 0:
                        self.rect.bottom = platform.top
                        self.vel_y = 0
                        self.on_ground = True

        def draw(self):
            pygame.draw.rect(screen, self.color, self.rect)

    # Spieler erstellen
    player1 = Player(
        200,
        100,
        RED,
        {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w
        }
    )

    player2 = Player(
        700,
        100,
        BLUE,
        {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP
        }
    )

    winner = None

    def reset_positions():
        player1.rect.x = 200
        player1.rect.y = 100
        player1.vel_y = 0

        player2.rect.x = 700
        player2.rect.y = 100
        player2.vel_y = 0

    # -----------------------------
    # Game Loop
    # -----------------------------
    running = True

    while running:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not winner:

            keys = pygame.key.get_pressed()

            player1.move(keys)
            player2.move(keys)

            player1.apply_gravity()
            player2.apply_gravity()

            # Kopf-Sprung Erkennung
            if player1.rect.colliderect(player2.rect):

                # Spieler 1 springt auf Spieler 2
                if (
                    player1.vel_y > 0
                    and player1.rect.bottom < player2.rect.centery
                ):
                    player1.score += 1
                    reset_positions()
                    time.sleep(0.5)

                # Spieler 2 springt auf Spieler 1
                elif (
                    player2.vel_y > 0
                    and player2.rect.bottom < player1.rect.centery
                ):
                    player2.score += 1
                    reset_positions()
                    time.sleep(0.5)

            # Gewinner prüfen
            if player1.score >= 3:
                winner = "Spieler 1"

            if player2.score >= 3:
                winner = "Spieler 2"

        # -----------------------------
        # Zeichnen
        # -----------------------------
        screen.fill(WHITE)

        # Plattformen
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)

        # Spieler
        player1.draw()
        player2.draw()

        # Scores
        score_text = font.render(
            f"Spieler 1: {player1.score}      Spieler 2: {player2.score}",
            True,
            BLACK
        )

        screen.blit(score_text, (250, 20))

        # Gewinnertext
        if winner:
            win_text = big_font.render(
                f"{winner} gewinnt!",
                True,
                BLACK
            )

            screen.blit(win_text, (300, 300))

        pygame.display.update()

    pygame.quit()


if run_game:
    game_thread = threading.Thread(target=start_game)
    game_thread.start()
