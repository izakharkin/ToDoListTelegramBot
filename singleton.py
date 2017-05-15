class Singleton(type):
    """
    Singleton pattern
    
    """
    _instances = {}

    def __call__(_class, *args, **kwargs):
        if _class not in _class._instances:
            _class._instances[_class] = super(Singleton, _class).__call__(*args, **kwargs)
        return _class._instances[_class]
