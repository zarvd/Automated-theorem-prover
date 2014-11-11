class Operator(object):
    negative    = '-'
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

    @staticmethod
    def items():
        return [Operator.negative,
                Operator.con,
                Operator.dis,
                Operator.implication,
                Operator.equivalence
                ]
