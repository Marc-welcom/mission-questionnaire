from fileinput import filename
from multiprocessing.dummy import Value
from re import I
import unittest
from unittest.mock import patch
import questionnaire
import os
import questionnaire_import
import json

def additionner(a, b):
    return a+b

def conversion_nombre():
    num_str = input("Rentrez un nombre: ")
    return int(num_str)

class TestsUnitaireDemo(unittest.TestCase):
    # sert a preparer les donnees avant chaque test
    def setUp(self) -> None:
        print("SetUp")
        return super().setUp()

     # sert a nettoyer les donnees apres chaque test
    def tearDown(self) -> None:
        print("tearDown")
        return super().tearDown()

    def test_additionner1(self):
        print("test_additionner1")
        self.assertEqual(additionner(5,10),15)

    def test_additionner2(self):
        print("test_additionner2")
        self.assertEqual(additionner(16, 20), 36)
    
    def test_conversion_nombre(self):
        print("test_conversion_nombre")
        with patch("builtins.input", return_value="10"):
            self.assertEqual(conversion_nombre(), 10)
        with patch("builtins.input", return_value="101"):
            self.assertEqual(conversion_nombre(), 101)

    def test_conversion_entree_invalide(self):
        print("test_conversion_entree_invalide")
        with patch("builtins.input", return_value="abjce"):
            self.assertRaises(ValueError, conversion_nombre)

class TestsQuestion(unittest.TestCase):
    def test_question_bonne_mauvaise_reponse(self):
        choix =("choix1", "choix2", "choix3")
        q= questionnaire.Question("titre_question", choix, "choix2")
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser(1,1))
        with patch("builtins.input", return_value="2"):
            self.assertTrue(q.poser(1,1))
        with patch("builtins.input", return_value="3"):
            self.assertFalse(q.poser(1,1))

class TestsQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join("test_data", "cinema_alien_debutant.json")
        q= questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
       
        # nombre de questions
        self.assertEqual(len(q.questions), 10)
        # titre, categorie, difficulte
        self.assertEqual(q.titre, "Alien")
        self.assertEqual(q.categorie, "Cinéma")
        self.assertEqual(q.difficulte, "débutant")
        # patcher le input -> forcer de toujours repondre a 1 -> score = 4
        # lancer
        with patch("builtins.input", return_value="1"):
            self.assertEqual(q.lancer(), 1)

    def test_questionnaire_format_invalide(self):
        filename = os.path.join("test_data", "format_invalide1.json")
        q= questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q.categorie, "inconnue")
        self.assertEqual(q.difficulte, "inconnue")
        self.assertIsNotNone(q.questions)

        filename = os.path.join("test_data", "format_invalide2.json")
        q= questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)

        filename = os.path.join("test_data", "format_invalide3.json")
        q= questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)

class TestsImportQuestionnaire(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050634995/OpenQuizzDB_050/openquizzdb_50.json")
        filenames = ("animaux_leschats_confirme.json", "animaux_leschats_debutant.json", "animaux_leschats_expert.json")

        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            
            try:
                data = json.loads(json_data)
            except:
                self.fail("Probleme de deserialisation pour le fichier " + filename)
            
            # TESTS A INCLURE
            # Pour chaque questionnaire, verifier qu'il contient:
            #   -> titre, questions, difficulte, categorie
            # Pour chaque question, verifier qu'elle contient:
            #   -> titre, choix
            # Pour chaque choix 
            #       -> longueur du titre >0
            #       -> 2eme champs est bien un bool isInstance(..., bool)
            #       -> il ya bien une seule bonne reponse
    
            self.assertIsNotNone(data.get("titre"))
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("difficulte"))
            self.assertIsNotNone(data.get("categorie"))
            
            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))

                for choix in question.get("choix"):
                    self.assertGreater(len(choix[0]), 0)
                    self.assertTrue(isinstance(choix[1], bool))
                bonne_reponse = [i[0] for i in question.get("choix") if i[1]]
                self.assertEqual(len(bonne_reponse), 1)

unittest.main()