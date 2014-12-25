import re

from prover import proveFormula
from Expression import (Proposition,
                        NotExpression, AndExpression,
                        OrExpression, ImpExpression)


class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message


class Tokens(object):
    # Command
    ADD_PRE = 'pre'
    ADD_CON = 'con'
    SHOW_PRE = 'pres'
    SHOW_CON = 'cons'
    REMOVE = 'remove'
    RESET = 'reset'
    NO_PARA_COM = [SHOW_PRE, SHOW_PRE, RESET]
    WITH_PARA_COM = [ADD_PRE, ADD_CON, REMOVE]
    # Punctuation
    DOT = '.'
    OPEN = '('
    CLOSE = ')'
    COMMA = ','
    # Operations
    NOT = '-';         NOT_LIST = ['not', '-', '!']
    AND = '&';         AND_LIST = ['and', '&', '^']
    OR = '|';          OR_LIST = ['or', '|']
    IMP = '->';        IMP_LIST = ['implies', '->', '=>']
    # IFF = '<->';       IFF_LIST = ['iff', '<->', '<=>']
    # Collections of tokens
    COMMANDS = NO_PARA_COM + WITH_PARA_COM
    BINOPS = AND_LIST + OR_LIST + IMP_LIST
    PUNCT = [DOT, OPEN, CLOSE, COMMA]
    TOKENS = BINOPS + PUNCT + NOT_LIST + COMMANDS

    # Special
    SYMBOLS = [x for x in TOKENS if re.match(r'^[-\\.(),!&^|>=<]*$', x)]


class LogicParser(object):
    premises = set()
    conclusion = {}

    @classmethod
    def fromstring(cls, line):
        tokens = []  # contain premises and operators
        for token in Tokens.SYMBOLS:
            if token in line:
                if token == Tokens.NOT:
                    # TODO: simplify
                    line = line.replace('->', '**')
                    line = line.replace('-', ' - ')
                    line = line.replace('**', '->')
                else:
                    line = line.replace(token, ' '+token+' ')
        words = line.split(' ')
        for word in words:
            if word:
                tokens.append(word)
        return tokens

    @classmethod
    def parse(cls, tokens):
        try:
            for token in tokens[1:]:
                if token in Tokens.COMMANDS:
                    raise InvalidInputError('Unexpected keyword: %s.' % token)
            if tokens:
                if tokens[0] in Tokens.NO_PARA_COM:
                    if len(tokens) > 1:
                        raise InvalidInputError('Unexpected: %s.' % tokens[1])

                    if tokens[0] == Tokens.SHOW_PRE:
                        """Command: show all premises"""
                        for premise in cls.premises:
                            print(premise)
                    elif tokens[0] == Tokens.SHOW_CON:
                        """Command: show all conclusion"""
                        for con in cls.conclusion:
                            print(con)
                    elif tokens[0] == Tokens.RESET:
                        """Command: reset premises and conclusion"""
                        cls.premises = set()
                        cls.conclusion = {}

                elif tokens[0] in Tokens.WITH_PARA_COM:
                    formula = cls.process(tokens[1:])
                    cls.check_formula(formula)

                    if tokens[0] == Tokens.ADD_PRE:
                        """Command: add an premise"""
                        cls.premises.add(formula)
                        print('Premise added: %s.' % formula)
                    elif tokens[0] == Tokens.ADD_CON:
                        """Command: add an conclusion"""
                        result = proveFormula(cls.premises | set(cls.conclusion.keys()), formula)
                        if result:
                            cls.conclusion[formula] = cls.premises.copy()
                            print('Conclusion proven: %s.' % formula)
                        else:
                            print('Conclusion unprovable: %s.' % formula)
                    elif tokens[0] == Tokens.REMOVE:
                        """Command: remove an premise or conclusion"""
                        if formula in cls.premises:
                            # Remove the premise if it stored in premises
                            cls.premises.remove(formula)
                            related_conclusion = []
                            for con, related_premises in cls.conclusion.items():
                                if formula in related_premises:
                                    related_conclusion.append(con)
                            for con in related_conclusion:
                                del cls.conclusion[con]
                            print('Premise removed: %s.' % formula)
                            print('These conclusion were proven using that ' \
                                'premises and were also removed:')
                            index = 1
                            for con in related_conclusion:
                                print('[d]    %s' % (index, con))
                                index += 1
                        elif formula in cls.conclusion:
                            del cls.conclusion[formula]
                            print('Conclusion removed: %s.' % formula)
                        else:
                            print('Not an premise or conclusion: %s.' % formula)
            else:
                formula = cls.process(tokens)
                cls.check_formula(formula)
                result = proveFormula(cls.premises | set(cls.conclusion.keys()), formula)
                if result:
                    print('Formula proven: %s.' % formula)
                else:
                    print('Formula unprovable: %s.' % formula)
        except InvalidInputError as e:
            print(e.message)

    @classmethod
    def process(cls, tokens):
        if not tokens:
            raise InvalidInputError('Empty formula.')

        # Implies
        pos = None

        _imp = None
        _or = None
        _and = None

        depth = 0
        for i in range(len(tokens)):
            if tokens[i] == Tokens.OPEN:
                depth += 1
                continue
            elif tokens[i] == Tokens.CLOSE:
                depth -= 1
                continue
            elif depth == 0 and tokens[i] in Tokens.IMP_LIST:
                pos = i
                _imp = True
                break
            elif depth == 0 and tokens[i] in Tokens.OR_LIST:
                pos = i
                _or = True
                break
            elif depth == 0 and tokens[i] in Tokens.AND_LIST:
                pos = i
                _and = True
                break
        if pos:
            quantifier_in_left = False
            depth = 0
            for i in range(pos):
                if tokens[i] == Tokens.OPEN:
                    depth += 1
                    continue
                if tokens[i] == Tokens.CLOSE:
                    depth -= 1
                    continue
            if not quantifier_in_left:
                if _imp:
                    if pos == len(tokens) - 1:
                        raise InvalidInputError('Missing formula in IMPLIES connective.')
                    return ImpExpression(cls.process(tokens[0:pos]),
                        cls.process(tokens[pos+1:]))
                elif _or:
                    if pos == len(tokens) - 1:
                        raise InvalidInputError('Missing formula in OR connective.')
                    return OrExpression(cls.process(tokens[0:pos]), cls.process(tokens[pos+1:]))
                elif _and:
                    if pos == len(tokens) - 1:
                        raise InvalidInputError('Missing formula in AND connective.')
                    return AndExpression(cls.process(tokens[0:pos]), cls.process(tokens[pos+1:]))

        # Not
        if tokens[0] in Tokens.NOT_LIST:
            if len(tokens) < 2:
                raise InvalidInputError('Missing formula in NOT connective.')
            return NotExpression(cls.process(tokens[1:]))

        # Proposition
        if tokens[0].isalnum() and tokens[0].lower() not in Tokens.TOKENS and \
            len(tokens) == 1 and any([c.isupper() for c in tokens[0]]):
            return Proposition(tokens[0], [])
        if tokens[0].isalnum() and tokens[0].lower() not in Tokens.TOKENS and \
            len(tokens) > 1 and any([c.isupper() for c in tokens[0]]) and \
            tokens[1] == Tokens.OPEN:
            if tokens[-1] != Tokens.CLOSE:
                raise InvalidInputError('Missing \')\' after proposition argument list.')
            name = tokens[0]
            args = []
            i = 2
            if i < len(tokens) - 1:
                while i <= len(tokens) - 1:
                    end = len(tokens) - 1
                    depth = 0
                    for j in range(i, len(tokens) - 1):
                        if tokens[j] == Tokens.OPEN:
                            depth += 1
                            continue
                        if tokens[j] == Tokens.CLOSE:
                            depth -= 1
                            continue
                        if depth == 0 and tokens[j] == Tokens.COMMA:
                            end = j
                            break
                    if i == end:
                        raise InvalidInputError('Missing proposition argument.')
                    args.append(cls.process(tokens[i:end]))
                    i = end + 1
            return Proposition(name, args)

        # Group
        if tokens[0] == Tokens.OPEN:
            if tokens[-1] != Tokens.CLOSE:
                raise InvalidInputError('Missing \')\'.')
            if len(tokens) == 2:
                raise InvalidInputError('Missing formula in parenthetical group.')
            return cls.process(tokens[1:-1])

        raise InvalidInputError('Unable to parse: %s...' % tokens[0])

    @classmethod
    def check_formula(cls, formula):
        if isinstance(formula, Proposition):
            return
        if isinstance(formula, NotExpression):
            cls.check_formula(formula.formula)
            return
        if isinstance(formula, AndExpression):
            cls.check_formula(formula.formula_a)
            cls.check_formula(formula.formula_b)
            return
        if isinstance(formula, OrExpression):
            cls.check_formula(formula.formula_a)
            cls.check_formula(formula.formula_b)
            return
        if isinstance(formula, ImpExpression):
            cls.check_formula(formula.formula_a)
            cls.check_formula(formula.formula_b)
            return
        raise InvalidInputError('Invalid formula: %s.' % formula)
