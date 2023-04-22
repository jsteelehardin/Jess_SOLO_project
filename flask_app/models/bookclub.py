# Import mysqlconnection config
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user

"""
Change class construct, queries, and db for bookclub
"""

class Bookclub:
    # Use a alias for the database; call in classmethods as cls.db
    # For staticmethod need to call the database name not alias
    db = "bookclubfav2"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # Needed to create this to capture the creator of the bookclub
        self.creator = None
        self.user_ids_who_favsubscribed = []
        self.users_who_favsubscribed = []

    # CRUD CREATE METHODS
    @classmethod
    def create_bookclub(cls,data):
        """Create a bookclub"""
        query = "INSERT INTO bookclubs (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def favsubscribe(cls,data):
        query = "INSERT INTO favsubscriptions (user_id, bookclub_id) VALUES (%(user_id)s, %(id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    # CRUD READ METHODS -- Modified for many to many
    @classmethod
    def get_all_bookclubs(cls):
        """Get all the bookclubs in db"""
        query = '''SELECT * FROM bookclubs
                JOIN users AS creators ON bookclubs.user_id = creators.id
                LEFT JOIN favsubscriptions ON favsubscriptions.bookclub_id = bookclubs.id
                LEFT JOIN users AS users_who_favsubscribed ON favsubscriptions.user_id = users_who_favsubscribed.id;'''
        # query = "SELECT * FROM bookclubs LEFT JOIN users ON bookclubs.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_bookclubs = []
        for r in results:
            new_bookclub = True
            users_who_favsubscribed_data = {
                'id': r['users_who_favsubscribed.id'],
                'first_name': r['users_who_favsubscribed.first_name'],
                'last_name': r['users_who_favsubscribed.last_name'],
                'email': r['users_who_favsubscribed.email'],
                'password': r['users_who_favsubscribed.password'],
                'created_at': r['users_who_favsubscribed.created_at'],
                'updated_at': r['users_who_favsubscribed.updated_at']
            }
            # Check to see if previous processed bookclub, exist as current row
            num_of_bookclub = len(all_bookclubs)
            print(num_of_bookclub)
            # Check to see if we have bookclubs in list
            # If num_of_bookclub is > 0; then we have procesed a row/bookclub
            # already
            if num_of_bookclub > 0:
                # Check if last bookclub equals current row
                last_bookclub = all_bookclubs[num_of_bookclub-1]
                if last_bookclub.id == r['id']:
                    last_bookclub.user_ids_who_favsubscribed.append(r['users_who_favsubscribed.id'])
                    last_bookclub.users_who_favsubscribed.append(user.User(users_who_favsubscribed_data))
                    new_bookclub = False
            # Create new bookclub object if bookclub has not been created
            # and added to the list
            if new_bookclub:
                # Create the bookclub object
                bookclub = cls(r)
                # Create the associated User object; include all contructors
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set user to creator in bookclub
                bookclub.creator = one_user
                # Check to see if any user favsubscribed this bookclub
                if r['users_who_favsubscribed.id']:
                    bookclub.user_ids_who_favsubscribed.append(r['users_who_favsubscribed.id'])
                    bookclub.users_who_favsubscribed.append(user.User(users_who_favsubscribed_data))
                    print(bookclub.users_who_favsubscribed)
                # Append the bookclub to the all_bookclub list
                all_bookclubs.append(bookclub)

        return all_bookclubs

    @classmethod
    def get_one_bookclub(cls,data):
        """Get one bookclub to display"""
        query = '''SELECT * FROM bookclubs
                JOIN users AS creators ON bookclubs.user_id = creators.id
                LEFT JOIN favsubscriptions ON favsubscriptions.bookclub_id = bookclubs.id
                LEFT JOIN users AS users_who_favsubscribed ON favsubscriptions.user_id = users_who_favsubscribed.id 
                WHERE bookclubs.id = %(id)s;'''
        # query = "SELECT * FROM bookclubs LEFT JOIN users ON bookclubs.user_id = users.id WHERE bookclubs.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        # Now due to fav; we can get back multiple rows or no rows (if no fav)
        # So we need to check for both conditions
        # First condition no results; return False
        if len(result) < 1:
            return False
        # Check if multiple rows (or fav)
        # If one row then bookclub so set to True to start
        new_bookclub = True
        for r in result:
            if new_bookclub:
                # If this is the first row
                bookclub = cls(result[0])
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set user to creator in bookclub
                bookclub.creator = one_user
                # Set new_bookclub to False once we create 
                new_bookclub = False
            # if fav data associate it with user
            if r['users_who_favsubscribed.id']:
                users_who_favsubscribed_data = {
                    'id': r['users_who_favsubscribed.id'],
                    'first_name': r['users_who_favsubscribed.first_name'],
                    'last_name': r['users_who_favsubscribed.last_name'],
                    'email': r['users_who_favsubscribed.email'],
                    'password': r['users_who_favsubscribed.password'],
                    'created_at': r['users_who_favsubscribed.created_at'],
                    'updated_at': r['users_who_favsubscribed.updated_at']
                }
                # Create instance of user who fav
                users_who_favsubscribed = user.User(users_who_favsubscribed_data)
                # Add user to users_who_favsubscribed list
                bookclub.users_who_favsubscribed.append(users_who_favsubscribed)
                # Add users_who_favsubscribed id to user_ids_who_favsubscribed list
                bookclub.user_ids_who_favsubscribed.append(r['users_who_favsubscribed.id'])
        return bookclub

    # CRUD UPDATE METHODS
    @classmethod
    def update_bookclub(cls,data):
        """Update the bookclub"""
        query = "UPDATE bookclubs SET title=%(title)s, description=%(description)s WHERE bookclubs.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    

    @classmethod
    def save_bookclub(cls,data):
        query='''
            INSERT INTO bookclubs(user_id, title, description)
            VALUES(%(user_id)s, %(title)s, %(description)s);
        '''
        results= connectToMySQL(cls.db).query_db(query, data)
        return results

    # CRUD DELETE METHODS
    @classmethod
    def delete_bookclub(cls,data):
        """Delete bookclub"""
        query = "DELETE FROM bookclubs WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unfavsubscribe(cls,data):
        query = "DELETE FROM favsubscriptions WHERE user_id=%(user_id)s AND bookclub_id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # FORM VALIDATION
    @staticmethod
    def validate_form(data):
        """Validate the new bookclub create form"""
        is_valid = True # We set True until False
        if len(data['title']) < 5:
            flash("The Title must be at least 5 characters.", "danger")
            is_valid = False
        if len(data['description']) < 10:
            flash("The description must be at least 10 characters.", "danger")
            is_valid = False
        return is_valid

    # insert into
    @classmethod
    def save_bookclub(cls,data):
        query='''
            INSERT INTO bookclubs(user_id, title, description)
            VALUES(%(user_id)s, %(title)s, %(description)s);
        '''
        return connectToMySQL(cls.db).query_db(query, data)


