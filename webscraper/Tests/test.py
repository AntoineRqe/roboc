# -*- coding: utf-8 -*-

import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.getcwd(), ".."))
from toolbox import *


database_test = os.path.join(os.getcwd(), "Datas", "test.db")
database_entries = [(1, 1, 0, 'https://www.netboxe.fr/'),
                    (2, 1, 1, 'https://www.netboxe.fr/audits-de-securite/'),
                    (3, 1, 1, 'https://www.netboxe.fr/societe/recrutement/')]


class UnitTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(os.path.join(os.getcwd(), "Datas")):
            os.mkdir(os.path.join(os.getcwd(), "Datas"))

    def test_increment_key(self):
        """
        Test increment_key function
        :return:
        """

        for key in range(4, 100):
            self.assertEqual(key, increment_key())

    def test_get_urls_from_page(self):
        """
        Test get_hyperlinks_from_page function
        """

        test = get_urls_from_page("https://www.netboxe.fr/")
        self.assertIsInstance(test, list)
        self.assertNotEqual(len(test), 0)
        self.assertNotIn(None, test)

        with self.assertRaises(TypeError):
            test = get_urls_from_page(102)

        with self.assertRaises(ValueError):
            test = get_urls_from_page("")

        test = get_urls_from_page("https://www.linkedin.com/feed/")
        self.assertListEqual(test, [])

        test = get_urls_from_page("/test")
        self.assertListEqual(test, [])

    def test_is_url_secure(self):
        """
        Test is_url_secure function
        """

        self.assertEqual(is_url_secure("https://www.netboxe.fr/"), 1)
        self.assertEqual(is_url_secure("http://www.netboxe.fr/"), 0)
        self.assertEqual(is_url_secure("www.netboxe.fr/"), 0)

        with self.assertRaises(TypeError):
            is_url_secure(102)

        with self.assertRaises(ValueError):
            is_url_secure("")

    def test_is_absolute_link(self):
        """
        Test is_absolute_link function
        """

        with self.assertRaises(TypeError):
            is_absolute_link(102)

        with self.assertRaises(ValueError):
            is_absolute_link("")

        self.assertTrue(is_absolute_link("https://www.netboxe.fr/"))
        self.assertTrue(is_absolute_link("http://www.netboxe.fr/"))
        self.assertFalse(is_absolute_link("htt://www.netboxe.fr/"))
        self.assertFalse(is_absolute_link("www.netboxe.fr/"))
        self.assertFalse(is_absolute_link("ttps://www.netboxe.fr/"))
        self.assertFalse(is_absolute_link("/asdfcsdfs"))

    def test_is_url_link_to_page(self):
        """
        Test is_url_link_to_page function
        """

        correct_link = "https://www.netboxe.fr/"
        pdf_link = "https://www.netboxe.fr/pdf.pdf"
        mov_link = "https://www.netboxe.fr/mov.mov"

        with self.assertRaises(TypeError):
            is_url_link_to_page(102)

        with self.assertRaises(ValueError):
            is_url_link_to_page("")

        self.assertTrue(is_url_link_to_page(correct_link))
        self.assertFalse(is_url_link_to_page(pdf_link))
        self.assertFalse(is_url_link_to_page(mov_link))

    def test_is_string_in_url(self):
        """
        Test is_string_in_url function
        """
        with self.assertRaises(TypeError):
            is_string_in_url(102, "https://www.netboxe.fr/")

        with self.assertRaises(ValueError):
            is_string_in_url("", "https://www.netboxe.fr/")

        test = "www.netboxe.fr"
        self.assertTrue(is_string_in_url(test, "https://www.netboxe.fr/"))
        self.assertFalse(is_string_in_url(test, "https://www.xco.fr/"))

    def test_create_database(self):
        """
        Test create_database function
        """

        if os.path.exists(database_test):
            os.remove(database_test)

        with self.assertRaises(TypeError):
            create_database(123)

        with self.assertRaises(ValueError):
            create_database("")

        conn, cur = create_database(database_test)

        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsInstance(cur, sqlite3.Cursor)

        with self.assertRaises(sqlite3.OperationalError):
            create_database(database_test)

    def test_construct_database_entry(self):
        """
        Test construct_database_entry function
        """

        with self.assertRaises(ValueError):
            construct_database_entry(-1, "123")
        with self.assertRaises(ValueError):
            construct_database_entry(-1, "")
        with self.assertRaises(TypeError):
            construct_database_entry("hde", "dfsq")
        with self.assertRaises(TypeError):
            construct_database_entry(123, 0)

        test_tuple = construct_database_entry(1, "www.google.fr")
        self.assertIsInstance(test_tuple, tuple)
        self.assertEqual(test_tuple, (1, 0, 1, "www.google.fr"))

        test_tuple = construct_database_entry(2, "http://www.google.fr")
        self.assertIsInstance(test_tuple, tuple)
        self.assertEqual(test_tuple, (2, 0, 2, "http://www.google.fr"))

        test_tuple = construct_database_entry(3, "https://www.google.fr")
        self.assertIsInstance(test_tuple, tuple)
        self.assertEqual(test_tuple, (3, 1, 3, "https://www.google.fr"))

    def test_pretty_print_database(self):
        """
        Test pretty_print_database function
        """

        self.assertIsInstance(pretty_print_database(database_entries), str)

        with self.assertRaises(TypeError):
            pretty_print_database("")
        with self.assertRaises(TypeError):
            pretty_print_database(list())


if __name__ == "__main__":
    unittest.main()
