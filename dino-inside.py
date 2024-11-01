import streamlit as st
import streamlit.components.v1 as components

st.title("Jeu du Dinosaure avec Coach Inside")

# HTML et JavaScript intégrés avec p5.js pour une meilleure ressemblance avec le jeu Chrome
html_code = """
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
  </head>
  <body>
    <script>
      let dino;
      let obstacles = [];
      let score = 0;
      let obstacleWords = ["RGPD", "Hallucination", "Erreurs", "Biais"];
      let coachDino;
      let isGameOver = false;

      function setup() {
        createCanvas(800, 400);
        dino = new Dino();
        coachDino = new CoachDino();
        obstacles.push(new Obstacle());
        textSize(18);
        textAlign(CENTER);
      }

      function draw() {
        background(240);
        
        if (!isGameOver) {
          dino.show();
          dino.move();
          coachDino.show(dino);

          // Gestion des obstacles
          if (frameCount % 90 === 0) {
            obstacles.push(new Obstacle());
          }

          for (let o of obstacles) {
            o.move();
            o.show();

            // Affichage du mot IA sous chaque obstacle
            fill(0);
            text(obstacleWords[o.wordIndex], o.x + o.w / 2, o.y + 60);

            // Vérification de la collision
            if (dino.hits(o)) {
              isGameOver = true;
            }
          }

          // Affichage du score
          score++;
          fill(0);
          text("Score: " + score, width / 2, 30);
        } else {
          fill(0);
          textSize(32);
          text("Game Over", width / 2, height / 2);
          textSize(18);
          text("Press 'R' to Restart", width / 2, height / 2 + 40);
        }
      }

      function keyPressed() {
        if (key == ' ') {
          dino.jump();
        } else if (key == 'R' || key == 'r') {
          resetGame();
        }
      }

      function resetGame() {
        isGameOver = false;
        obstacles = [];
        score = 0;
        dino = new Dino();
        obstacles.push(new Obstacle());
      }

      class Dino {
        constructor() {
          this.x = 50;
          this.y = height - 60;
          this.size = 40;
          this.velY = 0;
          this.gravity = 1.2;
        }

        jump() {
          if (this.y == height - 60) {
            this.velY = -15;
          }
        }

        hits(obstacle) {
          return (this.x + this.size > obstacle.x &&
                  this.x < obstacle.x + obstacle.w &&
                  this.y + this.size > obstacle.y);
        }

        move() {
          this.y += this.velY;
          this.velY += this.gravity;
          this.y = constrain(this.y, 0, height - 60);
        }

        show() {
          fill(0, 0, 255);  // Dino en bleu
          rect(this.x, this.y, this.size, this.size);
        }
      }

      class CoachDino {
        show(dino) {
          fill(0, 0, 255);
          ellipse(dino.x + 50, dino.y - 50, 20, 20);  // Coach en bleu
        }
      }

      class Obstacle {
        constructor() {
          this.w = 20;
          this.h = 40;
          this.x = width;
          this.y = height - this.h;
          this.wordIndex = floor(random(obstacleWords.length));
        }

        move() {
          this.x -= 5;
        }

        show() {
          fill(0);
          rect(this.x, this.y, this.w, this.h);
        }
      }
    </script>
  </body>
</html>
"""

# Affichage du jeu avec Streamlit Components
components.html(html_code, height=500, width=800)
