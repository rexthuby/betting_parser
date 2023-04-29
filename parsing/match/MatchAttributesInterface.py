from abc import ABC, abstractmethod


class MatchAttributesInterface(ABC):

    @abstractmethod
    def get_attributes(self) -> dict | list:
        pass