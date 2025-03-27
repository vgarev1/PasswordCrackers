import unittest, database, random, string, create_read

from database import store_password
from pass_generator import PasswordGenerator

from flask.testing import FlaskClient

class TestScenario6(unittest.TestCase):
    def test_unique_password(self):
        for i in range(0, 20):
            user_pass_object = PasswordGenerator(minlen=2, maxlen=2,
                                                 minlchars=0, minuchars=0,
                                                 minnumbers=0, minschars=0)
            user_pass = user_pass_object.generate()

            user_id = database.create_user("test" + str(i),
                                           "test" + str(i) + "pass")

            database.store_password(user_id, user_pass, "Test")

        try:
            for attempt in range(1, 10):
                user_pass_object = PasswordGenerator(minlen=1, maxlen=1,
                                                     minlchars=0, minuchars=0,
                                                     minnumbers=0, minschars=0)
                user_pass = user_pass_object.generate()

                for password_entry in database.get_password_history():
                    self.assertNotEqual(user_pass, password_entry["password"])

        except AssertionError:
            for del_password_entry in database.get_password_history():
                database.delete_user(del_password_entry["user_id"])

            database.delete_test_passwords()

            self.assertNotEqual(user_pass, password_entry["password"])

        else:
            for del_password_entry in database.get_password_history():
                database.delete_user(del_password_entry["user_id"])

            database.delete_test_passwords()

    def test_meets_requirements(self):
        test_minlen = random.randint(1, 10)
        test_maxlen = random.randint(test_minlen, 10)

        test_minuchars = random.randint(test_minlen, test_maxlen)

        test_minlchars = random.randint(test_minlen - test_minuchars,
            test_maxlen - test_minuchars)
        if (test_minlchars < 0):
            test_minlchars = 0

        test_minnumbers = random.randint(
            test_minlen - test_minuchars - test_minlchars,
            test_maxlen - test_minuchars - test_minlchars)
        if (test_minnumbers < 0):
            test_minnumbers = 0

        test_minschars = random.randint(
            test_minlen - test_minuchars - test_minlchars - test_minnumbers,
            test_maxlen - test_minuchars - test_minlchars - test_minnumbers)
        if (test_minschars < 0):
            test_minschars = 0

        test_excludeuchars = str()
        test_excludelchars = str()
        test_excludenumbers = str()
        test_excludeschars = str()

        for char in string.ascii_uppercase:
            if (random.random() < 0.5):
                test_excludeuchars += char

        for char in string.ascii_lowercase:
            if (random.random() < 0.5):
                test_excludelchars += char

        for char in string.digits:
            if (random.random() < 0.5):
                test_excludenumbers += char

        special_chars = ["!", "#", "$", "%", "^", "&", "*", "(", ")", ",", ".",
            "-", "_", "+", "=", "<", ">", "?"]

        for char in special_chars:
            if (random.random() < 0.5):
                test_excludeuchars += char

        password_object = PasswordGenerator(minlen=test_minlen,
            maxlen=test_maxlen, minuchars=test_minuchars,
            minlchars=test_minlchars, minnumbers=test_minnumbers,
            minschars=test_minschars, excludeuchars=test_excludeuchars,
            excludelchars=test_excludelchars,
            excludenumbers=test_excludenumbers,
            excludeschars=test_excludeschars)

        password = password_object.generate()

        self.assertLessEqual(test_minlen, len(password))

        self.assertLessEqual(len(password), test_maxlen)

        lcount = 0
        ucount = 0
        numcount = 0
        scount = 0

        for char in password:
            self.assertNotIn(char, test_excludelchars)
            self.assertNotIn(char, test_excludeuchars)
            self.assertNotIn(char, test_excludenumbers)
            self.assertNotIn(char, test_excludeschars)

            if char in string.ascii_lowercase:
                lcount += 1

            elif char in string.ascii_uppercase:
                ucount += 1

            elif char in string.digits:
                numcount += 1

            elif char in special_chars:
                scount += 1

        self.assertLessEqual(test_minlchars, lcount)
        self.assertLessEqual(test_minuchars, ucount)
        self.assertLessEqual(test_minnumbers, numcount)
        self.assertLessEqual(test_minschars, scount)

    def test_save(self):
        user_id = database.create_user("test", "test_pass")

        pass_object = PasswordGenerator()

        password = pass_object.generate()

        store_password(user_id, password, "Test")

        password_list = list()

        for password_entry in database.get_password_history():
            password_list.append(password_entry["password"])

        try:
            self.assertIn(password, password_list)

        except AssertionError:
            for del_password_entry in database.get_password_history():
                database.delete_user(del_password_entry["user_id"])

            database.delete_test_passwords()

            self.assertIn(password, password_list)

        else:
            for del_password_entry in database.get_password_history():
                database.delete_user(del_password_entry["user_id"])

            database.delete_test_passwords()


    def test_quit(self):
        test_client = FlaskClient(create_read.app)
        response = test_client.post("/display-page",
            data={"username": "test_username", "password": "test_pass"})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()