import random

class Dice:

    def __init__(self):
        self.__value =  random.randint(1,6)

    def _throw_dice(self):
        self._set_value(random.randint(1,6))
        return self._get_value()
    
    def _set_value(self,value):
        self.__value = value
    
    def _get_value(self):
        return self.__value
