import sys
import handlers
import parsers

if __name__ == '__main__':
    handler = handlers.HTMLRenderer()
    parser = parsers.BasicTextParser(handler)

    parser.parse(sys.argv[1], sys.argv[2])
