from django.test import TestCase, Client
from django.urls import reverse, path


from website.forms import (
    RegisterForm,
    LoginForm,
    SearchForm,
    UpdateMenuItemForm,
)
from website.models import (
    Order,
    OrderItem,
    MenuItem,
    Restaurant,
    ReservationSlot,
    Table
)

class RegisterTest(TestCase):
    # simulate a user entering in a valid form and being redirected to login successfully
    def test_restaurant_created(self):
        response = self.client.post(reverse('website:register'), 
            {
            'restaurantname':'restaurant', 
            'username':'username', 
            'password1': 'password',
            'password2': 'password'
            }, follow = True)
        # print('right here buttface')
        # print(response)
        self.assertRedirects(response, '/website/accounts/login/')

class LoginTest(TestCase):
    # simulate a user entering in an existing restaurant's account information
    # successfully redirect to that restaurant's homepage
    def test_login_worked(self):
        database = Restaurant.objects.create(
            restaurant_name = 'restaurant',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )
        restaurant_id = str(database.id)

        response = self.client.post(reverse('website:login'),
            {
            'restaurantname':'restaurant', 
            'username':'username', 
            'password': 'password',
            }, follow = True)

        # print('HELLO there')
        # # print(MenuItem.objects.get(menu_item_name = 'test1'))
        # print(response)

        redirect_url = "/website/restaurant/" + str(restaurant_id) + "/"

        self.assertRedirects(response, redirect_url)

class SearchbarTest(TestCase):
    def test_no_restaurants_exist(self):
        # simulate a user searching for a restaurant called 'restaurant'
        # no results found so restaurant homepage html is returned
        response = self.client.post(reverse('website:search'),
            {
            'restaurantsearch':'restaurant2', 
            }, follow = True)
        self.assertTemplateUsed(response, 'website/searchbar.html')
        
    def test_no_restaurants_from_search(self):
        # simulate a user searching for a restaurant called 'restaurant'
        # no results found so restaurant homepage html is returned
        database = Restaurant.objects.create(
            restaurant_name = 'restaurant',
            restaurant_username = 'username',
            restaurant_password = 'password',
        )    
        response = self.client.post(reverse('website:search'),
            {
            'restaurantsearch':'restaurant2', 
            }, follow = True)
        self.assertTemplateUsed(response, 'website/searchbar.html')
        # self.assertInHTML('/website/templates/website/restaurants.html', response.content.decode())


    def test_one_restaurant_found(self):
        # simulate a user searching for a restaurant called 'restaurant'
        # one result found so searchbar html is returned
        database = Restaurant.objects.create(
            restaurant_name = 'restaurant',
            restaurant_username = 'username',
            restaurant_password = 'password',
        )        
        response = self.client.post(reverse('website:search'),
            {
            'restaurantsearch':'restaurant', 
            }, follow = True)
        self.assertTemplateUsed(response, 'website/searchbar.html')


class MenuItemTest(TestCase):

    def test_add_menu_item(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        restaurant_id = str(database.id)

        response = self.client.post(reverse('website:addmenuitem', kwargs={'restaurant_id': restaurant_id}), 
            {
            'menuitemname':'test1', 
            'menuitemdescription':'testing 1', 
            'menuitemprice': 1,
            }, follow = True)

        self.assertEqual(MenuItem.objects.count(), 1)

        redirect_url = "/website/restaurant/" + str(restaurant_id) + "/"
        self.assertRedirects(response, redirect_url)

    def test_delete_menu_item(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        restaurant_id = str(database.id)

        og_menu_item = MenuItem.objects.create(
            restaurant_id = database.id,
            menu_item_name = "original",
            menu_item_description = "original description",
            menu_item_price = 1
        )

        response = self.client.post(reverse('website:deletemenuitem', kwargs={'menu_item_id': og_menu_item.id}), follow = True)
        self.assertEqual(MenuItem.objects.count(), 0)

        redirect_url = "/website/restaurant/" + restaurant_id + "/"
        self.assertRedirects(response, redirect_url)

    def test_update_menu_item(self):

        database = Restaurant.objects.create(
            restaurant_name = 'SARA2',
            restaurant_username = 'username',
            restaurant_password = 'password'
        )

        og_menu_item = MenuItem.objects.create(
            restaurant_id = database.id,
            menu_item_name = "original",
            menu_item_description = "original description",
            menu_item_price = 1
        )

         # Testing no inputs
        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': og_menu_item.id}), 
            {
            }, follow = True)

        updated_name = MenuItem.objects.get(id = og_menu_item.id)
        self.assertEqual(updated_name.menu_item_name, 'original')
        self.assertEqual(updated_name.menu_item_description, 'original description')
        self.assertEqual(updated_name.menu_item_price, 1)
        redirect_url = "/website/restaurant/edit_menu/" + str(database.id) + "/"
        self.assertRedirects(response, redirect_url)

        menu_id = og_menu_item.id

        # Testing only updating name input
        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': og_menu_item.id}), 
            {
            'menuitemname':'updated', 
            }, follow = True)

        updated_name = MenuItem.objects.get(id = og_menu_item.id)
        self.assertEqual(updated_name.menu_item_name, 'updated')
        self.assertEqual(updated_name.menu_item_description, 'original description')
        self.assertEqual(updated_name.menu_item_price, 1)
        redirect_url = "/website/restaurant/edit_menu/" + str(database.id) + "/"
        self.assertRedirects(response, redirect_url)

        # Testing only updating description input
        og_menu_item.menu_item_name = 'original'
        og_menu_item.save(update_fields=["menu_item_name"]) 

        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': og_menu_item.id}), 
            {
            'menuitemdescription':'updated description', 
            }, follow = True)

        updated_name = MenuItem.objects.get(id = og_menu_item.id)
        self.assertEqual(updated_name.menu_item_name, 'original')
        self.assertEqual(updated_name.menu_item_description, 'updated description')
        self.assertEqual(updated_name.menu_item_price, 1)
        redirect_url = "/website/restaurant/edit_menu/" + str(database.id) + "/"
        self.assertRedirects(response, redirect_url)

        # Testing only updating price input
        og_menu_item.menu_item_description = 'original description'
        og_menu_item.save(update_fields=["menu_item_description"]) 

        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': og_menu_item.id}), 
            {
            'menuitemprice':2, 
            }, follow = True)

        updated_name = MenuItem.objects.get(id = og_menu_item.id)
        self.assertEqual(updated_name.menu_item_name, 'original')
        self.assertEqual(updated_name.menu_item_description, 'original description')
        self.assertEqual(updated_name.menu_item_price, 2)
        redirect_url = "/website/restaurant/edit_menu/" + str(database.id) + "/"
        self.assertRedirects(response, redirect_url)

        # Testing all 3 inputs
        og_menu_item.menu_item_price = 1
        og_menu_item.save(update_fields=["menu_item_price"]) 

        response = self.client.post(reverse('website:editmenuitem', kwargs={'menu_item_id': og_menu_item.id}), 
            {
            'menuitemname':'updated', 
            'menuitemdescription':'updated description', 
            'menuitemprice':2, 
            }, follow = True)

        updated_name = MenuItem.objects.get(id = og_menu_item.id)
        self.assertEqual(updated_name.menu_item_name, 'updated')
        self.assertEqual(updated_name.menu_item_description, 'updated description')
        self.assertEqual(updated_name.menu_item_price, 2)
        redirect_url = "/website/restaurant/edit_menu/" + str(database.id) + "/"
        self.assertRedirects(response, redirect_url)





    
