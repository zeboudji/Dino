import streamlit as st
import streamlit.components.v1 as components

st.title("Jeu du Dinosaure avec Coach Inside")

# Code HTML et JavaScript intégrés pour p5.js
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

      function setup() {
        createCanvas(800, 400);
        dino = new Dino();
        coachDino = new CoachDino();
        obstacles.push(new Obstacle());
      }

      function draw() {
        background(255);
        dino.show();
        dino.move();

        // Coach dino volant
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
          textSize(16);
          text(obstacleWords[o.wordIndex], o.x + 5, o.y + 55);

          // Collision
          if (dino.hits(o)) {
            noLoop();
          }
        }

        // Score
        fill(0);
        textSize(24);
        text("Score: " + score, 10, 25);
        score++;
      }

      function keyPressed() {
        if (key == ' ') {
          dino.jump();
        }
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
          fill(0, 0, 255);  // Dino bleu
          rect(this.x, this.y, this.size, this.size);
        }
      }

      class CoachDino {
        show(dino) {
          fill(0, 0, 255);
          ellipse(dino.x + 50, dino.y - 50, 30, 30);  // Coach en bleu
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

# Afficher le jeu directement dans Streamlit
components.html(html_code, height=500, width=800)
