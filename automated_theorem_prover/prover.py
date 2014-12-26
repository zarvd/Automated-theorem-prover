from render import bcolors
from expression import (Proposition, NotExpression,
                        AndExpression, OrExpression,
                        ImpExpression)


class Sequent:
    def __init__(self, premises, conclusion, depth):
        self.pre = premises
        self.con = conclusion
        self.depth = depth

    def __eq__(self, other):
        for pre in self.pre:
            if pre not in other.pre:
                return False
        for pre in other.pre:
            if pre not in self.pre:
                return False
        for con in self.con:
            if con not in other.con:
                return False
        for pre in other.con:
            if con not in self.con:
                return False
        return True

    def __str__(self):
        premises = ', '.join([str(premise) for premise in self.pre])
        conclusion = ', '.join([str(conclusion) for conclusion in self.con])
        return premises + ' => ' + conclusion

    def __hash__(self):
        return hash(str(self))


def proveSequent(sequent):
    # TODO: Iff
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
        if len(set(old_sequent.pre.keys()) & set(old_sequent.con.keys())):
            premises.add(old_sequent)
            continue

        while True:
            # determine which formula to expand
            left_formula = None
            left_depth = None
            for formula, depth in old_sequent.pre.items():
                if not left_depth or left_depth > depth:
                    if not isinstance(formula, Proposition):
                        left_formula = formula
                        left_depth = depth
            right_formula = None
            right_depth = None
            for formula, depth in old_sequent.con.items():
                if not right_depth or right_depth > depth:
                    if not isinstance(formula, Proposition):
                        right_formula = formula
                        right_depth = depth
            apply_left = False
            apply_right = False
            if left_formula or right_formula:
                if not right_formula:
                    apply_left = True
                elif not left_formula:
                    apply_right = True
                elif left_depth < right_depth:
                    apply_left = True
                else:
                    apply_right = True
            else:
                return False

            sequent_a = Sequent(
                old_sequent.pre.copy(),
                old_sequent.con.copy(),
                old_sequent.depth + 1
            )
            sequent_b = Sequent(
                old_sequent.pre.copy(),
                old_sequent.con.copy(),
                old_sequent.depth + 1
            )
            # apply a left rule
            if apply_left:
                del sequent_a.pre[left_formula]
                del sequent_b.pre[left_formula]

                if isinstance(left_formula, NotExpression):
                    sequent_a.con[left_formula.formula] = \
                        old_sequent.pre[left_formula] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(left_formula, AndExpression):
                    sequent_a.pre[left_formula.left] = \
                        old_sequent.pre[left_formula] + 1
                    sequent_a.pre[left_formula.right] = \
                        old_sequent.pre[left_formula] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(left_formula, OrExpression):
                    sequent_a.pre[left_formula.left] = \
                        old_sequent.pre[left_formula] + 1
                    sequent_b.pre[left_formula.right] = \
                        old_sequent.pre[left_formula] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(left_formula, ImpExpression):
                    sequent_a.con[left_formula.left] = \
                        old_sequent.pre[left_formula] + 1
                    sequent_b.pre[left_formula.right] = \
                        old_sequent.pre[left_formula] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break

            # apply a right rule
            elif apply_right:
                del sequent_a.con[right_formula]
                del sequent_b.con[right_formula]
                if isinstance(right_formula, NotExpression):
                    sequent_a.pre[right_formula.formula] = \
                        old_sequent.con[right_formula] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(right_formula, AndExpression):
                    sequent_a.con[right_formula.left] = \
                        old_sequent.con[right_formula] + 1
                    sequent_b.con[right_formula.right] = \
                        old_sequent.con[right_formula] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(right_formula, OrExpression):
                    sequent_a.con[right_formula.left] = \
                        old_sequent.con[right_formula] + 1
                    sequent_a.con[right_formula.right] = \
                        old_sequent.con[right_formula] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(right_formula, ImpExpression):
                    sequent_a.pre[right_formula.left] = \
                        old_sequent.con[right_formula] + 1
                    sequent_a.con[right_formula.right] = \
                        old_sequent.con[right_formula] + 1
                    conclusion.append(sequent_a)
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
