import os
import webview
import sys

def resource_path(relative_path):
    """Obtenir le chemin absolu pour les ressources, compatible avec PyInstaller."""
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # Chemin vers le fichier HTML
    html_file = resource_path("index.html")
    # Créer une fenêtre WebView
    window = webview.create_window("Jeu du Dinosaure IA", html=html_file, width=1200, height=400)
    # Lancer l'application
    webview.start()

if __name__ == "__main__":
    main()
