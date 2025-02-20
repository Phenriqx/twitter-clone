from django.test import TestCase, override_settings
from django.urls import reverse

class MaintenanceModeTest(TestCase):
    
    @override_settings(MAINTENANCE_MODE=False)
    def test_maintenance_mode_is_off(self):
        """TEST IF MAINTENANCE MODE IS OFF AND APPLICATION CAN BE ACCESSED"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode_is_on(self):
        """TEST IF MAINTENANCE MODE IS ON AND APPLICATION CAN BE ACCESSED ONLY BY ADMIN"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 503)