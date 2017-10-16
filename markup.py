"""
The program takes a text file as input and gives a html formatetd file
as output.

Example:

    You can use the program as following:

        python markup.py input_file.txt output_file.html

"""
import sys
import handlers
import parsers

if __name__ == '__main__':
    handler = handlers.HTMLRenderer()
    parser = parsers.BasicTextParser(handler)

    parser.parse(sys.argv[1], sys.argv[2])
