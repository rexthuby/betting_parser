from enum import Enum

from parsing.match.MatchAttributesInterface import MatchAttributesInterface
from parsing.match.bets.coefficient import BaseCoefficient



class BetNameEnum(Enum):
    one_x_two = '1x2'
    both_goal = 'Обе забьют'
    double_chance = 'Двойной шанс'
    total = 'Тотал'
    team_wins = 'Победа в матче'


class Bet:
    def __init__(self, name: BetNameEnum, coefficients: list[BaseCoefficient]):
        self.name = name
        self.coefficients = coefficients

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: BetNameEnum):
        self._name = name

    @property
    def coefficients(self):
        return self._coefficients

    @coefficients.setter
    def coefficients(self, coefficients: list[BaseCoefficient]):
        self._validate_coefficients(coefficients)
        self._coefficients = coefficients

    def _validate_coefficients(self, coefficients: list[BaseCoefficient]):
        """
        :exception ValueError:
        """

        if len(coefficients) < 1:
            raise ValueError

        first_class = type(coefficients[0])
        for elem in coefficients:
            if not issubclass(type(elem), BaseCoefficient):
                raise ValueError('All elements of coefficients must belong to the DictableInterface class')
            if type(elem) != first_class:
                raise ValueError('All elements of coefficients must belong to the same class')

    def get_attributes_dict(self) -> dict:
        coefficients = []
        for coefficient in self.coefficients:
            coefficients.append(coefficient.get_attributes_dict())
        return {'name': self.name.value, 'coefficients': coefficients}


class MatchBets(MatchAttributesInterface):
    def __init__(self, bets: list[Bet]):
        self.bets = bets

    @property
    def bets(self) -> list[Bet]:
        return self._bets

    @bets.setter
    def bets(self, bets: list[Bet]):
        self._bets = bets

    def get_attributes(self) -> list:
        bets = []
        for bet in self.bets:
            bets.append(bet.get_attributes_dict())
        return bets
