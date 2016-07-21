""" 
 This is ze model.
  
"""
from system.core.model import Model

class Verification(Model):
    def __init__(self):
        super(Verification, self).__init__()

    def flasher(self, data):
        flash_code=0
        if len(data['first_name']) <2:
            flash_code=1
            return flash_code
        elif len(data['last_name']) <2:
            flash_code=2
            return flash_code
        elif len(data['email']) < 1:
            flash_code=3
            return flash_code
        elif data['password'] != data['confirmation']:
            flash_code=4
            return flash_code

    def encrypt(self, data):
        pw_hash = self.bcrypt.generate_password_hash(data['password'])

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
        data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email' : data['email'],
            'password': pw_hash
            }
        return self.db.query_db(query, data)

    def matching(self, data):

        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {
            'email':data['email'],
            'password':data['password']
            }

        user = self.db.query_db(user_query, user_data)[0]
        session['user']= user
        if user:

            if self.bcrypt.check_password_hash(user['password'], data['password']):
                response = True
                return response
            else:
                response = False
                return response
    
        