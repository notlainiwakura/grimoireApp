import sys
from lxml import etree

def generate_unique_xpaths(xml_file_path, element_filter=None):
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    def create_xpath(element):
        attributes = [f"@{k}='{v}'" for k, v in element.items()]
        attributes_str = "[" + " and ".join(attributes) + "]" if attributes else ""
        return f"//{element.tag}{attributes_str}"

    def is_unique_xpath(xpath, all_xpaths):
        return all_xpaths.get(xpath, 0) < 1

    all_xpaths = {}

    for element in root.iter():
        if element_filter and element_filter.lower() not in element.tag.lower():
            continue

        xpath = create_xpath(element)
        count = all_xpaths.get(xpath, 0)
        all_xpaths[xpath] = count + 1

        if count > 0:
            # Add index to XPath if it's not unique
            xpath += f"[{count + 1}]"

        yield xpath

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
