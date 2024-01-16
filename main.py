import sys
from lxml import etree

def generate_unique_xpaths(xml_file_path, element_filter=None):
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    used_xpaths = {}

    def is_specific_element(element, filter_type):
        if filter_type is None:
            return True

        filter_type = filter_type.lower()
        tag = element.tag.lower()

        # Check if filter_type is a substring of tag
        return filter_type in tag

    def generate_xpath_with_index(base_xpath, count):
        return f"{base_xpath}[{count}]" if count > 1 else base_xpath

    for element in root.iter():
        base_xpath = ''

        if not is_specific_element(element, element_filter):
            continue

        # Prioritize name and tag over text for XPath generation
        name = element.get('name')
        if name:
            base_xpath = f"//{element.tag}[@name='{name}']"
        elif element.tag and not element.text:
            base_xpath = f"//{element.tag}"

        if base_xpath:
            count = used_xpaths.get(base_xpath, 0) + 1
            used_xpaths[base_xpath] = count
            unique_xpath = generate_xpath_with_index(base_xpath, count)
            yield unique_xpath

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
