from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command
from django.conf import settings


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')
        self.user = ShopUser.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains')
        self.user_with__first_name = ShopUser.objects.create_user('umaturman', 'umaturman@geekshop.local',
                                                                  'geekbrains', first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Магазин')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)
        # с логином все должно быть хорошо
        self.client.login(username='tarantino', password='geekbrains')
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина,', response.content.decode())
        self.assertIn('Пользователь', response.content.decode())

    def test_user_logout(self):
        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')
        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)
        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    # регистрация пользователя с отправкой подтверждения по почте
    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '7'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
