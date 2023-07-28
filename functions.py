from psychopy import visual, event
import tkinter as tk
import pandas as pd
import os
import shutil
import subprocess # Pour la fonction de conversion edf2asc


# Déclaration des variables globales utilisées dans le fichier functions.py UNIQUEMENT
FONTSIZE = 36 # La taille de la police

"""
Fonction qui creer un dossier pour enregistrer les donnees de l'exp et qui retourne le nom du dossier cree
"""
def create_new_datafolder():
    # Spécifiez le chemin du dossier data
    dossier_data = r'C:\Users\manip\Desktop\Samet\OCTAV' # Chemin vers le dossier du code OCTAV

    # Vérifier si le dossier data existe
    if not os.path.exists(dossier_data):
        # Créer le dossier data s'il n'existe pas
        os.makedirs(dossier_data)

    # Spécifiez le nom de base pour le dossier
    nom_base_dossier = 'donnees_exp'

    # Compteur pour incrémenter le numéro du dossier
    compteur = 1

    # Boucle pour trouver un nom de dossier disponible
    while True:
        # Construire le nom du dossier avec le numéro
        folder_name = f"{nom_base_dossier}_{compteur:03d}"

        # Vérifier si le dossier existe déjà
        chemin_dossier = os.path.join(dossier_data, folder_name)
        if not os.path.exists(chemin_dossier):
            # Utilisez la fonction os.makedirs() pour créer le dossier
            os.makedirs(chemin_dossier)
            break

        # Incrémenter le compteur pour essayer le prochain numéro
        compteur += 1

    # Afficher le nom du dossier créé
    print(f"Dossier créé : {folder_name}")
    return folder_name

"""
Fonction qui genere un nouveau nom (en incrementant de 1 le dernier numero) en fonction d'un chemin et d'un fichier
"""
def generate_new_filename(directory, file):
    file_name, file_extension = os.path.splitext(file)
    file_list = os.listdir(directory)

    # Filter files in the directory with the same base name
    filtered_files = [f for f in file_list if f.startswith(file_name)]

    # Find the highest number in the existing file names
    existing_numbers = []
    for f in filtered_files:
        try:
            number = int(f[len(file_name):f.index(file_extension)])
            existing_numbers.append(number)
        except ValueError:
            pass

    if existing_numbers:
        # Increment the highest number by 1
        new_number = max(existing_numbers) + 1
    else:
        new_number = 1

    # Create the new file name
    new_filename = f"{file_name}{str(new_number).zfill(3)}{file_extension}"
    return new_filename

"""
Fonction qui permet de renommer un fichier
"""
def rename_file(file_path, new_name):
    directory = os.path.dirname(file_path)
    new_path = os.path.join(directory, new_name)
    os.rename(file_path, new_path)

"""
Fonction qui permet de deplacer un fichier
"""
def move_file(file_path, destination_directory):
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_directory, file_name)
    shutil.move(file_path, destination_path)

"""
Fonction qui permet de convertir le fichier .edf que l'on obtient en sortie du eyetracker en .asc
"""
def edf2asc(input_file, exe_path=r"C:\Program Files (x86)\SR Research\EyeLink\EDF_Access_API\Example\edf2asc.exe"):
    command = [exe_path, input_file]
    subprocess.run(command, shell=True, capture_output=True, text=True)

"""
Fonction qui permet de vérifier si les coordonnées de la souris sont à l intérieur d'un rectangle
"""
def is_mouse_inside_rectangle(mouse_x, mouse_y, rect_x, rect_y, rect_width, rect_height):
    return rect_x - rect_width / 2 < mouse_x < rect_x + rect_width / 2 and rect_y - rect_height / 2 < mouse_y < rect_y + rect_height / 2

"""
Fonction qui permet de demander un clic sur la souris à l'utilisateur afin de poursuivre l'éxécution du programme
La touche 'escape' permet d'arrêter complètement le programme si nécessaire
"""
def mouse_is_clicked(): # Fonction qui attend un clic sur la souris, termine le programme si 'escape' est pressé
    while True:
        mouse_cliked = event.Mouse().getPressed(getTime=True)[0] # renvoie [0, 0, 0] avec un 1 si une des touches de la souris est pressée
        if any(mouse_cliked):
            break
        # Vérifier si la touche 'escape' a été enfoncée pour quitter le programme
        if 'escape' in event.getKeys():
            print("La touche 'escape' a été pressé, arrêt du programme !")
            exit()

"""
Fonction qui permet de récupérer les dimensions de l'écran utiliser
La fonction renvoie les dimensions (width, height) en pixels
"""
def screen_size(): # Fonction qui récupère et renvoie les dimensions de l'écran 
    # Créer une fenêtre factice pour récupérer les dimensions de l'écran
    root = tk.Tk()

    # Récupérer les dimensions de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Afficher les dimensions de l'écran
    print("screen_width (Largeur de l'écran) :", screen_width)
    print("screen_height (Hauteur de l'écran) :", screen_height)

    # Fermer la fenêtre factice
    root.destroy()
    return screen_width, screen_height

"""
Fonction qui permet d'obtenir les phrases sources et cibles à partir d'un fichier excel bien spécifique !
Cette fonction renvoie une df de 3 colonnes: phrases sources, nombre d'erreurs et phrases cibles. Ainsi que, deux listes de phrases sources et cibles  
"""
def traitement_fichier_excel():
    """
    Traitement des données du fichier excel
    """
    # Récupération des données
    df = pd.read_excel("phrases_exp.xlsx")

    # Récupération des phrases source et cible dans des listes
    phrases_source = df['Phrase'].tolist()
    phrases_cible = df['Traduction erreur(s)'].tolist()

    if len(phrases_source) != len(phrases_cible):
        print("Erreur: Les listes de phrases sources et cible n'ont pas la même dimension !")
        exit()

    # Créer une liste vide pour stocker les noms des erreurs
    error_name = []

    # Parcourir la colonne "Type d'erreur considérée"
    for element in df['Type d\'erreur considérée'].unique():
        # Vérifier si l'élément est différent des autres
        if element not in error_name:
            error_name.append(element)

    if len(error_name) != 4 :
        print("Erreur: Le fichier excel doit comporter 4 erreurs ! Arrêt du programme.")
        exit()
    """
    Fin du traitement des données
    """
    return df, phrases_source, phrases_cible, error_name

"""
Fonction qui permet d'obtenir les dimensions en pixels d'un mot dans une fenêtre
Cela nous permet d'effectuer l'affichage des mots dans les bonnes coordonées
"""
def word_length(word, win): # Fonction qui renvoie la taille du mot en entrée dans la fenêtre win
    textbox_word = visual.TextBox(
        window=win,
        text=word,
        font_size = FONTSIZE,
        pos=(0, 0),
        units='pix',
        font_color=[-1,-1,-1],
        textgrid_shape=[len(word),1]
    )
    return textbox_word.getSize()