from time import sleep

from django.test import TestCase
from django.shortcuts import reverse

from rango.models import Category,Page
from django.utils import timezone
# Create your tests here.
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test', views=1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0 ), True)

    def test_slug_line_creation(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present')
        self.assertQuerysetEqual(response.context['categories'], [])



    def test_index_view_with_categories(self):
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1 ,1)
        add_cat('tmp test temp',1 ,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')

        self.assertEqual(len(response.context['categories']), 4)


class PageViewTests(TestCase):

    def test_time_not_in_the_future(self):
        c = Category(name='demo')
        c.save()
        p = Page(title='page', url='https://www.baidu.com')
        p.category = c
        p.save()

        response = self.client.get(reverse('rango:goto')+'?page_id='+str(p.id))
        self.assertEqual(response.status_code, 302)
        page = Page.objects.get(id=p.id)
        self.assertTrue(page.last_visit <= timezone.now())
        self.assertTrue(page.first_visit <= timezone.now())
        sleep(2)
        self.client.get(reverse('rango:goto') + '?page_id=' + str(p.id))
        self.assertTrue(page.first_visit <= page.last_visit)


