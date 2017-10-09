def lines(file):
    """
    Adds an empty line at the end of the file
    """
    with open(file, 'r') as input:
        for line in input:
            yield line
        yield '\n'


def blocks(file):
    """
    Join the paragraph text lines in a single string 
    """
    block = []
    with open(file, 'r') as input:
        for line in input:
            if line.strip():
                block.append(line)
            elif block:
                yield ''.join(block).strip()
                block = []
