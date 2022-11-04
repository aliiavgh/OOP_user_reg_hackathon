import json 


def validate_password(password): 
    if len(password) < 8:
        raise Exception('Пароль слишком короткий!')
    if password.isdigit() or password.isalpha():
        raise Exception('Пароль должен состоять из букв и цифр!')
    else:
        return password 


class RegisterMixin: 

    def register(self, name: str, password:str) -> None: 
        if name in [user['name'] for user in self.data]:
            raise Exception('Такой юзер уже существует!')
        
        max_id = max([user['id'] for user in self.data])
        self.data.append({'id': max_id + 1, 'name':name, 'password': validate_password(password)})
        
        json.dump(self.data, open('user.json', 'w'))
        print('Successfully registered')


class LoginMixin:

    def login(self, name, password):
        if name in [user['name'] for user in self.data]:
            user = [i for i in self.data if name == i['name']] 

            if password == user[0]['password']:
                print('Вы успешно залогинились!')
            else: 
                raise Exception('Неверный пароль!')

        else:
            print('Нет такого юзера в БД!')


class ChangePasswordMixin:

    def change_password(self, name, old_password, new_passsword):
        validate_password(new_passsword)
        user = [i for i in self.data if name == i['name']] 

        if old_password == user[0]['password']:
            ind = self.data.index(user[0])
            self.data[ind]['password'] = new_passsword
            json.dump(self.data, open('user.json', 'w'))
            print('Password changed successfully!')
        else:
            raise Exception('Старый пароль указан не верно!')


class ChangeUserNameMixin:

    def change_name(self, old_name: str, new_name: str) -> None: 
        names = [user['name'] for user in self.data]

        if old_name in names: 
            user = [user for user in self.data if old_name == user['name']]
            ind = self.data.index(user[0])

            def __corr_n(name):
                while name in names: 
                    print('Пользователь с таким именем уже существует!')
                    name = input('Введите новое имя: ')
                return name

            self.data[ind]['name'] = __corr_n(new_name)
            json.dump(self.data, open('user.json', 'w'))
            print('Username changed successfully!')
        else:       
            raise Exception('Нет такого зарегистрированного юзера в БД!')



class CheckOwnerMixin:
    
    def check(self, owner):
        if owner in [user['name'] for user in self.data]:
            pass
        else: 
            raise Exception('Нет такого пользователя!')


class User(RegisterMixin, LoginMixin, ChangePasswordMixin, ChangeUserNameMixin): 
    def __init__(self, filename):
        self.data = json.load(open(filename))

class Post(CheckOwnerMixin):
    def __init__(self, title, description, price, quantity, owner):
        self.title = title 
        self.description = description
        self.price = price
        self.quantity = quantity
        self.owner = self.check(owner)

    def post(self):
        new_post = {
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity
        }
        print('Пост успешно создан: ', new_post)


# emma = User('user.json')
# emma.register('Emma', 'opq2555gggg34')
# emma.login('Emma', 'opq2555gggg34')
# emma.change_password('Emma', 'opq2555gggg34', 'neverland01')
# emma.login('Emma', 'neverland01')
# emma.change_name('Emma', 'Emma SS')

# emma_p = Post('Breadcrumbs', 'The whole grain bread with flaxseeds', 80, 40, 'Emma SS')
# emma_p.post()


# rick = User('user.json')
# rick.register('Rick', 'galaxy234500')
# rick.login('Rick', 'galaxy234500')
# rick.change_password('Rick', 'galaxy234500', 'galaxy6744600')
# rick.login('Rick', 'galaxy6744600')
# rick.change_name('Rick', 'Rick Sanchez')

# rick_p = Post('Teleporter', 'The best quality', 2987651, 5, 'Rick Sanchez')
# rick_p.post()


# yoongi = User('user.json')
# yoongi.register('Yoongi', 'banghtansoenoedan2013')
# yoongi.login('Yoongi', 'banghtansoenoedan2013')
# yoongi.change_password('Yoongi', 'banghtansoenoedan2013', 'thewonderfulworld1')
# yoongi.login('Yoongi', 'thewonderfulworld1')
# yoongi.change_name('Yoongi', 'Min Yoongi')

# yoongi_p = Post('Album', 'Wings', 5700, 100, 'Min Yoongi')
# yoongi_p.post()