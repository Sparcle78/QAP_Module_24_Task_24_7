from api import PetFriends
from settings import *

class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()
        print(2)

    def test_addNewPetWithoutPhoto(self, name='Shnau1', animal_type='шнауцер1', age = 14):
        '''Проверяем добавление питомца с параметрами имя, порода, возраст'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)

        status, result = self.pf.create_new_pet_simple(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    def test_addNewPetPhoto(self, pet_photo='images/cat_petFriends.jpg'):
        '''Проверяем добавление фотографии питомца первому питомцу из полученного списка питомцев'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:

            status, result = self.pf.add_pets_photo(auth_key, myPets['pets'][0]['id'], pet_photo)
            assert status == 200
            assert result['id'] == myPets['pets'][0]['id']
        else:
            raise Exception("There is no my pets")


    def test_addPetAgeNegativ(self, name='Shnau1', animal_type='шнауцер1', age = -1):
        '''Проверяем добавление питомца с отрицательным значением возраста'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)

        status, _ = self.pf.create_new_pet_simple(auth_key, name, animal_type, age)
        assert status != 200
        # ожидается ошибка, так как возраст меньше нуля, однако, фактически, питомец создается с отрицательным возрастом

    def test_addNewPetWithErrorAge (self, name='test', animal_type='test', age='test', pet_photo='images/dog_petsFriend.jpg'):
        '''Проверяем добавление питомца с текстовым значением возраста'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, _ = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status != 200
        # ожидается ошибка, так как возраст текстовое значение, однако, фактически, питомец создается с любым текстовым значением параметра age

    def test_addNewPetWithErrorPhoto (self, name='test', animal_type='test', age='2', pet_photo='photo'):
        '''Проверяем добавление питомца с неверным параметром pet_photo'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        try:
            status, _ = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        except FileNotFoundError:
            assert True

    def test_addNewPetPhotoWithErrorPhoto (self, name='test', animal_type='test', age='2', pet_photo='images/dog_petFriend.jpg'):
        '''Проверяем добавление фотографии питомца с неверным параметром pet_photo'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        try:
            status, _ = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        except FileNotFoundError:
            assert True

    def test_getApiKeyWithBadEmailCorrectPassword(self, email=invalid_email, password=valid_password):
        '''Проверяем запрос с верным паролем и неверным емейлом. Проверяем нет ли ключа в ответе'''

        status, result = self.pf.get_API_key(email, password)
        assert status == 403
        assert 'key' not in result

    def test_getApiKeyWithCorrectEmailBadPassword(self, email=valid_email, password=invalid_password):
        '''Проверяем запрос с неверным паролем и с верным емейлом. Проверяем нет ли ключа в ответе'''

        status, result = self.pf.get_API_key(email, password)
        assert status == 403
        assert 'key' not in result

    def test_addNewPetWithoutPhotoWithEmptyData(self, name='', animal_type='', age=''):
        '''Проверяем добавление питомца с пустыми значениями параметров имя, порода, возраст'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)

        status, result = self.pf.create_new_pet_simple(auth_key, name, animal_type, age)
        assert status == 400
        # ожидается ошибка, однако, фактически, питомец создается с пустыми значениями всех параметров

    def test_addNewPetWithoutPhotoWithFiveDigitAge(self, name='Fifa', animal_type='cat', age=12352):
        '''Добавление питомца с числом более трех знаков в переменной age. Ожидается ошибка, если значение переменной задано более чем трехзначным числом'''

        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, result = self.pf.create_new_pet_simple(auth_key, name, animal_type, age)
        number = result['age']

        assert len(number) <= 3, 'Питомец добавлен на сайт с числом превышающим 3 знака в поле возраст'

