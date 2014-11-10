class Operator(object):
    negation    = '-'
    con         = '&'
    dis         = '|'
    implication = '->'
    equivalence = '<->'

    @staticmethod
    def equal(this, that):
        if this is that:
            return True
        else:
            return False
