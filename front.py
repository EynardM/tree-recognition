import streamlit as st
from PIL import Image, ImageDraw
import torch
from util.imports import *
from util.locations import *
import cv2
from util.variables import *

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.pexels.com/photos/113338/pexels-photo-113338.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    color: white;  /* Set text color to white */
    font-size: 24px;  /* Set font size to 24 pixels */
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

# Fonction pour effectuer la prédiction YOLO
def predict_yolo(image, model):
    try:
        # Charger le modèle YOLO
        yolo_model = YOLO(model)

        # Effectuer la prédiction
        with torch.no_grad():
            results = yolo_model.predict(image)
        return results
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None

def draw_bbox(image_path, label_file):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with open(label_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            x_center *= image.shape[1]
            y_center *= image.shape[0]
            width *= image.shape[1]
            height *= image.shape[0]
            x_min = int(x_center - width / 2)
            y_min = int(y_center - height / 2)
            x_max = int(x_center + width / 2)
            y_max = int(y_center + height / 2)
            
            # Dessiner la boîte englobante
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), LABELS_TO_COLORS[int(class_id)][0], 2)
            
            # Ajouter le texte au-dessus de la boîte
            label_text = INT_TO_LABELS[int(class_id)]
            text_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(image, (x_min, y_min - text_size[1]), (x_min + text_size[0], y_min), LABELS_TO_COLORS[int(class_id)][0], -1)
            cv2.putText(image, label_text, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return image

def main():
    # Insérer le titre avec la mise en forme personnalisée
    st.title("YOLO Predictions")

    # Glisser-déposer une image
    uploaded_file = st.file_uploader("Drop Image Here", type=['jpg', 'jpeg'])
    if uploaded_file is not None:
        # Afficher l'image uploadée
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Sélectionner le modèle YOLO
        model_name = st.selectbox("Select Model", ["train_n_400_16", "augmented_n_400_16", "concatenated_n_400_16", "augmented_s_400_16", "concatenated_s_400_16", "train_m_400_16", "augmented_m_400_16", "concatenated_m_400_16", "augmented_l_400_16", "concatenated_l_400_16"])

        # Bouton pour prédire
        if st.button('Predict'):
            with st.spinner('Predicting...'):
                try:
                    # Charger l'image
                    image = Image.open(uploaded_file).convert("RGB")

                    # Effectuer la prédiction YOLO
                    results = predict_yolo(image, os.path.join("Models", model_name, "weights", "best.pt"))

                    # Afficher les résultats de prédiction
                    if results is not None:
                        st.success("Prediction successful!")
                        res_plotted = results[0].plot(font_size=0.1, line_width=1)
                        cv2.imwrite("prediction.jpg", res_plotted)
                        st.image('prediction.jpg', caption='Prediction', use_column_width=True)
                        os.remove("prediction.jpg")

                        label_file = DATASET_TEST_PATH+'/labels/'+uploaded_file.name.split('.')[0]+'.txt'
                        image_with_bbox = draw_bbox(DATASET_TEST_PATH+'/images/'+uploaded_file.name, label_file)
                        st.image(image_with_bbox, caption='Ground Truth', use_column_width=True)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
