import pytest
import generator

#test case 3: user generates a password with no specified requirements
passw = generator.PasswordGenerator()

#test to make sure password meets requirements
# len btwn 6-16, contains 1 of the following: uppercase, lowercase, number, special 
def func():
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"
    schars = "!#$%^&*(),.-_=+<>?"
    password = passw.generate()

    contains_lower = False
    contains_upper = False
    contains_num = False
    contains_special = False
    
    for x in password:
        if x in lower:
            contains_lower = True
        if x in upper:
            contains_upper = True
        if x in nums:
            contains_num = True
        if x in schars:
            contains_special = True
            
    if contains_lower == True and contains_upper == True and contains_num == True and contains_special == True and (6 <= len(password) <= 16):
        return True

def test_func():
    assert func() == True


