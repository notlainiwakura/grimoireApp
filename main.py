import sys
from lxml import etree

def generate_unique_xpaths(xml_file_path, element_filter=None):
    # Parse the XML file
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    # Initialize a dictionary to keep track of used XPaths
    used_xpaths = {}

    # Function to check if the element matches the specified filter
    def is_specific_element(element, filter_type):
        if filter_type is None:
            return True

        filter_type = filter_type.lower()
        tag = element.tag.lower()
        name = element.get('name', '').lower()

        # Check if filter_type is a substring of tag or name
        return filter_type in tag or filter_type in name

    # Function to generate XPath with an index if needed for uniqueness
    def generate_xpath_with_index(base_xpath, count):
        if count == 1:
            return base_xpath
        else:
            return f"{base_xpath}[{count}]"

    # Iterate through all elements
    for element in root.iter():

        base_xpath = ''

        # Check if element matches the specified filter
        if not is_specific_element(element, element_filter):
            continue

        # Generate base XPath
        name = element.get('name')
        if name:
            base_xpath = f"//{element.tag}[@name='{name}']"
        elif element.text:
            text = element.text.strip()
            base_xpath = f"//*[text()='{text}']"

        # Add a count index for uniqueness if needed
        if base_xpath:
            count = used_xpaths.get(base_xpath, 0) + 1
            used_xpaths[base_xpath] = count
            unique_xpath = generate_xpath_with_index(base_xpath, count)
            yield unique_xpath
        else:
            yield "Element cannot be found using 'name' or 'text' tag."

def main(xml_file_path, element_filter):
    xpaths = list(generate_unique_xpaths(xml_file_path, element_filter))
    for xpath in xpaths:
        print(xpath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <xml_file_path> [filter]")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    element_filter = sys.argv[2] if len(sys.argv) > 2 else None
    main(xml_file_path, element_filter)
