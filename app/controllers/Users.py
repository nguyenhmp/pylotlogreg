"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('Verification')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def create(self):

        ##### Request Form Handler
        data={
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email' : request.form['email'],
            'password': request.form['password'],
            'confirmation': request.form['confirmation']
             }
        flash_code = self.models['Verification'].flasher(data)
       

        ##### Flash response from verifying account inputs
        if flash_code == 0:
            flash("You have successfully created your account!")
        elif flash_code == 1:
            flash("First name field cannot be blank")
            return redirect('/')
        elif flash_code == 2:
            flash("Last name field cannot be blank")
            return redirect('/')
        elif flash_code == 3:
            flash("You must enter a valid email address.")
            return redirect('/')
        elif flash_code == 4:
            flash("Your password and confirmation do not match.  Please re-enter your password.")
            return redirect('/')

        self.models['Verification'].encrypt(data)

        return self.load_view('success.html', data=data)


    def login(self):
        print "something is working"

        #### Packaging data from the request form to send to def matching() modelfor verfication.
        data={
            'email': request.form['email'],
            'password': request.form['password']
            }
        #### Flashing responses to the verfication model and redirecting to either success.html or back to the login screen.

        response = self.models['Verification'].matching(data)
        if response == False:
            flash(" The information you have answered does not match our database.  Please try again or register for a new account.")
            return redirect('/')
        elif response == True:
            flash ("You have successfully logged into your account.")
            return self.load_view('success.html', data=data)
    



