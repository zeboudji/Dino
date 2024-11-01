// Récupération des éléments du DOM
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const gameOverElement = document.getElementById('gameOver');
const restartButton = document.getElementById('restartButton');

// Constantes du jeu
const WIDTH = canvas.width;
const HEIGHT = canvas.height;
const GROUND_Y = 350;
const DINO_SIZE = 40;
const COACH_SIZE = 15;
const OBSTACLE_WIDTH = 30;
const OBSTACLE_HEIGHT = 50;
const OBSTACLE_SPEED = 6;
const GRAVITY = 1;
const JUMP_FORCE = 20;

// Variables du jeu
let score = 0;
let gameOver = false;
let dino = {
    x: 50,
    y: GROUND_Y - DINO_SIZE,
    width: DINO_SIZE,
    height: DINO_SIZE,
    velocityY: 0,
    isJumping: false
};
let coach = {
    x: dino.x + DINO_SIZE / 2 - COACH_SIZE / 2,
    y: dino.y - COACH_SIZE - 10,
    radius: COACH_SIZE / 2
};
let obstacles = [];

// Liste des étiquettes IA
const obstacleLabels = ["RGPD", "Hallucination", "Erreurs", "Biais", "Sécurité"];

// Fonction pour gérer le saut du dinosaure
function jump() {
    if (!dino.isJumping && !gameOver) {
        dino.velocityY = -JUMP_FORCE;
        dino.isJumping = true;
    }
}

// Fonction pour réinitialiser le jeu
function resetGame() {
    score = 0;
    gameOver = false;
    dino.y = GROUND_Y - DINO_SIZE;
    dino.velocityY = 0;
    dino.isJumping = false;
    coach.x = dino.x + DINO_SIZE / 2 - COACH_SIZE / 2;
    coach.y = dino.y - COACH_SIZE - 10;
    obstacles = [];
    gameOverElement.style.display = 'none';
    restartButton.style.display = 'none';
    requestAnimationFrame(gameLoop);
}

// Fonction pour créer de nouveaux obstacles
function createObstacle() {
    const label = obstacleLabels[Math.floor(Math.random() * obstacleLabels.length)];
    const obstacle = {
        x: WIDTH,
        y: GROUND_Y - OBSTACLE_HEIGHT,
        width: OBSTACLE_WIDTH,
        height: OBSTACLE_HEIGHT,
        label: label
    };
    obstacles.push(obstacle);
}

// Fonction pour détecter les collisions
function detectCollision(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

// Fonction principale de la boucle de jeu
let obstacleTimer = 0;
function gameLoop() {
    if (gameOver) return;

    // Effacer le canvas
    ctx.clearRect(0, 0, WIDTH, HEIGHT);

    // Dessiner le sol
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, GROUND_Y, WIDTH, 2);

    // Gérer le saut
    dino.velocityY += GRAVITY;
    dino.y += dino.velocityY;

    if (dino.y >= GROUND_Y - DINO_SIZE) {
        dino.y = GROUND_Y - DINO_SIZE;
        dino.isJumping = false;
        dino.velocityY = 0;
    }

    // Mettre à jour la position du coach
    coach.x = dino.x + DINO_SIZE / 2 - COACH_SIZE / 2;
    coach.y = dino.y - COACH_SIZE - 10;

    // Dessiner le dinosaure
    ctx.fillStyle = "#0000FF"; // Bleu
    ctx.fillRect(dino.x, dino.y, dino.width, dino.height);

    // Dessiner le coach volant "Inside"
    ctx.beginPath();
    ctx.arc(coach.x + coach.radius, coach.y + coach.radius, coach.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#0000FF"; // Bleu
    ctx.fill();
    ctx.closePath();

    // Gérer les obstacles
    obstacleTimer++;
    if (obstacleTimer > 90) { // Intervalle entre les obstacles
        createObstacle();
        obstacleTimer = 0;
    }

    // Dessiner et mettre à jour les obstacles
    for (let i = 0; i < obstacles.length; i++) {
        let obs = obstacles[i];
        obs.x -= OBSTACLE_SPEED;

        // Dessiner l'obstacle
        ctx.fillStyle = "#FF0000"; // Rouge
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);

        // Dessiner l'étiquette IA sous l'obstacle
        ctx.fillStyle = "#000000"; // Noir
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.fillText(obs.label, obs.x + obs.width / 2, obs.y + obs.height + 20);

        // Détecter les collisions
        let dinoRect = {x: dino.x, y: dino.y, width: dino.width, height: dino.height};
        let obsRect = {x: obs.x, y: obs.y, width: obs.width, height: obs.height};
        if (detectCollision(dinoRect, obsRect)) {
            gameOver = true;
            gameOverElement.style.display = 'block';
            restartButton.style.display = 'block';
        }

        // Supprimer les obstacles hors écran
        if (obs.x + obs.width < 0) {
            obstacles.splice(i, 1);
            i--;
        }
    }

    // Mettre à jour le score
    score++;
    scoreElement.textContent = `Score: ${score}`;

    // Appeler la prochaine frame
    requestAnimationFrame(gameLoop);
}

// Gestion des entrées clavier
document.addEventListener('keydown', function(event) {
    if (event.code === 'Space') {
        jump();
    }
});

// Gestion du bouton de redémarrage
restartButton.addEventListener('click', resetGame);

// Démarrer le jeu
requestAnimationFrame(gameLoop);

