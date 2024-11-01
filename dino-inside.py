import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes de l'écran
WIDTH, HEIGHT = 800, 400
GROUND_Y = 300
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Configuration de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Dinosaure IA")
clock = pygame.time.Clock()

# Police pour le texte
font = pygame.font.SysFont(None, 36)

# Classe pour le Dinosaure
class Dinosaur:
    def __init__(self):
        self.size = 50
        self.x = 50
        self.y = GROUND_Y - self.size
        self.velocity_y = 0
        self.jump_force = 15
        self.gravity = 1
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -self.jump_force
            self.is_jumping = True

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        if self.y >= GROUND_Y - self.size:
            self.y = GROUND_Y - self.size
            self.is_jumping = False
            self.velocity_y = 0

    def draw(self, surface):
        # Dessin du dinosaure bleu
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.size, self.size))
        # Dessin du coach volant "Inside"
        coach_radius = 10
        coach_x = self.x + self.size // 2
        coach_y = self.y - 15
        pygame.draw.circle(surface, BLUE, (coach_x, coach_y), coach_radius)

# Classe pour les Obstacles
class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = 50
        self.x = WIDTH
        self.y = GROUND_Y - self.height
        self.speed = 6
        self.labels = ["RGPD", "Hallucination", "Erreurs", "Biais", "Sécurité"]
        self.label = random.choice(self.labels)
        self.font = pygame.font.SysFont(None, 24)
        self.label_surface = self.font.render(self.label, True, BLACK)

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        # Centrer le texte sous l'obstacle
        label_rect = self.label_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height + 10))
        surface.blit(self.label_surface, label_rect)

    def off_screen(self):
        return self.x < -self.width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Fonction principale du jeu
def main():
    dinosaur = Dinosaur()
    obstacles = []
    spawn_timer = 0
    spawn_interval = 90  # Nombre de frames entre les obstacles
    score = 0
    game_over = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dinosaur.jump()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            # Mise à jour du dinosaure
            dinosaur.update()

            # Gestion des obstacles
            spawn_timer += 1
            if spawn_timer >= spawn_interval:
                obstacles.append(Obstacle())
                spawn_timer = 0

            for obstacle in obstacles:
                obstacle.update()

            # Suppression des obstacles hors de l'écran
            obstacles = [ob for ob in obstacles if not ob.off_screen()]

            # Détection des collisions
            dino_rect = pygame.Rect(dinosaur.x, dinosaur.y, dinosaur.size, dinosaur.size)
            for obstacle in obstacles:
                if dino_rect.colliderect(obstacle.get_rect()):
                    game_over = True

            # Mise à jour du score
            score += 1

        # Dessin de l'écran
        screen.fill(WHITE)

        # Dessin du sol
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        # Dessin du dinosaure
        dinosaur.draw(screen)

        # Dessin des obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Affichage du score
        score_surface = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (WIDTH - 150, 20))

        if game_over:
            # Affichage du Game Over
            game_over_surface = font.render("Game Over", True, RED)
            restart_surface = pygame.font.SysFont(None, 24).render("Appuyez sur 'R' pour redémarrer", True, BLACK)
            screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()
