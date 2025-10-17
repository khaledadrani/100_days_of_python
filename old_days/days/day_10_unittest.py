# # calc.py

# def add(x,y):
#     return x + y

# def multiply(a,b):
#     return a * b

# def divide(a,b):
#     if b == 0:
#         raise ZeroDivisionError
#     return a / b


# class Person():
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age

#     def get_response(self):
#         import requests

#         res = requests.get(f"www.company.com/{self.name}")

#         if res.ok:
#             return res.text
#         else:
#             return "Bad Response!"



# ############################## test_calc.py
# import unittest
# import calc


# class TestCalc(unittest.TestCase):

#     def test_add(self): #must start with test_
#         result = calc.add(10,5)
#         self.assertEqual(result,15)
#         result = calc.add(-5,5)
#         self.assertEqual(result,0)
#         result = calc.add(-5,-5)
#         self.assertEqual(result,-10)

#     def test_multiply(self):
#         self.assertEqual(10,calc.multiply(2,5))
#         self.assertEqual(0,calc.multiply(2,0))
#         self.assertEqual(-10,calc.multiply(-2,5))
#         self.assertEqual(10,calc.multiply(-2,-5))

#     def test_divide(self):
#         self.assertEqual(2,calc.divide(6,3))
#         self.assertEqual(0,calc.divide(0,3))
#         self.assertEqual(-2,calc.divide(-6,3))
#         self.assertEqual(2,calc.divide(-6,-3))
#         self.assertEqual(2.5,calc.divide(5,2)) #add test cases for newer bugs
#         #self.assertRaises(ZeroDivisionError,calc.divide,10,0) #first method to test exceptions
#         with self.assertRaises(ZeroDivisionError):
#             calc.divide(10,0)

# #####################################

# from calc import Person
# import unittest
# from unittest.mock import patch

# class TestPerson(unittest.TestCase):

#     def setUp(self):
#         self.p1 = Person("Khaled",10)
#         self.p2 = Person("Riadh",9)

#     def tearDown(self):
#         pass

#     @classmethod
#     def setUpClass(self):
#         pass
#     @classmethod
#     def tearDownClass(self):
#         pass
#     def test_name(self):
#         self.assertEqual("Khaled",self.p1.name)

#     # def test_get_request(self): #mocking
#     #     with patch('calc.Person.requests.get') as mock_get:
#     #         mock_get.return_value.ok = True
#     #         mock_get.return_value = "success"

#     #         res = self.p1.get_response()
#     #         mock_get.assert_called_with('www.company.com/Khaled')
# #python -m unittest test_calc.py

# if __name__ == "__main__":
#     unittest.main()