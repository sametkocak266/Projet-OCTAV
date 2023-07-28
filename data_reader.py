import cv2, glob, os
import pandas as pd

# Numero du dossier a visualiser
number_exp = input("VISUALISATION\nEntrez le numero de l'exp : donnees_exp_")
eyelinkfolder = "donnees_exp_"+number_exp+"\data_eyelink.asc"

# On récupère la DataFrame contenant les informations de l'experimentation pour determiner le nombre de phrases
df = pd.read_csv("donnees_exp_"+number_exp+"\data_exp.csv")
n = len(df) # Nombre de phrases durant l'experience

# Récupération des données en sortie du eyetracker
eye_data = [[] for _ in range(int(n))]
mouse_data = [[] for _ in range(int(n))]

# Flag
phrase_number = 0 
start=False

with open(eyelinkfolder,'r', encoding='ISO-8859-1') as file :
    for line in file:
        if "DATA" in line:
            if "SCREENSIZE" in line:
                values = line.split()
                screen_width_exp = float(values[5]) # taille ecran de l'exp en longueur
                screen_height_exp = float(values[7]) # taille ecran de l'exp en largeur
                print("SCREENSIZE EXP", screen_width_exp, screen_height_exp)
        if ("EFIX" in line) and start:
            values = line.split()
            eye_data[phrase_number-1].append([float(values[4]), float(values[5]), float(values[6])])
        if "MOUSECLICK" in line:
            values = line.split()
            mouse_coord_x = float(values[3])
            mouse_coord_y = float(values[4])
            mouse_data[phrase_number-1].append([mouse_coord_x, mouse_coord_y])
        if "EVENT" in line:
            continue
        if "SENTENCE NUMBER" in line:
            start = True
            phrase_number+=1
        if "ERROR" in line and start:
            print("ERR : Le sujet a appuyer sur la touche 'espcape' durant l'expérience") 

# Chemin du dossier
folder_path = 'donnees_exp_'+number_exp
motif_fichier_image = 'page_exp_*.png'

chemin_fichiers = glob.glob(f"{folder_path}/{motif_fichier_image}")

page_number = 0

for path in chemin_fichiers:
    # Chargement de l'image
    image = cv2.imread(path)

    # Create a new file name for visualisation
    new_file_name = f"page_visualisation_{page_number+1}.png"

    # Construct the path for the new file
    new_path = os.path.join(folder_path, new_file_name)

    # Check if the file already exists
    if os.path.exists(new_path):
        os.remove(new_path)  # Supprimer le fichier existant
 

    # Color of EFIX circles (Blue, Green, Red)
    fixation_color = (0, 100, 255)  # Orange
    fixation_circle_radius = 10 # Radius of EFIX circles

    # Draw EFIX Circles
    for i, element in enumerate(eye_data[page_number]):
        time_fixation = int(element[0])
        coord_fixation = (int(element[1]), int(element[2])) #(int(element[1])+335, int(element[2])+41)
        radius = int(fixation_circle_radius * (time_fixation / 150))
        
        # Dessiner le cercle
        cv2.circle(image, coord_fixation, radius, fixation_color, 2)

        # Ajouter le rang de fixation au centre du cercle
        text = str(i+1)  # Le rang de fixation (1-indexé)
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        text_coord = (coord_fixation[0] - text_size[0] // 2, coord_fixation[1] + text_size[1] // 2)
        cv2.putText(image, text, text_coord, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)



    # Color of MOUSECLICK circles (Blue, Green, Red)
    mouseclick_color = (0, 255, 0)  # Green
    click_circle_radius = 5 # Radius of MOUSECLICK circles
    
    # Draw MOUSECLICK Circles
    for element in mouse_data[page_number]:
        coord_click = (int(element[0]) + int(screen_width_exp/2), - int(element[1]) + int(screen_height_exp/2))
        cv2.circle(image, coord_click, click_circle_radius, mouseclick_color, -1)

    # Afficher l'image avec les cercles
    cv2.imwrite(new_path, image)
    page_number+=1

print("Les fichiers .png contiennent les donnees de l'experimentation")