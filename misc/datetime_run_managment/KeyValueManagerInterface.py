class KeyValueManagerInterface:
    def save_or_update_key(self, key: str, value: str | int | float):
        raise NotImplementedError

    def get_value(self, key: str):
        raise NotImplementedError
