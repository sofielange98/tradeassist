from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_info):

        self.username = user_info['username']
        self.password = generate_password_hash(user_info['password'])
        self.email = user_info['email']
        self._is_logged_in = False
        self.strategies = None
        self.unique_id_to_inc = {}

        error = None
        if not self.username:
            error = 'Username is required.'
        elif not self.password:
            error = 'Password is required.'
        elif not self.email:
            error = "Email is required."
        self.error = error

        try:
            self.id = user_info['id'] 
        except:
            pass

    def login(self, password):
        if check_password_hash(self.password,password):
            self._is_logged_in = True
            return True
        else:
            return False
    
    def check_strategy_exists(self, form):
        for strat in self.strategies:
            if strat['name'] == form['strategy'] and strat['symbol'] == form['symbol'] and strat['interim'] == form['frequency']:
                return True
            else: 
                return False

    def update_strategies(self, db_rows):
        ct = 1
        for strat in db_rows:
            self.unique_id_to_inc[strat['id']] = ct
            ct += 1
            
    def __repr__(self):
        return '<User {}, Email {}>'.format(self.username, self.email)


