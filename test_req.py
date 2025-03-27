import pytest
import generator

#test case 4: user generates a password WITH specified requirements
passw = generator.PasswordGenerator()

#in this test, setting custom attributes 
#length = 10
#exclude numbers 5 and 7
#exclude characters ABCDEFG and abcdefg
#exclude characters !?$& 

def func():
    #custom properties of password from changing class attributes
    passw.maxlen = 5
    passw.minlen = 5
    passw.excludeuchars = "ABCDEF"
    passw.excludelchars = "abcdefg"
    passw.excludenumbers = "12345"
    passw.excludeschars = "!?#$."
    password = passw.generate()

    contains_lower = False
    contains_upper = False
    contains_num = False
    contains_special = False
    
    for x in password:
        if x in passw.excludeuchars:
            contains_lower = True
        if x in passw.excludelchars:
            contains_upper = True
        if x in passw.excludenumbers:
            contains_num = True
        if x in passw.excludeschars:
            contains_special = True
            
    if contains_lower == False and contains_upper == False and contains_num == False and contains_special == False and len(password) == passw.maxlen:
        return True
    

def test_func():
    assert func() == True