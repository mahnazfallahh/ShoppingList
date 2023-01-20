class NameISNotStringException(TypeError):
    def __str__(self):
        return "first name can't be a number ."