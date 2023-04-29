import pickle


class Serializer:
    @staticmethod
    def serialize(obj: object):
        pickled = pickle.dumps(obj, 0).decode()
        return pickled

    @staticmethod
    def deserialize(pickled: str):
        unpickled = pickle.loads(pickled.encode())
        return unpickled
