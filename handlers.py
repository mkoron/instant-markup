class Handler:
    """
    An object that handles method calls from the Parser.

    The Parser will call the start() and end() methods at the 
    beginning each of each block. The sub() method will be used in 
    regular expression substitution.

    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)
    
    def end(self, name):
        self.callback('end_', name)
    
    def sub(self, name):
        return lambda match: self.callback('sub_', name, match) or match.group(0)

class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.

    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end() and sub().
    """
    def start_document(self):
        print('<html><head><title>...</title></head><body>')
    def end_document(self):
        print('</body></html>')
    def start_paragraph(self):
        print('<p>')
    def end_paragraph(self):
        print('<p>')
    def start_heading(self):
        print('<h2>')
    def end_heading(self):
        print('</h2>')
    def start_list(self):
        print('<ul>')
    def end_list(self):
        print('</ul>')
    def start_listitem(self):
        print('<li>')
    def end_listitem(self):
        print('</li>')
    def start_title(self):
        print('<h1>')
    def end_title(self):
        print('</h1>')
    def sub_emphasis(self, match):
        return '<em>{}</em>'.format(match.group(1))
    def sub_url(self, match):
        return '<a href="{url}">{link}</a>'.format(url=match.group(1), link=match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:{url}">{link}</a>'.format(url=match.group(1), link=match.group(1))
    def feed(self, data):
        print(data)
