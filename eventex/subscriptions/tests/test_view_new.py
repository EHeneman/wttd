from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(resolve_url('subscriptions:new'))

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        return self.assertEquals(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        return self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = ( ('<form', 1),
                 ('<input', 6),
                 ('type="text"', 3),
                 ('type="email"', 1),
                 ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription_form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

class SubscriptionNewPostValid(TestCase):
    def setUp(self):
        data = dict(name="Henrique Bastos", cpf="12345678901",
                    email="henrique@bastos.net", phone="21-99618-6180")
        self.response = self.client.post(resolve_url('subscriptions:new'), data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertRedirects(self.response, resolve_url('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_saved_subscription(self):
        self.assertTrue(Subscription.objects.exists())

class SubscriptionNewPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(resolve_url('subscriptions:new'), {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
