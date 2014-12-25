class Proposition(object):
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms

    def replace(self, old, new):
        if self == old:
            return new
        return Predicate(self.name,
            [term.replace(old, new) for term in self.terms]
        )

    def occurs(self, unification_term):
        return any([term.occurs(unification_term) for term in self.terms])

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
        if len(self.terms) == 0:
            return self.name
        return self.name + '(' + ', '.join(
            [str(term) for term in self.terms]
        ) + ')'

    def __hash__(self):
        return hash(str(self))


class NotExpression(object):
    def __init__(self, formula):
        self.formula = formula

    def replace(self, old, new):
        if self == old:
            return new
        return Not(self.formula.replace(old, new))

    def occurs(self, unification_term):
        return self.formula.occurs(unification_term)

    def __eq__(self, other):
        if not isinstance(other, Not):
            return False
        return self.formula == other.formula

    def __str__(self):
        return '¬' + str(self.formula)

    def __hash__(self):
        return hash(str(self))


class AndExpression(object):
    def __init__(self, formula_a, formula_b):
        self.formula_a = formula_a
        self.formula_b = formula_b

    def replace(self, old, new):
        if self == old:
            return new
        return And(
            self.formula_a.replace(old, new),
            self.formula_b.replace(old, new)
        )

    def occurs(self, unification_term):
        return self.formula_a.occurs(unification_term) or \
            self.formula_b.occurs(unification_term)

    def __eq__(self, other):
        if not isinstance(other, And):
            return False
        return self.formula_a == other.formula_a and \
            self.formula_b == other.formula_b

    def __str__(self):
        return '(%s ∧ %s)' % (self.formula_a, self.formula_b)

    def __hash__(self):
        return hash(str(self))


class OrExpression(object):
    def __init__(self, formula_a, formula_b):
        self.formula_a = formula_a
        self.formula_b = formula_b

    def replace(self, old, new):
        if self == old:
            return new
        return Or(
            self.formula_a.replace(old, new),
            self.formula_b.replace(old, new)
        )

    def occurs(self, unification_term):
        return self.formula_a.occurs(unification_term) or \
            self.formula_b.occurs(unification_term)

    def __eq__(self, other):
        if not isinstance(other, Or):
            return False
        return self.formula_a == other.formula_a and \
            self.formula_b == other.formula_b

    def __str__(self):
        return '(%s ∨ %s)' % (self.formula_a, self.formula_b)

    def __hash__(self):
        return hash(str(self))


class ImpExpression(object):
    def __init__(self, formula_a, formula_b):
        self.formula_a = formula_a
        self.formula_b = formula_b

    def replace(self, old, new):
        if self == old:
            return new
        return Implies(
            self.formula_a.replace(old, new),
            self.formula_b.replace(old, new)
        )

    def occurs(self, unification_term):
        return self.formula_a.occurs(unification_term) or \
            self.formula_b.occurs(unification_term)

    def __eq__(self, other):
        if not isinstance(other, Implies):
            return False
        return self.formula_a == other.formula_a and \
            self.formula_b == other.formula_b

    def __str__(self):
        return '(%s → %s)' % (self.formula_a, self.formula_b)

    def __hash__(self):
        return hash(str(self))
