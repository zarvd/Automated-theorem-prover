class Proposition(object):
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms

    def __eq__(self, other):
        if not isinstance(other, Proposition):
            return False
        if self.name != other.name:
            return False
        if len(self.terms) != len(other.terms):
            return False
        return all(
            [self.terms[i] == other.terms[i] for i in range(len(self.terms))]
        )

    def __str__(self):
        if not self.terms:
            return self.name
        return self.name + '(' + ', '.join(
            [str(term) for term in self.terms]
        ) + ')'

    def __hash__(self):
        return hash(str(self))


class NotExpression(object):
    def __init__(self, formula):
        self.formula = formula

    def __eq__(self, other):
        if not isinstance(other, NotExpression):
            return False
        return self.formula == other.formula

    def __str__(self):
        return '¬' + str(self.formula)

    def __hash__(self):
        return hash(str(self))


class AndExpression(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, AndExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return '(%s ∧ %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))


class OrExpression(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, OrExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return '(%s ∨ %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))


class ImpExpression(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, ImpExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return '(%s → %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))


class EquiExpression(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, IffExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__ (self):
        return '(%s ↔ %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))
