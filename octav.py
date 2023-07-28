from psychopy import visual, core, event
# Importation de toutes les fonctions contenues dans le fichier functions
from functions import *
from pygaze.libscreen import Display
from pygaze.eyetracker import EyeTracker
import pygaze
import pandas as pd

"""
Préparation de l'expérimentation
Récupératin des dimensions de l'écran, des phrases du fichier excel et déclaration des variables 
"""
# Récupération des dimensions de l'écran
screen_width, screen_height = screen_size()

# Création d'un display "psychopy" avec la librairie pygaze
args = {
    'size': [screen_width, screen_height],
    'fullscr': True
}
disp = Display(disptype="psychopy", **args)

# Créer une instance de EyeTracker
# "dummy" pour le mode souris et "eyelink"/"tobii"/etc.. pour la connexion avec le eyetracker
tracker = EyeTracker(disp, trackertype="eyelink")

# Récupération de la DataFrame, des phrases sources et cibles, des noms des erreurs du fichier excel
X, phrases_source, phrases_cible, error_name = traitement_fichier_excel()

# Récupération des dimensions
# print(X.shape) # Dimension de la DataFrame
# Nombre d'observations (nombre de phrases sources et cibles à étudier)
n = X.shape[0]
# p = X.shape[1] # Nombre de variables

# Déclaration des variables globales à l'aide des dimensions de l'écran
rect_width = screen_width/8  # Longueur des buttons erreurs
rect_height = screen_height/13  # Largeur des buttons erreurs
# Position des buttons erreurs en largeur (axe y) sur l'écran
pos_height = - 0.6 * (screen_height/2)
text_height = rect_height/2  # Taille de la police à des noms d'erreurs en pixel
square_pix = 80  # Dimension en pixel du button carré NEXT, ATTENTION! : cette variable est fixé, elle ne dépend pas de l'écran utilisé

# ATTENTION! FONTSIZE : Taille de la police fixé dans le fichier functions.py
# Espacement d'une lettre entre les mots des phrases sources et cibles en pixels
espace = 13 * FONTSIZE/24
# Position of the first letter from the 'left' side of phrases source et cible
first_letter_pix = 100

# Position vertical sur l'ecran du texte source et du texte cible
y_pos_source = screen_height/3
y_pos_cible = screen_height/14

# Listes du nom des erreurs etudiees dans le jeu de donnees, ces données sont récupérer dans le fichier excel de base: phrases_exp.xlsx
erreur1 = error_name[0]
erreur2 = error_name[1]
erreur3 = error_name[2]
erreur4 = error_name[3]

# Color of buttons
color1 = [1, 1, -1]  # Color rgb of erreur1 - yellow
color2 = [-1, -1, 1]  # Color rgb of erreur2 - blue
color3 = [1, -1, -1]  # Color rgb of erreur3 - red
color4 = [1, -1, 1]  # Color rgb of erreur4 - pink

# Envoie des données utiles de l'expérimentation au fichier .edf en sortie de l'occulometre
tracker.log("DATA SCREENSIZE Width: {} Height: {}".format(
    screen_width, screen_height))
tracker.log("DATA FONTSIZE {}".format(FONTSIZE))
tracker.log("DATA FIRSTPIX {}".format(first_letter_pix))
tracker.log("DATA YPOS Source: {} Cible: {}".format(y_pos_source, y_pos_cible))
tracker.log("DATA ERREURS {} {} {} {}".format(
    erreur1, erreur2, erreur3, erreur4))
tracker.log("DATA COLOR {} {} {} {}".format(color1, color2, color3, color4))

# Variable results_source et results_cible qui sera stocker dans un fichier data_exp.csv à la fin de l'expérimentation
results_source = {
    # liste contenant toutes les phrases sources à afficher
    "Phrase source": phrases_source,
    # liste contenant toutes les erreurs sélectionnées dans la phrase source pour l'erreur 1
    erreur1 + " source": ["" for _ in range(n)],
    erreur2 + " source": ["" for _ in range(n)],
    erreur3 + " source": ["" for _ in range(n)],
    erreur4 + " source": ["" for _ in range(n)]
}

results_cible = {
    "Phrase cible": phrases_cible,
    erreur1 + " cible": ["" for _ in range(n)],
    erreur2 + " cible": ["" for _ in range(n)],
    erreur3 + " cible": ["" for _ in range(n)],
    erreur4 + " cible": ["" for _ in range(n)]
}

###
# Variable coord_source et coord_cible qui sera stocker dans un fichier ??.csv à la fin de l'expérimentation pour calculer le FP/TP pour chaque erreur dans l'analyse
coord_source = {
    # liste contenant toutes les coordonnées des erreurs sélectionnées dans la phrase source pour l'erreur i
    erreur1 + " coord source": [[] for _ in range(n)],
    erreur2 + " coord source": [[] for _ in range(n)],
    erreur3 + " coord source": [[] for _ in range(n)],
    erreur4 + " coord source": [[] for _ in range(n)]
}

coord_cible = {
    # liste contenant toutes les coordonnées des erreurs sélectionnées dans la phrase cible pour l'erreur i
    erreur1 + " coord cible": [[] for _ in range(n)],
    erreur2 + " coord cible": [[] for _ in range(n)],
    erreur3 + " coord cible": [[] for _ in range(n)],
    erreur4 + " coord cible": [[] for _ in range(n)]
}
###

# Liste qui contient les dimensions en pixels des rectangles source et cible à chaque screen
# Cette liste est envoyeée au fichier data_rect_pos.csv à la fin de l'expérimentation pour compter le temps des EFIX dans les deux rectangles
position_rect_sc = []

""" 
Début de l'expérimentation
"""
# Création de la fenêtre pour l'expérimentation
win_exp = pygaze.expdisplay

# Préparation de la fenêtre win_exp
# Création du rectangle des boutons ERREUR
button_rect1 = visual.Rect(win_exp, rect_width, rect_height, fillColor='lightgray',
                           lineColor=color1, lineWidth=4, pos=(-(3/5)*(screen_width/2), pos_height), units='pix',)
button_rect2 = visual.Rect(win_exp, rect_width, rect_height, fillColor='lightgray',
                           lineColor=color2, lineWidth=4, pos=(-(1/5)*(screen_width/2), pos_height), units='pix')
button_rect3 = visual.Rect(win_exp, rect_width, rect_height, fillColor='lightgray',
                           lineColor=color3, lineWidth=4, pos=((1/5)*(screen_width/2), pos_height), units='pix')
button_rect4 = visual.Rect(win_exp, rect_width, rect_height, fillColor='lightgray',
                           lineColor=color4, lineWidth=4, pos=((3/5)*(screen_width/2), pos_height), units='pix')

# Création des textes des boutons ERREUR
button_text1 = visual.TextStim(win_exp, text=erreur1, font="Consolas", pos=(
    -(3/5)*(screen_width/2), pos_height), units='pix', color='black', height=text_height)
button_text2 = visual.TextStim(win_exp, text=erreur2, font="Consolas", pos=(
    -(1/5)*(screen_width/2), pos_height), units='pix', color='black', height=text_height)
button_text3 = visual.TextStim(win_exp, text=erreur3, font="Consolas", pos=(
    (1/5)*(screen_width/2), pos_height), units='pix', color='black', height=text_height)
button_text4 = visual.TextStim(win_exp, text=erreur4, font="Consolas", pos=(
    (3/5)*(screen_width/2), pos_height), units='pix', color='black', height=text_height)

# Création du bouton NEXT
button_square_next = visual.Rect(win_exp, square_pix, square_pix, fillColor='lightgray',
                                 lineColor='black', lineWidth=4, pos=((screen_width/2)-square_pix/2, -2*square_pix), units='pix')
button_next = visual.TextStim(win_exp, text='NEXT', font="Consolas", pos=(
    (screen_width/2)-square_pix/2, -2*square_pix), units='pix', color='black', height=square_pix/3)

# Création du bouton REMOVE
button_remove = visual.Rect(win_exp, 2*square_pix, square_pix, fillColor='lightgray',
                            lineColor='black', lineWidth=4, pos=(0, pos_height - (3/2)*square_pix), units='pix')
button_text_remove = visual.TextStim(win_exp, text='REMOVE', font="Consolas", pos=(
    0, pos_height - (3/2)*square_pix), units='pix', color='black', height=square_pix/3)

# On cache la souris pendant la calibration
win_exp.setMouseVisible(False)

# Initialiser l'eye-tracker - calibration
tracker.calibrate()

# Envoie d'un message avant le début de l'expérience
tracker.log("Starting experiment")

# Début de l'enregistrement des données
tracker.start_recording()

# Création d'un dossier pour stocker les données de l'expérience
name_data_folder = create_new_datafolder()  # Nom du dossier : donnees_exp_*
data_folder_path = os.path.abspath(name_data_folder)  # Chemin du dossier

# Sending postion of buttons error to a list before .txt file for calculating the fixations time and the total time in the analysis.py code
# Creation d'un fichier data_buttons.txt pour stocker les dimensions et la position des 4 bouttons erreurs
datafile_buttons = open('data_buttons.txt', 'w')

datafile_buttons.write(
    "Dimensions des boutons erreurs : {} {}\n".format(rect_width, rect_height))
datafile_buttons.write("Coord du bouton erreur {}: {} {}\n".format(
    error_name[0], -(3/5)*(screen_width/2) + screen_width/2, - pos_height + screen_height/2))
datafile_buttons.write("Coord du bouton erreur {}: {} {}\n".format(
    error_name[1], -(1/5)*(screen_width/2) + screen_width/2, - pos_height + screen_height/2))
datafile_buttons.write("Coord du bouton erreur {}: {} {}\n".format(
    error_name[2], (1/5)*(screen_width/2) + screen_width/2, - pos_height + screen_height/2))
datafile_buttons.write("Coord du bouton erreur {}: {} {}\n".format(
    error_name[3], (3/5)*(screen_width/2) + screen_width/2, - pos_height + screen_height/2))

# Fermeture du fichier data_buttons.txt
datafile_buttons.close()

# Move the file in the folder
move_file('data_buttons.txt', data_folder_path)


for k in range(n):  # n corresponds aux nombres de phrases sources et cibles récupérer dans le fichier excel

    # Affichage d'un stimulus à la première lettre jusqu'a la fixation du sujet
    win_exp.flip()  # On rafraichit la fenêtre

    # Hiding the mouse
    win_exp.setMouseVisible(False)

    # Création d'un stimuli
    fixation_cross = visual.TextStim(win_exp, text="+", font="consolas", color="black",
                                     pos=(-screen_width/2 + first_letter_pix, screen_height/3), units='pix', height=FONTSIZE)
    # Affichage de la croix
    fixation_cross.draw()
    # Rafraichir la page de la croix
    win_exp.flip()

    # Pause de 2 secondes
    core.wait(2)

    win_exp.flip()  # On rafraichit la fenêtre
    win_exp.setMouseVisible(True)

    # Réinitialisation des couleurs (flag, et couleurs des buttons erreurs)
    highlight_color = None
    button_rect1.setFillColor('lightgray')
    button_rect2.setFillColor('lightgray')
    button_rect3.setFillColor('lightgray')
    button_rect4.setFillColor('lightgray')
    button_remove.setFillColor('lightgray')

    # Création des TextBox pour la phrase source
    # On remplace les apostrophes courbes pour un affichage correct
    phrases_source_corr = phrases_source[k].replace("’", "'")
    # On remplace les guillemets d'ouverture et de fermeture pour un affichage correct
    phrases_source_corr = phrases_source_corr.replace("“", "«")
    # RAJOUTER DES REPLACE SI DES CARACTERES SPECIAUX DANS LE JEU DE DONNEES
    phrases_source_corr = phrases_source_corr.replace("”", "»")
    # On sépare la phrase en mots dans une liste
    liste_source = phrases_source_corr.split()
    text_box_source = []  # Liste de TextBox contenant tous les mots de la phrases
    cumul_s = 0  # Variable pour la définition de la position des mots source
    y_pos_s = y_pos_source  # position de la phrase sur la largeur de l'ecran
    dimensions_words_source = []  # liste pour le calcule de la position du mot surligné

    nb_ligne_s = 0  # Variable comptant le nombre de ligne dans la phrase source affichée

    # Construction de la phrase source n°k
    for i in range(len(liste_source)):
        if i == 0:
            # Le premier mots commence au pixel "first_letter_pix" en partant de la gauche
            cumul_s = cumul_s + \
                word_length(liste_source[i], win_exp)[0]/2 + first_letter_pix
            nb_ligne_s += 1
        else:
            # Calcul de la position du mots précédent et de la longueur pour déterminer la position du mots
            cumul_s = cumul_s + word_length(liste_source[i-1], win_exp)[0]/2 + espace + word_length(liste_source[i], win_exp)[0]/2

        # Cas ou le prochain mots va deborder de l'écran
        if cumul_s + word_length(liste_source[i], win_exp)[0]/2 > screen_width - first_letter_pix:
            # revient à la ligne sur la largeur
            y_pos_s = y_pos_s - textboxs.getSize()[1]/2 - espace
            # position horizontale identique à la ligne d'avant
            cumul_s = word_length(liste_source[i], win_exp)[0]/2 + first_letter_pix
            nb_ligne_s += 1  # On détermine le nombre de ligne

        textboxs = visual.TextBox(
            window=win_exp,
            text=liste_source[i],
            # Taille du texte, à ajuster avec la variable espace pour une lecture confortable
            font_size=FONTSIZE,
            # Position du milieu du mot
            pos=(-screen_width/2 + cumul_s, y_pos_s),
            border_color=None,  # draw a blue border around stim
            border_stroke_width=4,  # border width of 3 pix.
            grid_color=None,
            grid_stroke_width=2,
            units='pix',  # Unité : pixels
            font_name="Consolas",  # Police pour avoir le même espace pour chaque lettre
            font_color=[-1, -1, -1],  # Couleur du texte 'black'
            italic=False,
            textgrid_shape=[len(liste_source[i]), 1],
        )
        textboxs.setTextGridLineWidth(3)
        # Liste contenant toutes les TextBox avec les mots de la phrase source
        text_box_source.append(textboxs)
        dimensions_words_source.append([text_box_source[i].getPosition()[0], text_box_source[i].getPosition()[1], text_box_source[i].getSize()[0], text_box_source[i].getSize()[1]])

    # Création des TextBox pour la phrase cible
    phrases_cible_corr = phrases_cible[k].replace("’", "'")
    phrases_cible_corr = phrases_cible_corr.replace("“", "«")
    phrases_cible_corr = phrases_cible_corr.replace("”", "»")
    liste_cible = phrases_cible_corr.split()
    text_box_cible = []
    cumul_c = 0
    y_pos_c = y_pos_cible
    dimensions_words_cible = []

    nb_ligne_c = 0  # Variable comptant le nombre de ligne dans la phrase cible affichée

    # Construction de la phrase cible n°k
    for j in range(len(liste_cible)):
        if j == 0:
            cumul_c = cumul_c + \
                word_length(liste_cible[j], win_exp)[0]/2 + first_letter_pix
            nb_ligne_c += 1
        else:
            cumul_c = cumul_c + word_length(liste_cible[j], win_exp)[0]/2 + espace + word_length(liste_cible[j-1], win_exp)[0]/2

        # Cas ou le prochain mots va deborder de l'écran
        if cumul_c + word_length(liste_cible[j], win_exp)[0]/2 > screen_width - first_letter_pix:
            y_pos_c = y_pos_c - textboxc.getSize()[1]/2 - espace
            # Erreur debut doit prendre en compte la longueur du prochain mot
            cumul_c = word_length(liste_cible[j], win_exp)[
                0]/2 + first_letter_pix
            nb_ligne_c += 1

        textboxc = visual.TextBox(
            window=win_exp,
            text=liste_cible[j],
            # Taille du texte, à ajuster avec la variable espace pour une lecture confortable
            font_size=FONTSIZE,
            # pos corresponds à la position du milieu du mot
            pos=(-screen_width/2 + cumul_c, y_pos_c),
            border_color=None,  # draw a blue border around stim
            border_stroke_width=4,  # border width of 3 pix.
            grid_color=None, grid_stroke_width=2,
            units='pix',  # Unité : pixels
            font_name="Consolas",  # Police pour avoir le même espace pour chaque lettre
            font_color=[-1, -1, -1],  # Couleur du texte 'black'
            italic=False,
            textgrid_shape=[len(liste_cible[j]), 1]
        )
        textboxc.setTextGridLineWidth(3)
        # Liste contenant toutes les TextBox avec les mots de la phrase cible
        text_box_cible.append(textboxc)
        dimensions_words_cible.append([text_box_cible[j].getPosition()[0], text_box_cible[j].getPosition()[1], text_box_cible[j].getSize()[0], text_box_cible[j].getSize()[1]])

    # Création des rectangles pour le fond des textes source et cible
    # On détermine la largeur du rectangle pour la phrase source
    height_rect_s = nb_ligne_s * textboxs.getSize()[1]
    # On détermine la largeur du rectangle pour la phrase cible
    height_rect_c = nb_ligne_c * textboxc.getSize()[1]

    # Déclaration des rectangles de fond pour les phrases source et cible
    back_rect_source = visual.Rect(win_exp, screen_width - first_letter_pix, height_rect_s, fillColor='lightgray',
                                   lineColor='black', pos=(0, y_pos_source - ((nb_ligne_s - 1) * (1/2) * (textboxs.getSize()[1]))), units='pix')
    back_rect_cible = visual.Rect(win_exp, screen_width - first_letter_pix, height_rect_c, fillColor='lightgray',
                                  lineColor='black', pos=(0, y_pos_cible - ((nb_ligne_c - 1) * (1/2) * (textboxc.getSize()[1]))), units='pix')

    # On ajoute les dimensions de ce screen a la liste position_rect_sc pour conserver ces donnees dans data_rect_pos.csv
    rect_pos = [int(y_pos_source + (1/2) * (textboxs.getSize()[1])), int(y_pos_source + (1/2) * (textboxs.getSize()[1]) - height_rect_s),
                int(y_pos_cible + (1/2) * (textboxc.getSize()[1])), int(y_pos_cible + (1/2) * (textboxc.getSize()[1]) - height_rect_c)]
    # columns=["pos_top1", "pos_bot1", "pos_top2", "pos_bot2"]
    position_rect_sc.append(rect_pos)

    # Envoyer un message pendant l'expérience
    tracker.log("SENTENCE NUMBER {}".format(k))
    while True:

        # On affiche les différents élements (textes, bouttons, etc...) sur la fenêtre win_exp
        back_rect_source.draw()
        back_rect_cible.draw()

        for textbox in text_box_source:
            textbox.draw()

        for textbox in text_box_cible:
            textbox.draw()

        button_rect1.draw()
        button_text1.draw()

        button_rect2.draw()
        button_text2.draw()

        button_rect3.draw()
        button_text3.draw()

        button_rect4.draw()
        button_text4.draw()

        button_square_next.draw()
        button_next.draw()

        button_remove.draw()
        button_text_remove.draw()

        # Récupérer les coordonnées de la souris
        mouse_x, mouse_y = event.Mouse().getPos()
        # Récupérer les clics de la souris
        # renvoie [0, 0, 0] avec un 1 si une des touches de la souris est pressée
        mouse_cliked = event.Mouse().getPressed(getTime=True)[0]

        # Récupération de la position de la souris à chaque clic
        if any(mouse_cliked):
            tracker.log("MOUSECLICK {} {}".format(mouse_x, mouse_y))

        # Sélection des erreurs dans la phrase source - Surligner
        for i in range(len(dimensions_words_source)):
            if ((dimensions_words_source[i][0] - dimensions_words_source[i][2]/2) <= mouse_x <= (dimensions_words_source[i][0] + dimensions_words_source[i][2]/2)) and ((dimensions_words_source[i][1] - dimensions_words_source[i][3]/2) <= mouse_y <= (dimensions_words_source[i][1] + dimensions_words_source[i][3]/2) and any(mouse_cliked)):
                if highlight_color == None:  # Cas REMOVE
                    text_box_source[i].setTextGridLineColor(highlight_color)  # Supprime la couleur de la grille
                    text_box_source[i].setFontColor([-1, -1, -1])  # 'black"
                    text_box_source[i].setBorderColor(None)  # Supprime les bordures
                    text_box_source[i].setBackgroundColor(highlight_color)  # Supprime la couleur de fond
                else:
                    if highlight_color == color1:
                        text_box_source[i].setBackgroundColor(highlight_color)  # Surligne le fond du mot
                    elif highlight_color == color2:
                        text_box_source[i].setBorderColor(highlight_color)  # Surligne les bordures du mot
                    elif highlight_color == color3:
                        text_box_source[i]._italic = True
                        text_box_source[i].setFontColor(highlight_color) # Change la couleur des lettres du mot
                    elif highlight_color == color4:  
                        text_box_source[i].setTextGridLineColor(highlight_color) # Surlignes les bordures des lettres

                win_exp.flip(clearBuffer=False)
        
        # Sélection des erreurs dans la phrase cible - Surligner
        for j in range(len(dimensions_words_cible)):
            if ((dimensions_words_cible[j][0] - dimensions_words_cible[j][2]/2) <= mouse_x <= (dimensions_words_cible[j][0] + dimensions_words_cible[j][2]/2)) and ((dimensions_words_cible[j][1] - dimensions_words_cible[j][3]/2) <= mouse_y <= (dimensions_words_cible[j][1] + dimensions_words_cible[j][3]/2)) and any(mouse_cliked):
                if highlight_color == None:  # Cas REMOVE
                    text_box_cible[j].setTextGridLineColor(
                        highlight_color)  # Supprime la couleur de la grille
                    text_box_cible[j].setFontColor([-1, -1, -1])  # 'black"
                    text_box_cible[j].setBorderColor(
                        None)  # Supprime les bordures
                    text_box_cible[j].setBackgroundColor(
                        highlight_color)  # Supprime la couleur de fond
                else:
                    if highlight_color == color1:
                        text_box_cible[j].setBackgroundColor(
                            highlight_color)  # Surligne le fond du mot
                    elif highlight_color == color2:
                        
                        text_box_cible[j].setBorderColor(highlight_color) # Surligne les bordures du mot
                    elif highlight_color == color3:
                        text_box_cible[j]._italic = True
                        text_box_cible[j].setFontColor(highlight_color) # Change la couleur des lettres du mot
                    elif highlight_color == color4:  
                        text_box_cible[j].setTextGridLineColor(highlight_color) # Surlignes les bordures des lettres

                win_exp.flip(clearBuffer=False)

        # Vérifier si les coordonnées de la souris sont à l'intérieur du rectangle du bouton erreur 1
        if is_mouse_inside_rectangle(mouse_x, mouse_y, button_rect1.pos[0], button_rect1.pos[1], button_rect1.width, button_rect1.height):
            if any(mouse_cliked): # Vérifier si le bouton a été cliqué
                tracker.log("EVENT BUTTON CLICK {}".format(erreur1))
                button_rect1.setFillColor(color1)
                button_rect2.setFillColor('lightgray')
                button_rect3.setFillColor('lightgray')
                button_rect4.setFillColor('lightgray')
                button_remove.setFillColor('lightgray')
                highlight_color = color1

        # Vérifier si les coordonnées de la souris sont à l'intérieur du rectangle du bouton erreur 2
        if is_mouse_inside_rectangle(mouse_x, mouse_y, button_rect2.pos[0], button_rect2.pos[1], button_rect2.width, button_rect1.height):
            if any(mouse_cliked):  # Vérifier si le bouton a été cliqué
                tracker.log("EVENT BUTTON CLICK {}".format(erreur2))
                button_rect2.setFillColor(color2)
                button_rect1.setFillColor('lightgray')
                button_rect3.setFillColor('lightgray')
                button_rect4.setFillColor('lightgray')
                button_remove.setFillColor('lightgray')
                highlight_color = color2

        # Vérifier si les coordonnées de la souris sont à l'intérieur du rectangle du bouton 3
        if is_mouse_inside_rectangle(mouse_x, mouse_y, button_rect3.pos[0], button_rect3.pos[1], button_rect3.width, button_rect1.height):
            if any(mouse_cliked):  # Vérifier si le bouton a été cliqué
                tracker.log("EVENT BUTTON CLICK {}".format(erreur3))
                button_rect3.setFillColor(color3)
                button_rect1.setFillColor('lightgray')
                button_rect2.setFillColor('lightgray')
                button_rect4.setFillColor('lightgray')
                button_remove.setFillColor('lightgray')
                highlight_color = color3

        # Vérifier si les coordonnées de la souris sont à l'intérieur du rectangle du bouton 4
        if is_mouse_inside_rectangle(mouse_x, mouse_y, button_rect4.pos[0], button_rect4.pos[1], button_rect4.width, button_rect1.height):
            if any(mouse_cliked):  # Vérifier si le bouton a été cliqué
                tracker.log("EVENT BUTTON CLICK {}".format(erreur4))
                button_rect4.setFillColor(color4)
                button_rect1.setFillColor('lightgray')
                button_rect2.setFillColor('lightgray')
                button_rect3.setFillColor('lightgray')
                button_remove.setFillColor('lightgray')
                highlight_color = color4

        # Vérifier si les coordonnées de la souris sont à l'intérieur du rectangle du bouton REMOVE
        if is_mouse_inside_rectangle(mouse_x, mouse_y, button_remove.pos[0], button_remove.pos[1], button_remove.width, button_remove.height):
            if any(mouse_cliked):  # Vérifier si le bouton a été cliqué
                tracker.log("EVENT BUTTON CLICK REMOVE")
                highlight = True
                button_remove.setFillColor('gray')
                button_rect1.setFillColor('lightgray')
                button_rect2.setFillColor('lightgray')
                button_rect3.setFillColor('lightgray')
                button_rect4.setFillColor('lightgray')
                highlight_color = None  # Highlight Color lightgray

        # Vérifier si les coordonnées de la souris sont à l'intérieur du rectangle du bouton NEXT
        if is_mouse_inside_rectangle(mouse_x, mouse_y, button_square_next.pos[0], button_square_next.pos[1], button_square_next.width, button_square_next.height):
            # Changer la couleur du rectangle lorsqu'il est survolé par la souris
            button_square_next.setFillColor('gray')
            if any(mouse_cliked):  # Vérifier si le bouton a été cliqué
                tracker.log("EVENT BUTTON CLICK NEXT")
                tracker.log("END SENTENCE {}".format(k))

                # Determiner le nom de la page
                screen_name = generate_new_filename(name_data_folder, "page_exp_.png")
                # Capturer la frame de la fenêtre
                frame_image = win_exp.getMovieFrame()
                # Enregistrer l'image capturée
                frame_image.save(screen_name)
                # Deplacer l'image dans le dossier de l'exp en cours
                move_file(screen_name, data_folder_path)

                break  # On sort de la boucle, et on affiche les phrases suivantes
        else:
            button_square_next.setFillColor('lightgray')

        # Vérifier si la touche 'escape' a été enfoncée pour quitter le programme
        if 'escape' in event.getKeys():
            tracker.log("ERROR 'escape' is pressed")
            # Arret de l'enregistrement des mouvements oculaire et fermeture du tracker
            tracker.stop_recording()
            tracker.close()
            # Fermeture du programme proprement
            core.quit()

        # On rafraichit la fenêtre
        win_exp.flip()

    # On récupère toutes les erreurs sélectionnées dans le screen courant avant d'afficher le screen suivant 
    # Ces données sont stockés dans les listes results_source et results_cible pour le fichier data_exp.csv utilisé dans analysis.py
    position_err_source = [None]
    for i in range(len(text_box_source)):
        if text_box_source[i].getBackgroundColor() == color1:  # erreur1
            coord_source[erreur1 + " coord source"][k].append([text_box_source[i].getPosition()[0] + screen_width/2, - text_box_source[i].getPosition()[1] + screen_height/2, text_box_source[i].getSize()[0], text_box_source[i].getSize()[1]])
            # Couleur Yellow : Ajouter le texte en jaune
            if -1 in position_err_source:
                results_source[erreur1 + " source"][k] += "&& "
                position_err_source = [x for x in position_err_source if x != -1]
            results_source[erreur1 + " source"][k] += text_box_source[i].getText() + " "
            position_err_source.append(1)

        if text_box_source[i].getBorderColor() == color2:  # erreur2
            coord_source[erreur2 + " coord source"][k].append([text_box_source[i].getPosition()[0] + screen_width/2, - text_box_source[i].getPosition()[1]  + screen_height/2, text_box_source[i].getSize()[0], text_box_source[i].getSize()[1]])
            # Couleur Red : Ajouter le texte en rouge
            if -2 in position_err_source:
                results_source[erreur2 + " source"][k] += "&& "
                position_err_source = [x for x in position_err_source if x != -2]
            results_source[erreur2 + " source"][k] += text_box_source[i].getText() + " "
            position_err_source.append(2)

        if text_box_source[i].getFontColor() == color3:  # erreur3
            coord_source[erreur3 + " coord source"][k].append([text_box_source[i].getPosition()[0] + screen_width/2, - text_box_source[i].getPosition()[1]  + screen_height/2, text_box_source[i].getSize()[0], text_box_source[i].getSize()[1]])
            # Couleur Green : Ajouter le texte en vert
            if -3 in position_err_source:
                results_source[erreur3 + " source"][k] += "&& "
                position_err_source = [x for x in position_err_source if x != -3]
            results_source[erreur3 + " source"][k] += text_box_source[i].getText() + " "
            position_err_source.append(3)

        if text_box_source[i].getTextGridLineColor() == color4:  # erreur4
            coord_source[erreur4 + " coord source"][k].append([text_box_source[i].getPosition()[0] + screen_width/2, - text_box_source[i].getPosition()[1]  + screen_height/2, text_box_source[i].getSize()[0], text_box_source[i].getSize()[1]])
            if -4 in position_err_source:
                results_source[erreur4 + " source"][k] += "&& "
                position_err_source = [x for x in position_err_source if x != -4]

            # Couleur Blue : Ajouter le texte en bleu
            results_source[erreur4 + " source"][k] += text_box_source[i].getText() + " "
            position_err_source.append(4)

        if text_box_source[i].getBackgroundColor() != color1 and 1 in position_err_source:
            position_err_source.append(-1)
            position_err_source = [x for x in position_err_source if x != 1]
        if text_box_source[i].getBorderColor() != color2 and 2 in position_err_source:
            position_err_source.append(-2)
            position_err_source = [x for x in position_err_source if x != 2]
        if text_box_source[i].getFontColor() != color3 and 3 in position_err_source:
            position_err_source.append(-3)
            position_err_source = [x for x in position_err_source if x != 3]
        if text_box_source[i].getTextGridLineColor() != color4 and 4 in position_err_source:
            position_err_source.append(-4)
            position_err_source = [x for x in position_err_source if x != 4]

    position_err_cible = [None]
    for i in range(len(text_box_cible)):

        if text_box_cible[i].getBackgroundColor() == color1:  # erreur1
            coord_cible[erreur1 + " coord cible"][k].append([text_box_cible[i].getPosition()[0] + screen_width/2, - text_box_cible[i].getPosition()[1] + screen_height/2, text_box_cible[i].getSize()[0], text_box_cible[i].getSize()[1]])
            if -1 in position_err_cible:
                results_cible[erreur1 + " cible"][k] += "&& "
                position_err_cible = [x for x in position_err_cible if x != -1]

            # Couleur Yellow : Ajouter le texte en jaune
            results_cible[erreur1 + " cible"][k] += text_box_cible[i].getText() + " "
            position_err_cible.append(1)

        if text_box_cible[i].getBorderColor() == color2:  # erreur2
            coord_cible[erreur2 + " coord cible"][k].append([text_box_cible[i].getPosition()[0] + screen_width/2, - text_box_cible[i].getPosition()[1] + screen_height/2, text_box_cible[i].getSize()[0], text_box_cible[i].getSize()[1]])
            if -2 in position_err_cible:
                results_cible[erreur2 + " cible"][k] += "&& "
                position_err_cible = [x for x in position_err_cible if x != -2]

            # Couleur Red : Ajouter le texte en rouge
            results_cible[erreur2 + " cible"][k] += text_box_cible[i].getText() + " "
            position_err_cible.append(2)

        if text_box_cible[i].getFontColor() == color3:  # erreur3
            coord_cible[erreur3 + " coord cible"][k].append([text_box_cible[i].getPosition()[0] + screen_width/2, - text_box_cible[i].getPosition()[1] + screen_height/2, text_box_cible[i].getSize()[0], text_box_cible[i].getSize()[1]])
            if -3 in position_err_cible:
                results_cible[erreur3 + " cible"][k] += "&& "
                position_err_cible = [x for x in position_err_cible if x != -3]

            # Couleur Green : Ajouter le texte en vert
            results_cible[erreur3 + " cible"][k] += text_box_cible[i].getText() + " "
            position_err_cible.append(3)

        if text_box_cible[i].getTextGridLineColor() == color4:  # erreur4
            coord_cible[erreur4 + " coord cible"][k].append([text_box_cible[i].getPosition()[0] + screen_width/2, - text_box_cible[i].getPosition()[1] + screen_height/2, text_box_cible[i].getSize()[0], text_box_cible[i].getSize()[1]])
            if -4 in position_err_cible:
                results_cible[erreur4 + " cible"][k] += "&& "
                position_err_cible = [x for x in position_err_cible if x != -4]

            # Couleur Blue : Ajouter le texte en bleu
            results_cible[erreur4 + " cible"][k] += text_box_cible[i].getText() + " "
            position_err_cible.append(4)

        if text_box_cible[i].getBackgroundColor() != color1 and 1 in position_err_cible:
            position_err_cible.append(-1)
            position_err_cible = [x for x in position_err_cible if x != 1]
        if text_box_cible[i].getBorderColor() != color2 and 2 in position_err_cible:
            position_err_cible.append(-2)
            position_err_cible = [x for x in position_err_cible if x != 2]
        if text_box_cible[i].getFontColor() != color3 and 3 in position_err_cible:
            position_err_cible.append(-3)
            position_err_cible = [x for x in position_err_cible if x != 3]
        if text_box_cible[i].getTextGridLineColor() != color4 and 4 in position_err_cible:
            position_err_cible.append(-4)
            position_err_cible = [x for x in position_err_cible if x != 4]


# Envoyer un message à la fin de l'expérience
tracker.log("End of experiment")

# Arrêter l'enregistrement des données
tracker.stop_recording()


""" 
Fin de l'expérimentation
"""

# Création de la dernière fenêtre de remerciements le temps de sauvegarder les données
win_exp.flip()
text_stim = visual.TextStim(win_exp, text="Thank you for your participation !", font="consolas", color='black')
text_stim.draw()
win_exp.flip()

# dataframe pour les positions des rect source et cible
df_post_rect = pd.DataFrame(position_rect_sc, columns=["pos_top1", "pos_bot1", "pos_top2", "pos_bot2"])
# Stockage des positions top et bottom des rect source et cible dans le dossier donnees_exp* sous format  .csv
file_name = "data_rect_pos.csv"
csv_path = os.path.join(name_data_folder, file_name)
df_post_rect.to_csv(csv_path, index_label=False)

# Convertion en DataFrame des resultats pour les erreurs surlignés
dfs = pd.DataFrame(results_source)
dfc = pd.DataFrame(results_cible)
# Concaténer les DataFrames en colonne, groupés par le numero de la colonne "phrase"
df = pd.concat([dfs, dfc], axis=1)
# Stockage des données dans le dossier data sous format  .csv
file_name = "data_exp.csv"
csv_path = os.path.join(name_data_folder, file_name)
df.to_csv(csv_path, index_label=False)


# Convertion en DataFrame des coordonnées des erreurs surlignés
dfs_coord = pd.DataFrame(coord_source)
dfc_coord = pd.DataFrame(coord_cible)
# Concaténer les DataFrames en colonne
df_coord = pd.concat([dfs_coord, dfc_coord], axis=1)
# Stockage des données dans le dossier data sous format  .csv afin d'analyser le FP/TP de chaque mots sélectionné
file_name = "df_coord.csv"
csv_path = os.path.join(name_data_folder, file_name)
df_coord.to_csv(csv_path, index_label = False)


# Fermeture de l'eyetracker et téléversement des données
tracker.close()

# Enregistrement des donnees en sortie du eyelink dans le dossier de l'exp
file_name = "data_eyelink.edf"
rename_file("default.edf", file_name)
move_file(file_name, data_folder_path)

# Convertion du fichier .edf to .asc
# ATTENTION! : Les chemins du fichier funtions.py sont aussi à mettre à jour en fonction du poste d'expérimentation
file_path = os.path.join(name_data_folder, file_name)
edf2asc(file_path, r"C:\Program Files (x86)\SR Research\EyeLink\EDF_Access_API\Example\edf2asc.exe")

# Fermeture de la dernière fenêtre et fin du programme
win_exp.close()

core.quit()
