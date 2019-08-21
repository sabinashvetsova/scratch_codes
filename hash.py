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

    def sha1hash(self, input):
        bytes_string = str.encode(input)
        return hashlib.sha1(bytes_string).hexdigest()

    def sha256hash(self, input):
        bytes_string = str.encode(input)
        return hashlib.sha256(bytes_string).hexdigest()

    def sha384hash(self, input):
        bytes_string = str.encode(input)
        return hashlib.sha384(bytes_string).hexdigest()

    def sha512hash(self, input):
        bytes_string = str.encode(input)
        return hashlib.sha512(bytes_string).hexdigest()

    def md5hash(self, input):
        bytes_string = str.encode(input)
        return hashlib.md5(bytes_string).hexdigest()

    def blake2bhash(self, input):
        bytes_string = str.encode(input)
        return hashlib.blake2b(bytes_string).hexdigest()

    def calc_hash(self, input):
        return self.hash_func(input)
