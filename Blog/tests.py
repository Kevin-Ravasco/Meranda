from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, category, trending, contact, blog_single
from .models import Post


def setUp(self):
    Post.objects.create(title='corona virus', description='Django board.')


class HomePageTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class CategoryPageTests(TestCase):
    def test_category_view_status_code(self):
        url = reverse('category')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

'''    def test_category_url_resolves_category_view(self):
        view = resolve()'''


'''class PopularPageTests(TestCase):
    def test_popular_view_status_code(self):
        url = reverse('popular')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)'''


class TrendingPageTests(TestCase):
    def test_trending_view_status_code(self):
        url = reverse('trending')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class ContactageTests(TestCase):
    def test_contact_view_status_code(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)