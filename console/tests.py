"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase


#class SimpleTest(TestCase):
    #def test_basic_addition(self):
    #    """
    #    Tests that 1 + 1 always equals 2.
    #    """
    #    self.assertEqual(1 + 1, 2)

from Crypto.Cipher import AES

key = 'F74E66709E1C4647323DBEA92412411E'
obj = AES.new(key, AES.MODE_ECB)
#msg = obj.encrypt('F74E66709E1C4647323DBEA92412411EF74E66709E1C4647323DBEA92412411E')
msg = obj.encrypt('192.168.30.59')
print msg.encode('hex') 
msg1 = obj.decrypt(msg)
print msg1