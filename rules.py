class Rule:
    """
    Base class for all rules.
    """

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


class ListItemRule(Rule):
    """
    A list item is a paragraph that begins with a hypen. During formatting
    the hypen is removed.
    """
    type = 'listitem'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)


class ListRule(ListItemRule):
    """
    A list begins between a block that is not a list item and a subsequent
    list item. It ends after the last consecutive item.
    """
    type = 'list'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.indside = False
        return False


class ParagraphRule(Rule):
    """
    A paragraph is a block of text which isn't covered by any other rules.
    """
    type = 'pararaph'

    def condition(self, block):
        return True
