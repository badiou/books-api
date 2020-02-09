import os
import unittest
import json
from flaskr import create_app
from models import setup_db, Book



class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

#Cette méhode est et initialise les variables necessaires pour faire les tests
    def setUp(self):
        """define test variables and initialize app. Elle est exécutée avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path="postgresql://{}:{}@{}/{}".format('postgres','badiou','localhost:5432',self.database_name)
        setup_db(self.app,self.database_path)

        self.new_book={
            'title':'Miracle morning',
            'author':'Hal Elrod',
            'rating':5
        }


#cette methode est éxecutée après chaque test
    def tearDown(self):
        """Cette fonction est exécutée apres chaque test"""
        pass



#ici on fait le test pour récupérer la liste des books enregistrés dans la base de données
    def test_get_paginated_books(self):
        res=self.client().get('/books')
        data=json.loads(res.data) #ici on recupère la données provenant de la response
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'],True)
        self.assertTrue(data['books']) 
        self.assertTrue(len(data['books']))


#ici on demande une page à la limite du nombre de pages disponibles
    def test_404_send_requesting_beyond_the_value_page(self):
        res=self.client().get('/books?page=1000',json={'rating': 1})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not found')


#ici on fait la la mise à jour d'un champ de la table en passant la données json
    def test_update_book_rating(self):
        res=self.client().patch('/books/5',json={'rating':1})
        data=json.loads(res.data)
        book=Book.query.filter(Book.id==5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(book.format()['rating'],1)

#ici on veut faire la mise à jour mais on omet de donner le parametre à modifier et la valeur
    def test_400_failed_for_update(self):
        res=self.client().patch('/books/5')#ici on ne donne pas le parametre qu'on veut modifier
        data=json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Bad request')

    
#ici on fait le test par rapport à la suppression
    def test_delete_book(self):
        res=self.client().delete('/books/1')
        data=json.loads(res.data)

        book=Book.query.filter(Book.id==1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True) 
        self.assertEqual(data['deleted'],1)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
        self.assertEqual(book,None)


#ici c'est qu'on veut supprimer un book qui n'existe pas
    def test_422_if_book_deos_not_exist(self):
        res=self.client().delete('/books/1000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')

#ici on veut créer un book
    def test_create_new_book(self):
        res=self.client().post('/books',json=self.new_book)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'],True) 
        self.assertTrue(data['created'])
        self.assertTrue(len(data['books']))

#ici on veut créer un book. Seulement l'URl fournit n'est pas le bon books/45
    def test_405_if_book_creation_not_allowed(self):
        res=self.client().post('/books/45',json=self.new_book)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 405) 
        self.assertTrue(data['success'],False) 
        self.assertTrue(data['message'],'method not allowed') 

    
    def test_get_book_search_with_results(self):
        res=self.client().post('/books',json={'search':'Novel'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'],True) 
        self.assertTrue(data['total_books'])
        self.assertEqual(len(data['books']),6)  #4 est le nombre de fois que Novel existe dans la base de données...

    def test_get_book_search_without_results(self):
        res=self.client().post('/books',json={'search':'applejacks'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'],True) 
        self.assertEqual(data['total_books'],0) #0 veut dire que le livre recherché n'existe pas dans la base de données....
        self.assertEqual(len(data['books']),0)  


if __name__ == "__main__":
    unittest.main()

        



    
            
        

        
