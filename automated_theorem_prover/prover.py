from render import bcolors
from Expression import (Proposition, NotExpression,
                        AndExpression, OrExpression,
                        ImpExpression)


class Sequent:
    def __init__(self, left, right, depth):
        self.left = left
        self.right = right
        self.depth = depth

    def __eq__(self, other):
        for formula in self.left:
            if formula not in other.left:
                return False
        for formula in other.left:
            if formula not in self.left:
                return False
        for formula in self.right:
            if formula not in other.right:
                return False
        for formula in other.right:
            if formula not in self.right:
                return False
        return True

    def __str__(self):
        left_part = ', '.join([str(formula) for formula in self.left])
        right_part = ', '.join([str(formula) for formula in self.right])
        if left_part != '':
            left_part = left_part + ' '
        if right_part != '':
            right_part = ' ' + right_part
        return left_part + '⊢' + right_part

    def __hash__(self):
        return hash(str(self))


def proveSequent(sequent):
    conclusion = [sequent]

    premises = {sequent}

    while True:
        # get the next sequent
        old_sequent = None
        while conclusion and (not old_sequent or old_sequent in premises):
            old_sequent = conclusion.pop(0)
        if not old_sequent:
            break
        bcolors.print_ok('[%s] %s' % (old_sequent.depth, old_sequent))

        # check if this sequent is axiomatically true without unification
        if len(set(old_sequent.left.keys()) & set(old_sequent.right.keys())):
            premises.add(old_sequent)
            continue

        while True:
            # determine which formula to expand
            left_formula = None
            left_depth = None
            for formula, depth in old_sequent.left.items():
                if left_depth is None or left_depth > depth:
                    if not isinstance(formula, Proposition):
                        left_formula = formula
                        left_depth = depth
            right_formula = None
            right_depth = None
            for formula, depth in old_sequent.right.items():
                if right_depth is None or right_depth > depth:
                    if not isinstance(formula, Proposition):
                        right_formula = formula
                        right_depth = depth
            apply_left = False
            apply_right = False
            if left_formula and not right_formula:
                apply_left = True
            if not left_formula and right_formula:
                apply_right = True
            if left_formula and right_formula:
                if left_depth < right_depth:
                    apply_left = True
                else:
                    apply_right = True
            if not left_formula and not right_formula:
                return False

            # apply a left rule
            if apply_left:
                new_sequent_a = Sequent(
                    old_sequent.left.copy(),
                    old_sequent.right.copy(),
                    old_sequent.depth + 1
                )
                new_sequent_b = Sequent(
                    old_sequent.left.copy(),
                    old_sequent.right.copy(),
                    old_sequent.depth + 1
                )
                del new_sequent_a.left[left_formula]
                del new_sequent_b.left[left_formula]

                if isinstance(left_formula, NotExpression):
                    new_sequent_a.right[left_formula.formula] = \
                        old_sequent.left[left_formula] + 1
                    conclusion.append(new_sequent_a)
                    break
                elif isinstance(left_formula, AndExpression):
                    new_sequent_a.left[left_formula.left] = \
                        old_sequent.left[left_formula] + 1
                    new_sequent_a.left[left_formula.right] = \
                        old_sequent.left[left_formula] + 1
                    conclusion.append(new_sequent_a)
                    break
                elif isinstance(left_formula, OrExpression):
                    new_sequent_a.left[left_formula.left] = \
                        old_sequent.left[left_formula] + 1
                    new_sequent_b.left[left_formula.right] = \
                        old_sequent.left[left_formula] + 1
                    conclusion.append(new_sequent_a)
                    conclusion.append(new_sequent_b)
                    break
                elif isinstance(left_formula, ImpExpression):
                    new_sequent_a.right[left_formula.left] = \
                        old_sequent.left[left_formula] + 1
                    new_sequent_b.left[left_formula.right] = \
                        old_sequent.left[left_formula] + 1
                    conclusion.append(new_sequent_a)
                    conclusion.append(new_sequent_b)
                    break

            # apply a right rule
            if apply_right:
                new_sequent_a = Sequent(
                    old_sequent.left.copy(),
                    old_sequent.right.copy(),
                    old_sequent.depth + 1
                )
                new_sequent_b = Sequent(
                    old_sequent.left.copy(),
                    old_sequent.right.copy(),
                    old_sequent.depth + 1
                )
                del new_sequent_a.right[right_formula]
                del new_sequent_b.right[right_formula]
                if isinstance(right_formula, NotExpression):
                    new_sequent_a.left[right_formula.formula] = \
                        old_sequent.right[right_formula] + 1
                    conclusion.append(new_sequent_a)
                    break
                elif isinstance(right_formula, AndExpression):
                    new_sequent_a.right[right_formula.left] = \
                        old_sequent.right[right_formula] + 1
                    new_sequent_b.right[right_formula.right] = \
                        old_sequent.right[right_formula] + 1
                    conclusion.append(new_sequent_a)
                    conclusion.append(new_sequent_b)
                    break
                elif isinstance(right_formula, OrExpression):
                    new_sequent_a.right[right_formula.left] = \
                        old_sequent.right[right_formula] + 1
                    new_sequent_a.right[right_formula.right] = \
                        old_sequent.right[right_formula] + 1
                    conclusion.append(new_sequent_a)
                    break
                elif isinstance(right_formula, ImpExpression):
                    new_sequent_a.left[right_formula.left] = \
                        old_sequent.right[right_formula] + 1
                    new_sequent_a.right[right_formula.right] = \
                        old_sequent.right[right_formula] + 1
                    conclusion.append(new_sequent_a)
                    break
    return True


def proveFormula(premises, conclusion):
    """
    :return bool: true if it's provable
    """
    return proveSequent(Sequent(
        {premise: 0 for premise in premises},
        {conclusion: 0},
        0
    ))
