import logging
import xml.etree.ElementTree as ElementT


logger = logging.getLogger("Xml Parser")
logging.basicConfig(level=logging.INFO)


def main():
    tree = ElementT.parse("cd_catalog.xml")
    root = tree.getroot()
    parsed_data = []
    for cd in root:
        cd_data = []
        for child in cd:
            if child.tag in ["ARTIST", "TITLE"]:
                cd_data.append(child.text)
        parsed_data.append("("+", ".join(cd_data)+")")

    logger.info("{"+(", ".join(parsed_data)+"}"))


if __name__ == '__main__':
    main()