from abc import abstractmethod, ABC


class BaseCoefficient(ABC):

    @abstractmethod
    def get_attributes_dict(self) -> dict:
        pass


class Total(BaseCoefficient):
    def __init__(self, total: int | float, larger: int | float, lesser: int | float):
        self.total = total
        self.larger = larger
        self.lesser = lesser

    @property
    def total(self) -> int:
        return self._total

    @total.setter
    def total(self, total: int | float):
        self._total = total

    @property
    def larger(self) -> int | float:
        return self._larger

    @larger.setter
    def larger(self, coefficient: int | float):
        self._larger = coefficient

    @property
    def lesser(self) -> int | float:
        return self._lesser

    @lesser.setter
    def lesser(self, coefficient: int | float):
        self._lesser = coefficient

    def get_attributes_dict(self) -> dict:
        return {'total': self.total, 'larger': self.larger, 'lesser': self.lesser}


class Coefficient(BaseCoefficient):

    def __init__(self, coefficient: int | float):
        self.coefficient = coefficient

    @property
    def coefficient(self):
        return self._coefficient

    @coefficient.setter
    def coefficient(self, coefficient: int | float):
        self._coefficient = coefficient

    def get_attributes_dict(self) -> dict:
        return {'coefficient': self.coefficient}
