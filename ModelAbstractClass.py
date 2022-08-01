import json
from abc import ABC, abstractmethod


class MyModel(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)