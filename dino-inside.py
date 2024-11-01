import streamlit as st
from PIL import Image, ImageDraw
import time
import random

# Configuration de la page
st.set_page_config(page_title="Jeu du Dinosaure IA", page_icon="🦖", layout="centered")

# Variables de jeu
WIDTH = 600
HEIGHT = 200
GROUND_Y = 150
DINO_SIZE = 20
COACH_SIZE = 10
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
FPS = 30

# Initialisation de l'état du jeu
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'dino_y' not in st.session_state:
    st.session_state.dino_y = GROUND_Y - DINO_SIZE
if 'velocity' not in st.session_state:
    st.session_state.velocity = 0
if 'obstacles' not in st.session_state:
    st.session_state.obstacles = []
if 'jumping' not in st.session_state:
    st.session_state.jumping = False

# Fonction pour gérer le saut
def jump():
    if not st.session_state.jumping and not st.session_state.game_over:
        st.session_state.jumping = True
        st.session_state.velocity = -10

# Fonction pour réinitialiser le jeu
def reset_game():
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.dino_y = GROUND_Y - DINO_SIZE
    st.session_state.velocity = 0
    st.session_state.obstacles = []
    st.session_state.jumping = False

# Détection des touches
st.text("Appuyez sur la barre d'espace pour sauter.")
if st.button("Sauter"):
    jump()
if st.button("Redémarrer") and st.session_state.game_over:
    reset_game()

# Gestion des entrées clavier
# Note: Streamlit ne supporte pas directement la détection des touches du clavier.
# Une alternative serait d'utiliser un composant personnalisé ou des boutons pour les actions.

# Boucle de jeu
if not st.session_state.game_over:
    placeholder = st.empty()
    start_time = time.time()
    last_time = start_time
    while not st.session_state.game_over:
        current_time = time.time()
        delta = current_time - last_time
        if delta < 1/FPS:
            time.sleep(1/FPS - delta)
            current_time = time.time()
            delta = current_time - last_time
        last_time = current_time

        # Mise à jour du score
        st.session_state.score += 1

        # Mise à jour de la position du dinosaure
        if st.session_state.jumping:
            st.session_state.velocity += 1  # Gravité
            st.session_state.dino_y += st.session_state.velocity
            if st.session_state.dino_y >= GROUND_Y - DINO_SIZE:
                st.session_state.dino_y = GROUND_Y - DINO_SIZE
                st.session_state.jumping = False
                st.session_state.velocity = 0

        # Génération d'obstacles
        if random.randint(1, 20) == 1:
            obstacle_x = WIDTH
            obstacle_label = random.choice(["RGPD", "Hallucination", "Erreurs", "Biais", "Sécurité"])
            st.session_state.obstacles.append({"x": obstacle_x, "label": obstacle_label})

        # Mise à jour des obstacles
        for obstacle in st.session_state.obstacles:
            obstacle["x"] -= 5  # Vitesse de déplacement des obstacles

        # Suppression des obstacles hors de l'écran
        st.session_state.obstacles = [ob for ob in st.session_state.obstacles if ob["x"] > -OBSTACLE_WIDTH]

        # Détection des collisions
        for obstacle in st.session_state.obstacles:
            if (0 < obstacle["x"] < DINO_SIZE) and (st.session_state.dino_y + DINO_SIZE > GROUND_Y - OBSTACLE_HEIGHT):
                st.session_state.game_over = True

        # Création de l'image du jeu
        img = Image.new("RGB", (WIDTH, HEIGHT), "white")
        draw = ImageDraw.Draw(img)

        # Dessin du sol
        draw.line((0, GROUND_Y, WIDTH, GROUND_Y), fill="black", width=2)

        # Dessin du dinosaure
        draw.rectangle([0, st.session_state.dino_y, DINO_SIZE, st.session_state.dino_y + DINO_SIZE], fill="blue")

        # Dessin du coach volant "Inside"
        coach_x = DINO_SIZE // 2 - COACH_SIZE // 2
        coach_y = st.session_state.dino_y - COACH_SIZE - 5
        draw.ellipse([coach_x, coach_y, coach_x + COACH_SIZE, coach_y + COACH_SIZE], fill="blue")

        # Dessin des obstacles
        for obstacle in st.session_state.obstacles:
            draw.rectangle([obstacle["x"], GROUND_Y - OBSTACLE_HEIGHT, obstacle["x"] + OBSTACLE_WIDTH, GROUND_Y], fill="red")
            draw.text((obstacle["x"], GROUND_Y), obstacle["label"], fill="black")

        # Dessin du score
        draw.text((WIDTH - 100, 10), f"Score: {st.session_state.score}", fill="black")

        # Affichage de l'image
        placeholder.image(img, use_column_width=False)

    # Affichage du Game Over et du bouton de redémarrage
    st.markdown("<h1 style='color: red;'>Game Over</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2>Score final: {st.session_state.score}</h2>", unsafe_allow_html=True)
    if st.button("Redémarrer"):
        reset_game()
else:
    # Affichage initial du jeu
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)
    draw.line((0, GROUND_Y, WIDTH, GROUND_Y), fill="black", width=2)
    draw.rectangle([0, st.session_state.dino_y, DINO_SIZE, st.session_state.dino_y + DINO_SIZE], fill="blue")
    coach_x = DINO_SIZE // 2 - COACH_SIZE // 2
    coach_y = st.session_state.dino_y - COACH_SIZE - 5
    draw.ellipse([coach_x, coach_y, coach_x + COACH_SIZE, coach_y + COACH_SIZE], fill="blue")
    draw.text((WIDTH - 100, 10), f"Score: {st.session_state.score}", fill="black")
    st.image(img, use_column_width=False)
