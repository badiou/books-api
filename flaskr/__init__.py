from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random
from models import setup_db, Book

BOOKS_PER_SHELF = 8


def paginate_books(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * BOOKS_PER_SHELF
  end = start + BOOKS_PER_SHELF
  books = [book.format() for book in selection]
  current_books = books[start:end]

  return current_books

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/books')
  def get_all_books():
    books=Book.query.order_by(Book.id).all()
    current_books=paginate_books(request,books)
    if len(current_books)==0:
          abort(404)
    return jsonify({
      'success':True,
      'books':current_books,
      'total_books':len(Book.query.all())
    })

  @app.route('/books/<int:book_id>')
  def get_one_book(book_id):
    book=Book.query.filter(Book.id==book_id).one_or_none()
    if book is None:
      abort(404)
    else:
      return jsonify({
        'success':True,
        'book':book.format()
      })

  @app.route('/books/<int:book_id>',methods=['PATCH'])
  def update_book(book_id):
    body=request.get_json()
    try:
      book=Book.query.filter(Book.id==book_id).one_or_none()
      if book is None:
            abort(404)
      if 'rating' in body:
            book.rating=int(body.get('rating'))
      book.update()
      return jsonify({
        'success':True,
        'id':book.id
      })
    except:
      abort(400) # Bad request. The user send request that server could not be understand

  @app.route('/books/<int:book_id>',methods=['DELETE'])
  def delete_book(book_id):
    try:
      book=Book.query.filter(Book.id==book_id).one_or_none()
      if book is None:
        abort(404)
      book.delete()
      selection=Book.query.order_by(Book.id).all()
      current_books=paginate_books(request,selection)
      return jsonify({
        'success':True,
        'deleted':book_id,
        'books':current_books,
        'total_books':len(Book.query.all())
      })
    except:
      abort(422) #Unprocessable Entity


  @app.route('/books',methods=['POST'])
  def create_book():
    body=request.get_json()

    new_title=body.get('title',None)
    new_author=body.get('author',None)
    new_rating=body.get('rating',None)
    search=body.get('search',None)
    try:
      if search:
        selection=Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
        current_books=paginate_books(request,selection)
        
        return jsonify({
          'success':True,
          'books':current_books,
          'total_books':len(selection.all())

        })
      else:     
        book=Book(title=new_title, author=new_author, rating=new_rating)
        book.insert()

        selection=Book.query.order_by(Book.id).all()
        current_books=paginate_books(request,selection)

        return jsonify({
          'success':True,
          'created':book.id,
          'books':current_books,
          'total_books':len(Book.query.all())
        })
    except:
      abort(422)

  @app.errorhandler(404)
  #ici on fait un get et la ressource n'existe pas http://localhost:5000?page=100
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404


  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      "error":422,
      "message":"unprocessable"
    }),422
  
  @app.errorhandler(400)
  #Curl -X PATCH http://localhost:5000/books/1000 -H "Content-Type:application/json" -d "{\"rating\": \"2\"}"
  def error_client(error):
    return jsonify({
      'success':False,
      "error":400,
      "message":"Bad request"
    }),400

  @app.errorhandler(405)
  #ici on veut envoyer un post sur une route qui donne des erreurs POST /books/6... On ne peut pas faire de post sur cette route....
  def error_badRequest(error):
        return jsonify({
          'success':False,
          "error":405,
          "message":"Method not allowed"
        }),405


  return app


#ici en bas c'est un exemple pour les test unitaires

# class AppNameTestCase(unittest.TestCase):
#     """This class represents the ___ test case"""

#     def setUp(self):
#         """Executed before each test. Define test variables and initialize app."""
#         self.client = app.test_client
#         pass

#     def tearDown(self):
#         """Executed after reach test"""
#         pass

#     def test_given_behavior(self):
#         """Test _____________ """
#         res = self.client().get('/')

#         self.assertEqual(res.status_code, 200)

# # Make the tests conveniently executable
# if __name__ == "__main__":
# unittest.main()