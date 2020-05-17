from typing import Any
from typing import Iterable

from selenium.common import exceptions


class AnyEC:
    """Use with WebDriverWait to combine expected_conditions in an OR."""

    def __init__(self, *ecs):
        self.ecs = ecs  # type: Iterable[Any]

    def __call__(self, driver):
        for ec in self.ecs:
            try:
                if ec(driver):
                    return True
            except exceptions.WebDriverException:
                pass
