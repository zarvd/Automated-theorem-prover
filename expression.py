class AtomExpression(object):
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms

    def __eq__(self, other):
        if not isinstance(other, AtomExpression):
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
    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        if not isinstance(other, NotExpression):
            return False
        return self.expression == other.expression

    def __str__(self):
        return '¬' + str(self.expression)

    def __hash__(self):
        return hash(str(self))


class BinaryExpression(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_brother(self, other):
        """If `self` contain `other` return the other child,
        else return False
        Example:
        self.left = A
        self.right = B
        self.get_brother(A) => return B
        self.get_brother(C) => return False

        """
        if self.left == other:
            return self.right
        elif self.right == other:
            return self.left
        else:
            return False


class AndExpression(BinaryExpression):
    def __eq__(self, other):
        if not isinstance(other, AndExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return '(%s ∧ %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))


class OrExpression(BinaryExpression):
    def __eq__(self, other):
        if not isinstance(other, OrExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return '(%s ∨ %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))


class ImpExpression(BinaryExpression):
    def __eq__(self, other):
        if not isinstance(other, ImpExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return '(%s → %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))


class EquiExpression(BinaryExpression):
    def __eq__(self, other):
        if not isinstance(other, EquiExpression):
            return False
        return self.left == other.left and self.right == other.right

    def __str__ (self):
        return '(%s ↔ %s)' % (self.left, self.right)

    def __hash__(self):
        return hash(str(self))
