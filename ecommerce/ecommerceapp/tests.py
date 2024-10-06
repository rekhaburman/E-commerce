from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from unittest.mock import patch  # For mocking the PayPal API

from .models import Order, OrderUpdate

class CheckoutViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_redirect_if_not_logged_in(self):
        # If not logged in, user should be redirected to the login page
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, '/auth/login')

    def test_access_checkout_when_logged_in(self):
        # Test authenticated access to the checkout page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')

    def test_post_order_creation(self):
        # Test if an order is created successfully upon form submission
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('checkout'), {
            'item_json': '{"item": "example"}',
            'name': 'Test User',
            'amount': '500',
            'email': 'testuser@example.com',
            'address1': '123 Test St',
            'address2': 'Apt 1',
            'city': 'Test City',
            'state': 'Test State',
            'zipcode': '12345',
            'phone': '1234567890'
        })

        # Ensure the order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.name, 'Test User')
        self.assertEqual(OrderUpdate.objects.count(), 1)
        order_update = OrderUpdate.objects.first()
        self.assertEqual(order_update.update_desc, "Your Order Has Been Placed")

    @patch('paypalrestsdk.Payment.create')
    def test_paypal_redirection(self, mock_paypal_create):
        # Mock the PayPal create method to simulate successful payment initiation
        self.client.login(username='testuser', password='testpassword')

        # Simulate the approval URL response from PayPal
        mock_paypal_create.return_value = True
        mock_payment = mock_paypal_create.return_value
        mock_payment.links = [
            type('obj', (object,), {"rel": "approval_url", "href": "http://paypal.com/approval"})
        ]

        response = self.client.post(reverse('checkout'), {
            'item_json': '{"item": "example"}',
            'name': 'Test User',
            'amount': '500',
            'email': 'testuser@example.com',
            'address1': '123 Test St',
            'address2': 'Apt 1',
            'city': 'Test City',
            'state': 'Test State',
            'zipcode': '12345',
            'phone': '1234567890'
        })

        # Ensure the user is redirected to PayPal for approval
        self.assertRedirects(response, 'http://paypal.com/approval')

    @patch('paypalrestsdk.Payment.create')
    def test_paypal_error_handling(self, mock_paypal_create):
        # Simulate PayPal payment creation failure
        self.client.login(username='testuser', password='testpassword')

        # Mock the create method to return False, simulating an error
        mock_paypal_create.return_value = False
        mock_paypal_create.error = "Some error occurred"

        response = self.client.post(reverse('checkout'), {
            'item_json': '{"item": "example"}',
            'name': 'Test User',
            'amount': '500',
            'email': 'testuser@example.com',
            'address1': '123 Test St',
            'address2': 'Apt 1',
            'city': 'Test City',
            'state': 'Test State',
            'zipcode': '12345',
            'phone': '1234567890'
        })

        # Ensure error message is added to the messages framework
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Some error occurred" in message.message for message in messages))
        self.assertEqual(response.status_code, 200)  # Renders checkout.html again due to error
        self.assertTemplateUsed(response, 'checkout.html')
