import string
from copy import deepcopy
from random import shuffle, randint

try:
    from secrets import choice
except ImportError:
    from random import choice


class PasswordGenerator:
    """reqs:
        min length 6 chars
        max len 16 chars
        must contain at least 1 upper case, lower case, number, special char
    """

    def __init__(self):
        self.minlen = 6
        self.maxlen = 16
        self.minuchars = 1
        self.minlchars = 1
        self.minnumbers = 1
        self.minschars = 1
        self.excludeuchars = ""
        self.excludelchars = ""
        self.excludenumbers = ""
        self.excludeschars = ""

        self.lower_chars = string.ascii_lowercase
        self.upper_chars = string.ascii_uppercase
        self.numbers_list = string.digits
        self._schars = [
            "!",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            ",",
            ".",
            "-",
            "_",
            "+",
            "=",
            "<",
            ">",
            "?",
        ]
        self._allchars = (
            list(self.lower_chars)
            + list(self.upper_chars)
            + list(self.numbers_list)
            + self._schars
        )

    def generate(self):
        #Generates a password using default or custom properties
        if (
            self.minlen < 0
            or self.maxlen < 0
            or self.minuchars < 0
            or self.minlchars < 0
            or self.minnumbers < 0
            or self.minschars < 0
        ):
            raise ValueError("Character length should not be negative")

        if self.minlen > self.maxlen:
            raise ValueError(
                "Minimum length cannot be greater than maximum length. The default maximum length is 16."
            )

        collectiveMinLength = (
            self.minuchars + self.minlchars + self.minnumbers + self.minschars
        )

        if collectiveMinLength > self.minlen:
            self.minlen = collectiveMinLength

        final_pass = [
            choice(list(set(self.lower_chars) - set(self.excludelchars)))
            for i in range(self.minlchars)
        ]
        final_pass += [
            choice(list(set(self.upper_chars) - set(self.excludeuchars)))
            for i in range(self.minuchars)
        ]
        final_pass += [
            choice(list(set(self.numbers_list) - set(self.excludenumbers)))
            for i in range(self.minnumbers)
        ]
        final_pass += [
            choice(list(set(self._schars) - set(self.excludeschars)))
            for i in range(self.minschars)
        ]

        currentpasslen = len(final_pass)
        all_chars = list(
            set(self._allchars)
            - set(
                list(self.excludelchars)
                + list(self.excludeuchars)
                + list(self.excludenumbers)
                + list(self.excludeschars)
            )
        )

        if len(final_pass) < self.maxlen:
            randlen = randint(self.minlen, self.maxlen)
            final_pass += [choice(all_chars) for i in range(randlen - currentpasslen)]

        shuffle(final_pass)
        return "".join(final_pass)

    def shuffle_password(self, password, maxlen):
        #shuffle the given chars to return a password
        final_pass = [choice(list(password)) for i in range(int(maxlen))]
        shuffle(final_pass)
        return "".join(final_pass)

    def non_duplicate_password(self, maxlen):
        #generate a non-duplicate key of given length
        allchars = deepcopy(self._allchars)
        final_pass = []
        try:
            for i in range(maxlen):
                character = choice(allchars)
                element_index = allchars.index(character)
                final_pass.append(character)
                allchars.pop(element_index)
        except IndexError as e:
            raise ValueError("Length should be less than 77 characters.")

        shuffle(final_pass)
        return "".join(final_pass)
    
password = PasswordGenerator2()
#custom properties of password from changing class attributes
password.maxlen = 5
password.minlen = 5
password.excludelchars = "A"
password.generate()
