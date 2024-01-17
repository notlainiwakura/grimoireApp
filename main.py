import sys
import json
from lxml import etree
import os


def generate_unique_xpaths(xml_file_path, element_filter=None):
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    xpath_data = []

    for element in root.iter():
        if element_filter and element_filter.lower() not in element.tag.lower():
            continue

        element_data = {
            "name": element.tag,
            "SimpleName": element.get('name', element.tag),
            "XPath": generate_xpath(element)
        }
        xpath_data.append(element_data)

    return xpath_data


def generate_xpath(element):
    if element.get('name'):
        return f"//{element.tag}[@name='{element.get('name')}']"
    elif element.text and element.text.strip():
        return f"//{element.tag}[text()='{element.text.strip()}']"
    else:
        return f"//{element.tag}"


def write_to_json_file(xpath_data, output_file):
    output = {data["name"]: {
        "SimpleName": data["SimpleName"],
        "locators": {
            "Roku": {
                "AllLocales": {
                    "AllDevices": f"XPath::{data['XPath']}"
                }
            }
        }
    } for data in xpath_data}

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output, file, indent=4)


def get_json_filename(tree):
    root = tree.getroot()
    for element in root.iter():
        if 'BaseScreen' in element.get('extends', ''):
            return element.tag + '.json'
    return 'default_output.json'


def main(xml_file_path, element_filter):
    tree = etree.parse(xml_file_path)
    json_filename = get_json_filename(tree)
    xpath_data = generate_unique_xpaths(xml_file_path, element_filter)
    output_file = os.path.join(os.path.dirname(xml_file_path), json_filename)
    write_to_json_file(xpath_data, output_file)
    print(f"XPaths have been written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <xml_file_path> [filter]")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    element_filter = sys.argv[2] if len(sys.argv) > 2 else None
    main(xml_file_path, element_filter)
