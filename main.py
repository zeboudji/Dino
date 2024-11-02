import streamlit as st
import base64
import os

def get_base64_encoded_image(image_path):
    """
    Lit une image et retourne son contenu encodé en base64.
    """
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded

def embed_game():
    # Chemin vers le dossier des images
    images_dir = "images"

    # Dictionnaire pour stocker les images encodées
    encoded_images = {}

    # Encodez toutes les images et stockez-les dans le dictionnaire
    for image_name in os.listdir(images_dir):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
            path = os.path.join(images_dir, image_name)
            encoded = get_base64_encoded_image(path)
            encoded_images[image_name] = encoded

    # Lire le fichier HTML
    with open("index.html", "r", encoding='utf-8') as file:
        html_content = file.read()

    # Remplacer les chemins des images par les données encodées
    for image_name, encoded in encoded_images.items():
        # Remplacer 'images/image_name' par 'data:image/format;base64,encoded'
        extension = image_name.split('.')[-1].lower()
        if extension == 'png':
            mime = 'image/png'
        elif extension in ['jpg', 'jpeg']:
            mime = 'image/jpeg'
        elif extension == 'gif':
            mime = 'image/gif'
        elif extension == 'svg':
            mime = 'image/svg+xml'
        else:
            mime = 'image/png'  # Par défaut

        data_uri = f"data:{mime};base64,{encoded}"
        html_content = html_content.replace(f"images/{image_name}", data_uri)

    # Intégrer le HTML dans Streamlit
    st.components.v1.html(
        html_content,
        height=600,  # Ajustez la hauteur selon vos besoins
        scrolling=True
    )

def main():
    st.set_page_config(page_title="Jeu du Dinosaure IA", layout="centered")
    st.title("Jeu du Dinosaure IA 🦖")

    embed_game()

if __name__ == "__main__":
    main()
