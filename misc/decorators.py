def singleton(cls: type):
    def wrapper(*args: tuple[any, ...], **kwargs: dict[str, any]):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]
    __instances = {}
    return wrapper
