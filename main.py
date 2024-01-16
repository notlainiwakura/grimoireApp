import sys
from lxml import etree


def generate_unique_xpaths(xml_file_path, element_filter=None):
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    def create_basic_xpath(element):
        if element.get('name'):
            return f"//{element.tag}[@name='{element.get('name')}']"
        elif element.text and element.text.strip():
            return f"//{element.tag}[text()='{element.text.strip()}']"
        else:
            return f"//{element.tag}"

    def create_detailed_xpath(element):
        attributes = [f"@{k}='{v}'" for k, v in element.items()]
        return f"//{element.tag}[{' and '.join(attributes)}]"

    all_xpaths = {}

    for element in root.iter():
        if element_filter and element_filter.lower() not in element.tag.lower():
            continue

        basic_xpath = create_basic_xpath(element)
        count = all_xpaths.get(basic_xpath, 0)

        # Use basic xpath if unique, else create detailed xpath
        xpath = basic_xpath if count == 0 else create_detailed_xpath(element)

        all_xpaths[basic_xpath] = count + 1
        if count > 0:
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
