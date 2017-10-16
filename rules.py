class Rule:
    """
    Base class for all rules.
    """
    type = ''

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)

        return True


class HeadingRule(Rule):
    """
    A heading is line, with at most 70 characters that
    doesn't end with a colon.
    """
    type = 'heading'

    def condition(self, block):
        return '\n' not in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(HeadingRule):
    """
    First block in the document, provided that is a heading.
    """
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition(self, block)


class ListRule(Rule):
    """
    A list begins between a block that is not a list item and a subsequent
    list item. It ends after the last consecutive item.
    """
    type = 'list'

    def __init__(self):
        self.inside = False

    def condition(self, block):
        if not self.inside and block[0] == '-':
            return True
        elif self.inside and block[0] != '-':
            return True
        return False

    def action(self, block, handler):
        if not self.inside:
            handler.start(self.type)
            self.inside = True
            return False
        else:
            handler.end(self.type)
            self.inside = False
            return True


class ListItemRule(ListRule):
    """
    A list item is a paragraph that begins with a hyphen. During formatting
    the hyphen is removed.
    """
    type = 'listitem'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True


class ParagraphRule(Rule):
    """
    A paragraph is a block of text which isn't covered by any other rules.
    """
    type = 'paragraph'

    def condition(self, block):
        return True
