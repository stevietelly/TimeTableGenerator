from typing import List, Dict

class DOMNode:
    def __init__(self, tag: str, closing_tag=True) -> None:
        """
        The DOMNode class represents a single node in the Document Object Model (DOM).
        It can contain child nodes, attributes, and styles.

        Attributes:
            tag (str): The tag name of the node (e.g. 'div', 'p', 'a')
            closing_tag (bool): Whether the node should have a closing tag (default: True)
            text (str): The text content of the node
            attributes (List[Dict[str, str]]): The attributes of the node
            children (List[DOMNode]): The child nodes of the node
            class_list (List[str]): The list of CSS classes of the node
        """

        self.tag = tag
        self.attributes: List[Dict[str, str]] = []
        self.children: List['DOMNode'] = []

        self.class_list = []
        self.id = ""
        self.styles = {}
        self.text = ""

        self.closing_tag = closing_tag
    
    def add_attribute(self, attribute: Dict[str, str]):
        """Adds an attribute to this node"""
        self.attributes.append(attribute)
    
    def append_child(self, child_node):
        """Adds a child node to this node"""
        self.children.append(child_node)
    
    def add_class(self, *class_:str):
        """Adds one or more classes to this node"""
        [self.class_list.append(cls_) for cls_ in class_]
    
    def remove_class(self, class_:str):
        """Removes a class from this node"""
        self.class_list.pop(self.class_list.index(class_))
        
    def add_style(self, **styles):
        """Adds one or more styles to this node"""
        self.styles.update(styles)
    
    def set_text(self, text: str) -> None:
        """Sets the text content of the node."""
        self.text = text
    
    def get_elements_by_id(self, id_name: str) -> List['DOMNode']:
        result = []
        for element in self.children:
            if element.id == id_name:
                result.append(element)
        return result
        
    def get_elements_by_tagname(self, tag_name: str) -> List['DOMNode']:
        result = []
        for element in self.children:
            if element.tag == tag_name:
                result.append(element)
        return result
        
    def get_elements_by_class(self, class_name: str) -> List['DOMNode']:
        result = []
        for element in self.children:
            if class_name in self.class_list:
                result.append(element)
        return result

    def get_elements_by_attributes(self, attribute: Dict[str, str]) -> List['DOMNode']:
        result = []
        for element in self.children:
            if attribute in self.attributes:
                result.append(element)
        return result
    
    
    def __str__(self):
        """Converts the node and its children to HTML."""
        if not self.closing_tag:
            return f"<{self.tag}>"

        attr_str = ""
        for attribute in self.attributes:
            for name, value in attribute.items():
                attr_str += f' {name}="{value}"'
        class_str = ""
        if self.class_list:
            class_str = f' class="{self.class_list}"'
        style_str = ""
        if self.styles:
            style_str = " ".join([f"{name}:{value};" for name, value in self.styles.items()])
            style_str = f' style="{style_str}"'
        content_str = self.text
        for child in self.children:
            content_str += str(child)
        return f"<{self.tag}{attr_str}{class_str}{style_str}>{content_str}</{self.tag}>"

    
class DOMTree:
    def __init__(self, title: str, filename: str) -> None:
        self.head = DOMNode("head")
        self.body = DOMNode("body")
        self.title = title
        self.filename = filename
        
    def add_stylesheet(self, href: str) -> None:
        link_node = DOMNode("link")
        link_node.add_attribute({"rel": "stylesheet", "href": href})
        self.head.append_child(link_node)
        
    def add_script(self, src: str) -> None:
        script_node = DOMNode("script")
        script_node.add_attribute({"src": src})
        self.head.append_child(script_node)
        
    def add_element(self, element: DOMNode) -> None:
        self.body.append_child(element)
        
    def get_elements_by_id(self, id_name: str) -> List[DOMNode]:
        return self.body.get_elements_by_id(id_name)
        
    def get_elements_by_tagname(self, tag_name: str) -> List[DOMNode]:
        return self.body.get_elements_by_tagname(tag_name)
        
    def get_elements_by_class(self, class_name: str) -> List[DOMNode]:
        return self.body.get_elements_by_class(class_name)
    
    def get_elements_by_attributes(self, attribute: Dict[str, str]) -> List[DOMNode]:
        return self.body.get_elements_by_attributes(attribute)
    
    def __str__(self) -> str:
        return f"<!DOCTYPE html>\n<html>\n{str(self.head)}{str(self.body)}\n</html>"
    
    def save(self) -> None:
        with open(self.filename, "w") as f:
            f.write(str(self))


class HTMLParser:
    def __init__(self, filename:str):
        self.filename = filename
        self.root = DOMTree()
    def open_file(self):
        with open(self.filename) as file:
            self.content = file.read()     