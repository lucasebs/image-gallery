from werkzeug.security import check_password_hash

class User():

    # def __init__(self, username, couple):
    #     self.username = username
    #     self.couple = couple

    def __init__(self, user):
        self.username = user['_id']
        self.couple = user['couple']
        self.name = user['name']

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def get_name(self):
        return self.name

    def is_couple(self):
        return self.couple

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)