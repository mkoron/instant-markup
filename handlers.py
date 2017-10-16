class Handler:
    """
    An object that handles method calls from the Parser.

    The Parser will call the start() and end() methods at the
    beginning each of each block. The sub() method will be used in
    regular expression substitution.

    """

    def __init__(self):
        self.result = ''

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        return lambda match: self.callback(
            'sub_', name, match) or match.group(0)

    def getResult(self):
        return self.result


class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.

    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end() and sub().
    """

    def start_document(self):
        self.result += '<html><head><title>...</title></head><body>'

    def end_document(self):
        self.result += '</body></html>'

    def start_paragraph(self):
        self.result += '<p>'

    def end_paragraph(self):
        self.result += '<p>'

    def start_heading(self):
        self.result += '<h2>'

    def end_heading(self):
        self.result += '</h2>'

    def start_list(self):
        self.result += '<ul>'

    def end_list(self):
        self.result += '</ul>'

    def start_listitem(self):
        self.result += '<li>'

    def end_listitem(self):
        self.result += '</li>'

    def start_title(self):
        self.result += '<h1>'

    def end_title(self):
        self.result += '</h1>'

    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))

    def sub_bold(self, match):
        return '<strong>{}</strong>'.format(match.group(1))

    def sub_url(self, match):
        return '<a href="{url}">{link}</a>'.format(
            url=match.group(1), link=match.group(1))

    def sub_mail(self, match):
        return '<a href="mailto:{url}">{link}</a>'.format(
            url=match.group(1), link=match.group(1))

    def feed(self, data):
        self.result += data
