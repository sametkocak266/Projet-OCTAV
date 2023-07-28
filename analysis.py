import openpyxl, csv
import pandas as pd

# Numero du dossier a visualiser
number_exp = input("ANALYSIS\nEntrez le numero de l'exp : donnees_exp_")
eyelinkfolder = "donnees_exp_"+number_exp+"\data_eyelink.asc"

# On récupère la DataFrame 
df = pd.read_csv("donnees_exp_"+number_exp+"\data_exp.csv") 
n = len(df) # Nombre de phrases durant l'experience

# Dictionnaire pour stocker les donnees d'analyse
data = {
    "eye_data": [[] for _ in range(int(n))],
    "time_screen" : [],
    "time_rect_s" : [0] * n,
    "time_rect_c" : [0] * n,
    "come_and_go" : [0] * n,
    "fixations_buttons" : [],
    "durations_buttons" : [],
    "phrases source" : [],
    "phrases cible" : [],
    "erreur1_source" : [],
    "erreur2_source" : [],
    "erreur3_source" : [],
    "erreur4_source" : [],
    "erreur1_cible" : [],
    "erreur2_cible" : [],
    "erreur3_cible" : [],
    "erreur4_cible" : [],
    "analyses_erreurs_1_s" : [[] for _ in range(int(n))],
    "analyses_erreurs_2_s" : [[] for _ in range(int(n))],
    "analyses_erreurs_3_s" : [[] for _ in range(int(n))],
    "analyses_erreurs_4_s" : [[] for _ in range(int(n))],
    "analyses_erreurs_1_c" : [[] for _ in range(int(n))],
    "analyses_erreurs_2_c" : [[] for _ in range(int(n))],
    "analyses_erreurs_3_c" : [[] for _ in range(int(n))],
    "analyses_erreurs_4_c" : [[] for _ in range(int(n))]

}

# List for calculate the time passed in each screen
time_screen = []

phrase_number = 0 # Saving the fixations for the right screen
start=False # Flag for knowing when we started to draw the first screen and start to save the fixations

with open(eyelinkfolder,'r', encoding='ISO-8859-1') as file :
    for line in file:
        if "DATA" in line:
            if "SCREENSIZE" in line:
                values = line.split()
                screen_width_exp = float(values[5]) # taille ecran de l'exp en longueur
                screen_height_exp = float(values[7]) # taille ecran de l'exp en largeur
                print("SCREENSIZE EXP", screen_width_exp, screen_height_exp)
            if "FONTSIZE" in line:
                values = line.split()
                fontsize_exp = float(values[4]) # taille de la police durant l'exp
                print("FONTSIZE EXP", fontsize_exp)
            if "FIRSTPIX" in line:
                values = line.split()
                first_letter_pix_exp = int(values[4]) # Position of the first letter from the 'left' side of phrases source et cible de l'ecran exp
                print("FIRSTPIX EXP", first_letter_pix_exp)
            if "ERREURS" in line: # Recuperation des noms d'erreurs etudies
                values = line.split()
                erreur1_exp = values[4] # nom de l'erreur1 
                erreur2_exp = values[5] # nom de l'erreur2
                erreur3_exp = values[6] # nom de l'erreur3
                erreur4_exp = values[7] # nom de l'erreur4
            if "YPOS" in line:
                values = line.split()
                ypos_s_exp = float(values[5]) # coord de la position vertical de la phrase source
                ypos_c_exp = float(values[7]) # coord de la position vertical de la phrase cible 
                print("YPOS Source et Cible EXP", ypos_s_exp, ypos_c_exp)
        
        # Calcul du temps dans chaque screen
        if "SENTENCE NUMBER" in line:
            start = True
            phrase_number+=1
            values = line.split()
            data["time_screen"].append(values[1])
        
        # Stocker les données de fixations
        if ("EFIX" in line) and start:
            values = line.split()
            data["eye_data"][phrase_number-1].append([float(values[4]), float(values[5]), float(values[6])])
            
        if "END SENTENCE" in line:
            values = line.split()
            data["time_screen"][phrase_number-1] = int(values[1]) - int(data["time_screen"][phrase_number-1]) # Calcul du temps dans chaque screen
        
        if "EVENT" in line:
            continue
        
        if "ERROR" in line and start:
            print("ERR : Le sujet a appuyer sur la touche 'espcape' durant l'expérience") 

# DATA OF RECT SOURCE AND CIBLE POSITIONS
# List for size of rect source and cible of each screen
rect_pos = []

# Spécifiez le chemin du fichier CSV à lire
chemin_fichier_rect_pos = "donnees_exp_" + number_exp + "\data_rect_pos.csv"

# Ouvrir le fichier CSV en mode lecture
with open(chemin_fichier_rect_pos, 'r') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv)
    # Parcourir les lignes du fichier CSV
    i = 0
    for ligne in lecteur_csv:
        #if i == 0:  en-tête ['pos_top1', 'pos_bot1', 'pos_top2', 'pos_bot2']
        if i>0 : # Top rect S : ligne[1] / Bot rect S : ligne[2], Top rect C : ligne[3], Bot rect C : ligne[4]
            # rect_pos contient les coord des rect S&C (top/bot) dans la meme base que le fichier .asc 
            rect_pos.append([- float(ligne[1]) + screen_height_exp/2, 
                             - float(ligne[2]) + screen_height_exp/2, 
                             - float(ligne[3]) + screen_height_exp/2, 
                             - float(ligne[4]) + screen_height_exp/2
                             ])
        i+=1    

# DATA OF ERROR BUTTONS SIZE AND POSITIONS
# List for size of error buttons
buttons_pos = []

# Spécifiez le chemin du fichier CSV à lire
chemin_fichier_buttons = "donnees_exp_" + number_exp + "\data_buttons.txt"

# Ouvrir le fichier en mode lecture
with open(chemin_fichier_buttons, 'r') as fichiertxt:
    contenu = fichiertxt.readlines()
    for line in contenu:
        #print(line.strip())  # Utilisez strip() pour supprimer les espaces supplémentaires en début/fin de ligne

        if "Dimensions" in line:
            dimension = line.split(":")[-1].strip()  # Récupérez la dimension à droite du ":"
            dimension_x, dimension_y = map(float, dimension.split())

        if erreur1_exp in line:
            erreur1_pos = line.split(":")[-1].strip()
            erreur1_x, erreur1_y = map(float, erreur1_pos.split())

        if erreur2_exp in line:
            erreur2_pos = line.split(":")[-1].strip()
            erreur2_x, erreur2_y = map(float, erreur2_pos.split())

        if erreur3_exp in line:
            erreur3_pos = line.split(":")[-1].strip()
            erreur3_x, erreur3_y = map(float, erreur3_pos.split())

        if erreur4_exp in line:
            erreur4_pos = line.split(":")[-1].strip()
            erreur4_x, erreur4_y = map(float, erreur4_pos.split())


# DATA OF COORD WORD SELECTED
# dictionnaire pour stocker les coordonnées et dimensions des mots sélectionnées
words_coord = {
    "analyses_erreurs_1_s" : [],
    "analyses_erreurs_2_s" : [],
    "analyses_erreurs_3_s" : [],
    "analyses_erreurs_4_s" : [],
    "analyses_erreurs_1_c" : [],
    "analyses_erreurs_2_c" : [],
    "analyses_erreurs_3_c" : [],
    "analyses_erreurs_4_c" : []
}
coord = []
keys = [key for key in words_coord]
# Spécifiez le chemin du fichier CSV à lire
chemin_fichier_coord = "donnees_exp_" + number_exp + "\df_coord.csv"

# Ouvrir le fichier en mode lecture
with open(chemin_fichier_coord, 'r') as fichiercoord:
    lecteur_csv = csv.reader(fichiercoord)
    # Parcourir les lignes du fichier CSV
    for indice, line in enumerate(lecteur_csv):
        if indice == 0:  
            continue #en-tête skiped
        
        for idx, key in enumerate(words_coord):
            if (len(eval(line[idx + 1]))) == 0 :
                words_coord[key].append(eval(line[idx + 1]))
            else :
                for i in range (len(eval(line[idx + 1]))):
                    coord.append([eval(line[idx + 1])[i][0] + eval(line[idx + 1])[i][2]/2, eval(line[idx + 1])[i][0] - eval(line[idx + 1])[i][2]/2, 
                                eval(line[idx + 1])[i][1] + eval(line[idx + 1])[i][3]/2, eval(line[idx + 1])[i][1] - eval(line[idx + 1])[i][3]/2
                                ])
                words_coord[key].append(coord)
            coord = []
        

# ANALYSIS OF COME AND GO BETWEEN RECT SOURCE AND CIBLE AND FIXATION TIME IN BOTH, FIRST PASS TIME AND TOTAL TIME PASSED IN EACH WORD SELECTED DURING THE EXPERIMENT
flag_come_and_go = False
fixation_counts = [0] * 4
duration_fixation_counts = [0] * 4

for screen_number in range(len(data["eye_data"])):    

    for EFIX in data["eye_data"][screen_number]:
        stop = False
        # On vérifie si le regard est dans le rectangle source ou cible
        if rect_pos[screen_number][1] > float(EFIX[2]) > rect_pos[screen_number][0]: # EFIX dans rectangle source
            data["time_rect_s"][screen_number] += EFIX[0]
            flag_come_and_go = False
            
            # On verifie si le regard est dans l'un des mots surlignées dans la phrase source pour le FP/TP
            for key in keys[:4]:
                for coord_err in words_coord[key][screen_number]:
                    if ( coord_err[0] > float(EFIX[1]) > coord_err[1] ) and ( coord_err[2] > float(EFIX[2]) > coord_err[3] ) :
                        if data[key][screen_number] == [] :
                            data[key][screen_number] = [1, float(EFIX[0]), float(EFIX[0])]
                        else :
                            data[key][screen_number][0] +=1
                            data[key][screen_number][2] += float(EFIX[0])
                        stop = True
                        break
                if stop : 
                    stop = False 
                    break 
            
        elif rect_pos[screen_number][3] > float(EFIX[2]) > rect_pos[screen_number][2]: # EFIX dans rectangle cible
            data["time_rect_c"][screen_number] += EFIX[0]
            if not flag_come_and_go:
                flag_come_and_go = True
                data["come_and_go"][screen_number] += 1
            
            # On verifie si le regard est dans l'un des mots surlignées dans la phrase cible pour le FP/TP
            for key in keys[4:]:
                for coord_err in words_coord[key][screen_number]:
                    if ( coord_err[0] > float(EFIX[1]) > coord_err[1] ) and ( coord_err[2] > float(EFIX[2]) > coord_err[3] ) :
                        if data[key][screen_number] == [] :
                            data[key][screen_number] = [1, float(EFIX[0]), float(EFIX[0])]
                        else :
                            data[key][screen_number][0] += 1
                            data[key][screen_number][2] += float(EFIX[0])
                        stop = True
                        break
                if stop : 
                    stop = False 
                    break 

        # On vérifie si le regard est dans l'un des 4 boutons erreurs
        elif (erreur1_x + (dimension_x/2)) > float(EFIX[1]) > (erreur1_x - (dimension_x/2)) and (erreur1_y + (dimension_y/2)) > float(EFIX[2]) > (erreur1_y - (dimension_y/2)):
            fixation_counts[0] += 1
            duration_fixation_counts[0] += EFIX[0]
        elif (erreur2_x + (dimension_x/2)) > float(EFIX[1]) > (erreur2_x - (dimension_x/2)) and (erreur2_y + (dimension_y/2)) > float(EFIX[2]) > (erreur2_y - (dimension_y/2)):
            fixation_counts[1] += 1
            duration_fixation_counts[1] += EFIX[0]
        elif (erreur3_x + (dimension_x/2)) > float(EFIX[1]) > (erreur3_x - (dimension_x/2)) and (erreur3_y + (dimension_y/2)) > float(EFIX[2]) > (erreur3_y - (dimension_y/2)):
            fixation_counts[2] += 1
            duration_fixation_counts[2] += EFIX[0]
        elif (erreur4_x + (dimension_x/2)) > float(EFIX[1]) > (erreur4_x - (dimension_x/2)) and (erreur4_y + (dimension_y/2)) > float(EFIX[2]) > (erreur4_y - (dimension_y/2)):
            fixation_counts[3] += 1
            duration_fixation_counts[3] += EFIX[0]
    data["fixations_buttons"].append(fixation_counts)
    data["durations_buttons"].append(duration_fixation_counts)
    fixation_counts = [0] * 4
    duration_fixation_counts = [0] * 4

# Ouverture d'un classeur Excel pour presenter les resultats de l'analyse
classeur = openpyxl.Workbook()
feuille = classeur.active

# Lire le fichier CSV
chemin_fichier_csv = "donnees_exp_"+number_exp+"\data_exp.csv"

with open(chemin_fichier_csv, 'r', encoding='utf-8') as fichier_csv:
    lecteur_csv = csv.reader(fichier_csv)
    # Parcourir les lignes du fichier CSV
    i = 0
    for ligne in lecteur_csv:
        if i == 0: 
            # Spécifier les en-têtes des colonnes
            en_tetes = [ligne[0], ligne[5], ligne[1], ligne[2], ligne[3], ligne[4], ligne[6], ligne[7], ligne[8], ligne[9], 
                        erreur1_exp + " source (NF, FP, TD)", 
                        erreur2_exp + " source (NF, FP, TD)", 
                        erreur3_exp + " source (NF, FP, TD)", 
                        erreur4_exp + " source (NF, FP, TD)", 
                        erreur1_exp + " cible (NF, FP, TD)", 
                        erreur2_exp + " cible (NF, FP, TD)", 
                        erreur3_exp + " cible (NF, FP, TD)", 
                        erreur4_exp + " cible (NF, FP, TD)", 
                        "Button " + erreur1_exp + " time (ms)", "Number of EFIX in button " + erreur1_exp, 
                        "Button " + erreur2_exp + " time (ms)", "Number of EFIX in button " + erreur2_exp, 
                        "Button " + erreur3_exp + " time (ms)", "Number of EFIX in button " + erreur3_exp, 
                        "Button " + erreur4_exp + " time (ms)", "Number of EFIX in button " + erreur4_exp, 
                        "Screen time (ms)", "Phrase source time (ms)", "Phrase cible time (ms)", "Number of goings and comings between source and cible"]
            feuille.append(en_tetes)
        if i > 0 :
            # Récupérer les valeurs spécifiques
            data["phrases source"].append(ligne[1] if ligne[1] != '' else None)
            data["erreur1_source"].append(ligne[2] if ligne[2] != '' else None)
            data["erreur2_source"].append(ligne[3] if ligne[3] != '' else None)
            data["erreur3_source"].append(ligne[4] if ligne[4] != '' else None)
            data["erreur4_source"].append(ligne[5] if ligne[5] != '' else None)
            data["phrases cible"].append(ligne[6] if ligne[6] != '' else None)
            data["erreur1_cible"].append(ligne[7] if ligne[7] != '' else None)
            data["erreur2_cible"].append(ligne[8] if ligne[8] != '' else None)
            data["erreur3_cible"].append(ligne[9] if ligne[9] != '' else None)
            data["erreur4_cible"].append(ligne[10] if ligne[10] != '' else None)
        i+=1
    
    # Séparer les données en fonction du type et de l'erreur
    if len(data["erreur1_source"]) != len(data["erreur1_cible"]): 
        print("Erreur nombre de phrases source et cible")
    
    # Adding data in analysis.xlsx 
    for k in range(len(data["erreur1_source"])):
        ligne_excel = [
            data["phrases source"][k],
            data["phrases cible"][k],
            data["erreur1_source"][k],
            data["erreur2_source"][k],
            data["erreur3_source"][k],
            data["erreur4_source"][k],
            data["erreur1_cible"][k],
            data["erreur2_cible"][k],
            data["erreur3_cible"][k],
            data["erreur4_cible"][k], 
            str(data["analyses_erreurs_1_s"][k]),
            str(data["analyses_erreurs_2_s"][k]),
            str(data["analyses_erreurs_3_s"][k]),
            str(data["analyses_erreurs_4_s"][k]),
            str(data["analyses_erreurs_1_c"][k]),
            str(data["analyses_erreurs_2_c"][k]),
            str(data["analyses_erreurs_3_c"][k]),
            str(data["analyses_erreurs_4_c"][k]),
            data["durations_buttons"][k][0],
            data["fixations_buttons"][k][0],
            data["durations_buttons"][k][1],
            data["fixations_buttons"][k][1],
            data["durations_buttons"][k][2],
            data["fixations_buttons"][k][2],
            data["durations_buttons"][k][3],
            data["fixations_buttons"][k][3],
            data["time_screen"][k],
            data["time_rect_s"][k],
            data["time_rect_c"][k],
            data["come_and_go"][k]
        ]
        feuille.append(ligne_excel)

# Enregistrer le classeur Excel
chemin_fichier_xlsx = "donnees_exp_"+number_exp+"/analysis.xlsx"
classeur.save(chemin_fichier_xlsx)

# Fermer le classeur
classeur.close()

print("Data analysis completed, find it in the file analyses.xlsx")