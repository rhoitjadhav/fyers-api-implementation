# Packages
from typing import List, Union
from dataclasses import dataclass, field


@dataclass
class ReturnValue:
    """
    ReturnValue class is responsible for holding returned value
    from operations
    Args:
        success (bool): True if ope
        ration is successful otherwise False
        message (str): message after successful operation
        error (str): error message after failed operation
        data Optional(List, int, str, dict): processed data after operation completion
    """
    success: bool
    message: str = ""
    error: str = ""
    data: Union[List, dict, str, tuple] = field(default_factory=list)
