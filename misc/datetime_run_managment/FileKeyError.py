class FileKeyError(OSError):
    def __init__(self, message: str = None, key: str = None, file_name: str = None):
        if message is None:
            key_str = 'Key'
            file_str = ' not found in the file'
            if key is not None:
                key_str = f"{key}:{key}"
            if file_name is not None:
                file_str = f'{file_str}:{file_name}'
            message = key_str + file_str
        super().__init__(message)
