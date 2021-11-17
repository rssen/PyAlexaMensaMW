import unittest

from handler import xml_parser


class TestGeneratingDishes(unittest.TestCase):
    def test_xml_parser(self):
        all_dishes = xml_parser.parse_xml("test_menu.xml")


if __name__ == '__main__':
    unittest.main()
