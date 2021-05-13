import problog


def load(filename):
    parser = problog.parser.PrologParser(problog.program.ExtendedPrologFactory())
    parsed = parser.parseFile(filename)
    print("parsed is:", parsed)
    return parsed
