class PartialUser:
    username = str
    id = int
    global_name = str
    avatar = str


class UserParams(PartialUser):
    ...
    
class User(UserParams):
    def block(self):
        ...



