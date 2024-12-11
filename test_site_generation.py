import unittest

from main import *

class TestSiteGeneration(unittest.TestCase):

    # Section for testing extract_title
    def test_basic_single_header(self):
        input = """
        # Original title supreme

        And some information about it
        """

        result = extract_title(input)
        self.assertEqual("Original title supreme", result)

    def test_deeper_header(self):
        input = """
        Fake header
        Pseudo header
        # The real header
        """

        result = extract_title(input)

        self.assertEqual("The real header", result)
    def test_no_header_extract_title(self):
        input = """
        There are
        no 
        headers
        in this text
        """

        with self.assertRaises(Exception) as context:
            extract_title(input)

        self.assertEqual(str(context.exception), "No title found")
    def test_multiple_headers(self):
        input = """
        #### Quad header
        Info about 4s
        ## Duo header
        Info
        about
        2s
        ### Tri header

        # Number one header
        """

        result = extract_title(input)
        self.assertEqual("Number one header", result)



if __name__ == '__main__':
    unittest.main()