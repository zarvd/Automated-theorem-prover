import re


class Tokens(object):
    LAMBDA = '\\';     LAMBDA_LIST = ['\\']

    #Quantifiers
    EXISTS = 'exists'; EXISTS_LIST = ['some', 'exists', 'exist']
    ALL = 'all';       ALL_LIST = ['all', 'forall']

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
    QUANTS = EXISTS_LIST + ALL_LIST
    PUNCT = [DOT, OPEN, CLOSE, COMMA]

    TOKENS = BINOPS + EQ_LIST + NEQ_LIST + QUANTS + LAMBDA_LIST + PUNCT + NOT_LIST

    #Special
    SYMBOLS = [x for x in TOKENS if re.match(r'^[-\\.(),!&^|>=<]*$', x)]


class LogicParser(object):
    """A lambda calculus expression parser."""
    def parser(self, data):
        """
        Parse the expression.

        :param data: str for the input to be parsed
        :returns: a parsed Expression
        """
        pass


class Expression(object):
    """This is the base abstract object for all logical expressions"""
    _logic_parser = LogicParser()

    @classmethod
    def fromstring(cls, s):
        return cls._logic_parser.parse(s)


class NegatedExpression(Expression):
    pass


class BinaryExpression(Expression):
    pass


class BooleanExpression(BinaryExpression):
    pass


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
