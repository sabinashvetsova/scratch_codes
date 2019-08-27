import hashlib


class HashCode:
    """Модель хэш-кода"""

    def __init__(self, hash_name):
        if hash_name == 'sha1':
            self.hash_func = self.sha1hash
        elif hash_name == 'sha256':
            self.hash_func = self.sha256hash
        elif hash_name == 'sha384':
            self.hash_func = self.sha384hash
        elif hash_name == 'sha512':
            self.hash_func = self.sha512hash
        elif hash_name == 'blake2b':
            self.hash_func = self.blake2bhash
        elif hash_name == 'md5':
            self.hash_func = self.md5hash

    @staticmethod
    def sha1hash(input):
        bytes_string = str.encode(input)
        return hashlib.sha1(bytes_string).hexdigest()

    @staticmethod
    def sha256hash(input):
        bytes_string = str.encode(input)
        return hashlib.sha256(bytes_string).hexdigest()

    @staticmethod
    def sha384hash(input):
        bytes_string = str.encode(input)
        return hashlib.sha384(bytes_string).hexdigest()

    @staticmethod
    def sha512hash(input):
        bytes_string = str.encode(input)
        return hashlib.sha512(bytes_string).hexdigest()

    @staticmethod
    def md5hash(input):
        bytes_string = str.encode(input)
        return hashlib.md5(bytes_string).hexdigest()

    @staticmethod
    def blake2bhash(input):
        bytes_string = str.encode(input)
        return hashlib.blake2b(bytes_string).hexdigest()

    def calc_hash(self, input):
        return self.hash_func(input)
