# PROJET QUESTIONNAIRE V3 : POO
#
# Question
#    - titre       - str
#    - choix       - (str)
#    - bonne_reponse   - str
#
#    - poser()  -> bool
#
# Questionnaire
#    - questions      - (Question)
#
#    - lancer()
#

import json
import sys
import pathlib

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data):
        # Transforme les donnees choix tuple (titre, bool 'bonne reponse') -> [choix1, choix2,...]
        choix = [i[0] for i in data["choix"]]
        # Trouve le bon choix en fonction du bool 'bonne reponse'
        bonne_reponse = [i[0] for i in data["choix"] if i[1]]
        # si aucune bonne reponse ou plusieurs bonnes reponses -> anomalie dans les donnees
        if len(bonne_reponse) != 1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser(self, num_question, nombre_questions):
        print(f"QUESTION {num_question} / {nombre_questions}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions  =   questions
        self.categorie  =   categorie
        self.titre      =   titre   
        self.difficulte =   difficulte

    def from_json_data (data):
        questionnaire_data_questions = data["questions"]
        questions = [Question.from_json_data(i) for i in questionnaire_data_questions]
       
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])

    def from_json_file(filename):
        try:
            # charger un fichier json valide
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            questionnaire_data = json.loads(json_data)
        except Exception:
            print("Erreur lors de l'ouverture ou de la lecture du fichier! ")
            return None

        return Questionnaire.from_json_data(questionnaire_data)

    def lancer(self):
        score            =  0
        nombre_questions =  len(self.questions)
        print("-------------")
        print("QUESTIONNAIRE    : "+ self.titre)
        print("    Categorie    : "+ self.categorie)
        print("    Difficulte   : "+ self.difficulte)
        print("    Nombre de questions: "+ str(nombre_questions))
        print("-------------")

        for i in range(nombre_questions):
            question = self.questions[i]
            if question.poser(i+1, nombre_questions):
                score += 1
        print("Score final :", score, "sur", nombre_questions)
        return score

# Questionnaire.from_json_file("cinema_starwars_debutant.json").lancer()

if len(sys.argv) < 2:
    print("ERREUR: Vous devez specifier le nom du fichier json a charger !")
    exit(0)

json_filename = sys.argv[1]
path = pathlib.Path(json_filename)
if path.suffix != ".json":
    print("ERREUR: Le fichier specifié doit avoir l'extension .json !")
    exit(0)

questionnaire = Questionnaire.from_json_file(json_filename)
if questionnaire:
    questionnaire.lancer()