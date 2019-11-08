from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_info):

        self.username = user_info['username']
        self.password = generate_password_hash(user_info['password'])
        self.email = user_info['email']
        error = None
        if not self.username:
            error = 'Username is required.'
        elif not self.password:
            error = 'Password is required.'
        elif not self.email:
            error = "Email is required."
        self.error = error

        try:
            self.indicators = user_info.getlist('indicator')
            self.frequencies = []
            self.symbols = []
            print(self.indicators)
            for indicator in self.indicators:
                self.frequencies.append(user_info[indicator+'_frequency'])
                self.symbols.append(user_info[indicator + '_symbol'])
        except:
            self.id = user_info['id'] 

    def valid_user_password(self, password):
        return(check_password_hash(self.password,password))
        
    def __repr__(self):
        return '<User {}>'.format(self.username)


