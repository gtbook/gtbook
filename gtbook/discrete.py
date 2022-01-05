# AUTOGENERATED! DO NOT EDIT! File to edit: discrete.ipynb (unless otherwise specified).

__all__ = ['Variables', 'DiscreteKey']

# Cell
import gtsam

from typing import List, Tuple, Callable, Dict


# Cell

DiscreteKey = Tuple[int, int]


class Variables:
    """A problem domain for discrete variables."""

    BINARY = ["false", "true"]

    def __init__(self):
        self._variables = {}

    def discrete(self, name: str, domain: List[str]) -> DiscreteKey:
        """Create a variable with given name and discrete domain of named values.

        Args:
            name (str): name of the variable.
            domain (List[str]): names for the different values.

        Returns:
            key: DiscreteKey, i.e., (gtsam.Key, cardinality)
        """
        discreteKey = len(self._variables), len(domain)
        self._variables[discreteKey[0]] = name, domain
        return discreteKey

    def binary(self, name: str) -> DiscreteKey:
        """Create a binary variable with given name.

        Args:
            name (str): name of the variable.

        Returns:
            key: DiscreteKey, i.e., (gtsam.Key, cardinality)
        """
        return self.discrete(name, self.BINARY)

    def name(self, discreteKey: DiscreteKey) -> str:
        """Return name of variable with given discreteKey.

        Args:
            discreteKey (DiscreteKey): (gtsam.Key, cardinality)

        Returns:
            str: name of the variable.
        """
        return self._variables[discreteKey[0]][0]

    def domain(self, discreteKey: DiscreteKey):
        """Return domain of variable with given discreteKey.

        Args:
            discreteKey (DiscreteKey): (gtsam.Key, cardinality)

        Returns:
            str: domain of the variable.
        """
        return self._variables[discreteKey[0]][1]

    def keyFormatter(self) -> Callable:
        """Return a lambda that can be used as KeyFormatter in GTSAM"""
        return lambda key: self._variables[key][0]

    def names(self) -> Dict[int, List[str]]:
        """Return a names dictionary that is used by GTSAM markdown methods"""
        return {key: domain for (key, (name, domain)) in self._variables.items()}

    def assignment(self, map: Dict[DiscreteKey, str]) -> gtsam.DiscreteValues:
        """Create a GTSAM assignment of keys to values.

        Args:
            map (Dict[DiscreteKey, str]): map from discrete keys to values.

        Returns:
            gtsam.DiscreteValues: the GTSAM equivalent.
        """
        values = gtsam.DiscreteValues()
        for discreteKey, value in map.items():
            domain = self.domain(discreteKey)
            assert value in domain, f"Specified value not found in domain of {discreteKey}"
            values[discreteKey[0]] = domain.index(value)
        return values

    def values_markdown(self, assignment: gtsam.DiscreteValues) -> str:
        """Render a DiscreteValues instance as markdown.

        Args:
            assignment (gtsam.DiscreteValues): the values to render.

        Returns:
            str: a markdown string.
        """
        converted = {self._variables[key][0]: self._variables[key][1][value] for (
            key, value) in assignment.items()}
        ss = "|Variable|value|\n|:-:|:-:|\n"
        for key, value in assignment.items():
            name, domain = self._variables[key]
            ss += f"|{name}|{domain[value]}|\n"
        return ss
