from typing import Dict


class CSSRule:
    """
    A CSS rule with a selector and properties.

    Attributes:
    -----------
    selector : str
        The selector for the rule.
    properties : Dict[str, str]
        A dictionary of CSS properties and their values for the rule.
    """
    def __init__(self, selector: str) -> None:
        self.selector = selector
        self.properties: Dict[str, str] = {}
    
    def add_property(self, property_name: str, value: str) -> None:
        """Adds a single property to the rule."""
        self.properties[property_name] = value
    
    def add_properties(self, **properties: str) -> None:
        """Adds multiple properties to the rule."""
        self.properties.update(properties)
    
    def __str__(self) -> str:
        """Returns the CSS rule as a string."""
        properties_string = ""
        for property_name, value in self.properties.items():
            properties_string += f"{property_name}: {value};\n"
        
        return f"{self.selector} {{\n{properties_string}}}"


class CSSFile:
    """
    A CSS file containing CSS rules.

    Attributes:
    -----------
    filename : str
        The name of the CSS file.
    rules : List[CSSRule]
        A list of CSS rules in the file.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.rules = []

    def add_rule(self, rule: CSSRule):
        self.rules.append(rule)

    def remove_rule(self, rule: CSSRule):
        self.rules.remove(rule)

    def to_css_string(self) -> str:
        css_string = ""
        for rule in self.rules:
            css_string += rule.to_css_string() + "\n"
        return css_string

    def save(self):
        with open(self.filename, "w") as f:
            f.write(self.to_css_string())
