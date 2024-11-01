import streamlit as st
import pygame
import random
import time

# Initialiser Pygame
pygame.init()

# Fonction pour lancer le jeu
def jeu_dinosaure():
    # Dimensions de la fenêtre de jeu
    LARGEUR_FENETRE, HAUTEUR_FENETRE = 800, 400
    fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption("Dino avec Coach Inside")

    # Couleurs
    NOIR = (0, 0, 0)
    BLANC = (255, 255, 255)
    BLEU = (0, 0, 255)

    # Chargement des images du dinosaure principal et du dinosaure volant
    dino_image = pygame.Surface((40, 60))  # Placeholder pour le dinosaure principal
    dino_image.fill(NOIR)  # T-Rex original
    coach_image = pygame.Surface((30, 30))  # Placeholder pour "Inside"
    coach_image.fill(BLEU)  # Inside est en bleu

    # Position initiale des dinosaures
    dino_x, dino_y = 50, HAUTEUR_FENETRE - 60
    coach_x, coach_y = dino_x + 50, dino_y - 80

    # Obstacle et mots IA
    obstacles = ["RGPD", "Hallucination", "Erreurs", "Biais"]
    obstacle_x = LARGEUR_FENETRE
    obstacle_y = HAUTEUR_FENETRE - 40
    obstacle_texte = random.choice(obstacles)
    obstacle_vitesse = 5

    # Vitesse du dinosaure
    dino_vel_y = 0
    saut = False
    score = 0
    police = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    jeu_en_cours = True

    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False

        # Gestion du saut
        touches = pygame.key.get_pressed()
        if touches[pygame.K_SPACE] and not saut:
            saut = True
            dino_vel_y = -15

        if saut:
            dino_y += dino_vel_y
            dino_vel_y += 1
            if dino_y >= HAUTEUR_FENETRE - 60:
                dino_y = HAUTEUR_FENETRE - 60
                saut = False

        # Déplacement des obstacles
        obstacle_x -= obstacle_vitesse
        if obstacle_x < -50:
            obstacle_x = LARGEUR_FENETRE
            obstacle_texte = random.choice(obstacles)
            score += 1

        # Collision
        if (dino_x < obstacle_x + 40 and dino_x + 40 > obstacle_x and
                dino_y < obstacle_y + 40 and dino_y + 60 > obstacle_y):
            jeu_en_cours = False

        # Affichage des éléments du jeu
        fenetre.fill(BLANC)
        fenetre.blit(dino_image, (dino_x, dino_y))  # Dino principal
        fenetre.blit(coach_image, (coach_x, coach_y))  # Coach volant

        # Affichage de l'obstacle et du texte IA
        pygame.draw.rect(fenetre, NOIR, (obstacle_x, obstacle_y, 40, 40))
        texte_ia = police.render(obstacle_texte, True, NOIR)
        fenetre.blit(texte_ia, (obstacle_x, obstacle_y + 40))

        # Affichage du score
        texte_score = police.render(f"Score: {score}", True, NOIR)
        fenetre.blit(texte_score, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Utilisation de Streamlit pour lancer le jeu
st.title("Jeu du Dinosaure avec Coach Inside")
if st.button("Lancer le jeu"):
    jeu_dinosaure()
