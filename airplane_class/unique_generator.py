import random
import string


class UniqueIDGenerator:
    unique_ids = set()

    @classmethod
    def generate_unique_id(cls):
        uniqueId = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while uniqueId in cls.unique_ids:
            uniqueId = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        cls.unique_ids.add(uniqueId)
        return uniqueId
