from .classA import A

class B(A):
    def mymethod(self):
        return super().mymethod()

