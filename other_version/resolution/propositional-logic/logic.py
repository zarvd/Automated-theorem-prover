import re


class Tokens(object):
    #Punctuation
    DOT = '.'
    OPEN = '('
    CLOSE = ')'
    COMMA = ','
    #Operations
    NOT = '-';         NOT_LIST = ['not', '-', '!']
    AND = '&';         AND_LIST = ['and', '&', '^']
    OR = '|';          OR_LIST = ['or', '|']
    IMP = '->';        IMP_LIST = ['implies', '->', '=>']
    IFF = '<->';       IFF_LIST = ['iff', '<->', '<=>']
    EQ = '=';          EQ_LIST = ['=', '==']
    NEQ = '!=';        NEQ_LIST = ['!=']
    #Collections of tokens
    BINOPS = AND_LIST + OR_LIST + IMP_LIST + IFF_LIST
    PUNCT = [DOT, OPEN, CLOSE, COMMA]
    TOKENS = BINOPS + EQ_LIST + NEQ_LIST + PUNCT + NOT_LIST

    #Special
    SYMBOLS = [x for x in TOKENS if re.match(r'^[-\\.(),!&^|>=<]*$', x)]


class LogicParser(object):
    """A lambda calculus expression parser."""
    def __init__(self):
        self._currentIndex = 0
        self._buffer = []
        self.quote_chars = []

        self.operator_precedence = dict(
                           [(x,1) for x in Tokens.NOT_LIST]                + \
                           [(x,2) for x in Tokens.EQ_LIST+Tokens.NEQ_LIST] + \
                           [(x,3) for x in Tokens.AND_LIST]                + \
                           [(x,4) for x in Tokens.OR_LIST]                 + \
                           [(x,5) for x in Tokens.IMP_LIST]                + \
                           [(x,6) for x in Tokens.IFF_LIST]                + \
                           [(None,7)])

    def parser(self, data):
        """
        Parse the expression.

        :param data: str for the input to be parsed
        :returns: a parsed Expression
        """
        data = data.replace(' ', '')
        result = self.process(data)
        return result

    def process(self, data):
        """Split the data into tokens"""
        current_index = 0
        quote_count = 0

        for index in range(len(data)):
            char = data[index]
            if char == Tokens.OPEN:
                quote_count += 1
            elif char == Tokens.CLOSE:
                quote_count -= 1
                if not quote_count:
                    current_index = index
                    break
            elif not quote_count and not char.isspace():
                token = self._process_get_token(data[index:])
                if token in Tokens.TOKENS:
                    

    def _process_get_token(self, data):
        pass                

    def get_all_symbols(self):
        """This method exists to be overridden"""
        return Tokens.SYMBOLS


class Expression(object):
    """This is the base abstract object for all logical expressions"""
    _logic_parser = LogicParser()

    @classmethod
    def fromstring(cls, s):
        return cls._logic_parser.parse(s)

    def __neg__(self):
        return NegatedExpression(self)

    def negate(self):
        """If this is a negated expression, remove the negation.
        Otherwise add a negation."""
        return -self

    def __and__(self, other):
        if not isinstance(other, Expression):
            raise TypeError("%s is not an Expression" % other)
        return AndExpression(self, other)

    def __or__(self, other):
        if not isinstance(other, Expression):
            raise TypeError("%s is not an Expression" % other)
        return OrExpression(self, other)

    def __gt__(self, other):
        if not isinstance(other, Expression):
            raise TypeError("%s is not an Expression" % other)
        return ImpExpression(self, other)

    def __lt__(self, other):
        if not isinstance(other, Expression):
            raise TypeError("%s is not an Expression" % other)
        return IffExpression(self, other)

    def __eq__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return self.str()

    def equiv(self, other, prover=None):
        """
        Check for logical equivalence.
        Pass the expression (self <-> other) to the theorem prover.
        If the prover says it is valid, then the self and other are equal.

        :param other: an ``Expression`` to check equality against
        :param prover: a ``nltk.inference.api.Prover``
        """
        assert isinstance(other, Expression), "%s is not an Expression" % other

        if prover is None:
            from nltk.inference import Prover9
            prover = Prover9()
        bicond = IffExpression(self.simplify(), other.simplify())
        return prover.prove(bicond)


class NegatedExpression(Expression):
    pass


class IndividualExpression(Expression):
    def __init__(self, value):
        self.value = value


class BinaryExpression(Expression):
    def __init__(self, first, second):
        assert isinstance(first, Expression), "%s is not an Expression" % first
        assert isinstance(second, Expression), "%s is not an Expression" % second
        self.first = first
        self.second = second

    def __eq__(self, other):
        return (isinstance(self, other.__class__) or \
                isinstance(other, self.__class__)) and \
               self.first == other.first and self.second == other.second

    def __ne__(self, other):
        return not self == other

    __hash__ = Expression.__hash__

    def __str__(self):
        first = self._str_subex(self.first)
        second = self._str_subex(self.second)
        return Tokens.OPEN + first + ' ' + self.getOp() \
                + ' ' + second + Tokens.CLOSE

    def _str_subex(self, subex):
        return "%s" % subex


class BooleanExpression(BinaryExpression):
    def _set_type(self, other_type=ANY_TYPE, signature=None):
        """:see Expression._set_type()"""
        assert isinstance(other_type, Type)

        if signature is None:
            signature = defaultdict(list)

        if not other_type.matches(TRUTH_TYPE):
            raise IllegalTypeException(self, other_type, TRUTH_TYPE)
        self.first._set_type(TRUTH_TYPE, signature)
        self.second._set_type(TRUTH_TYPE, signature)


class AndExpression(BooleanExpression):
    """This class represents conjunctions"""
    def getOp(self):
        return Tokens.AND

    def _str_subex(self, subex):
        s = "%s" % subex
        if isinstance(subex, AndExpression):
            return s[1:-1]
        return s

class OrExpression(BooleanExpression):
    """This class represents disjunctions"""
    def getOp(self):
        return Tokens.OR

    def _str_subex(self, subex):
        s = "%s" % subex
        if isinstance(subex, OrExpression):
            return s[1:-1]
        return s

class ImpExpression(BooleanExpression):
    """This class represents implications"""
    def getOp(self):
        return Tokens.IMP

class IffExpression(BooleanExpression):
    """This class represents biconditionals"""
    def getOp(self):
        return Tokens.IFF


class EqualityExpression(BinaryExpression):
    """This class represents equality expressions like "(x = y)"."""
    def getOp(self):
        return Tokens.EQ
