import re
import utils
import rules


class Parser:
    """
    A Parser reads a text file, applying rules and controlling a
    handler.
    """

    def __init__(self, handler):

        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, inputFile, outputFile):
        self.handler.start('document')
        for block in utils.blocks(inputFile):
            with open(outputFile, 'w') as output:
                for filter in self.filters:
                    block = filter(block, self.handler)
                for rule in self.rules:
                    if rule.condition(block):
                        if rule.action(block, self.handler):
                            break
                output.write(self.handler.getResult())
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its
    constructor.
    """

    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(rules.ListRule())
        self.addRule(rules.ListItemRule())
        self.addRule(rules.TitleRule())
        self.addRule(rules.HeadingRule())
        self.addRule(rules.ParagraphRule())
        self.addFilter('\*(.+?)\*', 'emphasis')
        self.addFilter('(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter('([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')
