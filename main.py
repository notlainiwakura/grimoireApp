import sys
from lxml import etree

def generate_unique_xpaths(xml_file_path, filter_buttons=False):
    """
    Generates unique and precise XPaths  for each element in the XML file.
    Optionally filters to return only elements that are buttons, based on the tag or 'name' attribute.
    """
    # Parse the XML file
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    # Initialize a dictionary to keep track of used XPaths
    used_xpaths = {}

    # Function to check if the element is a button
    def is_button(element):
        tag_contains_button = 'button' in element.tag.lower()
        name_contains_button = 'button' in (element.get('name', '').lower())
        return tag_contains_button or name_contains_button

    # Function to generate XPath with an index if needed for uniqueness
    def generate_xpath_with_index(base_xpath, count):
        if count == 1:
            return base_xpath
        else:
            return f"{base_xpath}[{count}]"

    # Iterate through all elements
    for element in root.iter():
        base_xpath = ''

        # Check if element is a button when filtering
        if filter_buttons and not is_button(element):
            continue

        # Check if 'name' attribute exists
        name = element.get('name')
        if name:
            base_xpath = f"//{element.tag}[@name='{name}']"

        # Check if text content exists and 'name' is not available
        elif element.text and not name:
            text = element.text.strip()
            base_xpath = f"//*[text()='{text}']"

        # Add a count index for uniqueness if needed
        if base_xpath:
            count = used_xpaths.get(base_xpath, 0) + 1
            used_xpaths[base_xpath] = count
            unique_xpath = generate_xpath_with_index(base_xpath, count)
            yield unique_xpath
        else:
            # Indicate if neither 'name' nor text content can be used
            yield "Element cannot be found using 'name' or 'text' tag."

def main(xml_file_path, filter_buttons):
    xpaths = list(generate_unique_xpaths(xml_file_path, filter_buttons))
    for xpath in xpaths:
        print(xpath)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script_name.py <xml_file_path> [buttons]")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    filter_buttons = len(sys.argv) == 3 and sys.argv[2].lower() == "buttons"
    main(xml_file_path, filter_buttons)
