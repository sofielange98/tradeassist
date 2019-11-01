from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, request):
    	self.username = request.form['username']
        self.password = generate_password_hash(request.form['password'])
        self.email = request.form['email']
    	error = None
        if not self.username:
            error = 'Username is required.'
        elif not self.password:
            error = 'Password is required.'
        elif not self.email:
            error = "Email is required."
        self.error = error

        self.indicators = request.form.getlist('indicator')
        self.frequencies = []
        self.symbols = []
        for indicator in indicators:
            self.frequencies.append(request.form[indicator+'_frequency'])
            self.symbols.append(request.form[indicator + '_symbol'])


    def __repr__(self):
        return '<User {}>'.format(self.username)

