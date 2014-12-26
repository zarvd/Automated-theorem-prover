from render import bcolors
from expression import (Proposition, NotExpression,
                        AndExpression, OrExpression,
                        ImpExpression, EquiExpression)


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
            pre = None
            pre_depth = None
            for formula, depth in old_sequent.pre.items():
                if not pre_depth or pre_depth > depth:
                    if not isinstance(formula, Proposition):
                        pre = formula
                        pre_depth = depth
            con = None
            con_depth = None
            for formula, depth in old_sequent.con.items():
                if not con_depth or con_depth > depth:
                    if not isinstance(formula, Proposition):
                        con = formula
                        con_depth = depth
            apply_pre = None
            if pre or con:
                if not con:
                    apply_pre = True
                elif not pre:
                    apply_pre = False
                elif pre_depth < con_depth:
                    apply_pre = True
                else:
                    apply_pre = False
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
            if apply_pre:
                del sequent_a.pre[pre]
                del sequent_b.pre[pre]

                if isinstance(pre, NotExpression):
                    sequent_a.con[pre.formula] = old_sequent.pre[pre] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(pre, AndExpression):
                    sequent_a.pre[pre.left] = old_sequent.pre[pre] + 1
                    sequent_a.pre[pre.right] = old_sequent.pre[pre] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(pre, OrExpression):
                    sequent_a.pre[pre.left] = old_sequent.pre[pre] + 1
                    sequent_b.pre[pre.right] = old_sequent.pre[pre] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(pre, ImpExpression):
                    sequent_a.pre[pre.right] = old_sequent.pre[pre] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(pre, EquiExpression):
                    sequent_a.pre[pre.left] = old_sequent.pre[pre] + 1
                    sequent_a.pre[pre.right] = old_sequent.pre[pre] + 1
                    conclusion.append(sequent_a)
                    break
            else:
                del sequent_a.con[con]
                del sequent_b.con[con]
                if isinstance(con, NotExpression):
                    sequent_a.pre[con.formula] = old_sequent.con[con] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(con, AndExpression):
                    sequent_a.con[con.left] = old_sequent.con[con] + 1
                    sequent_b.con[con.right] = old_sequent.con[con] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(con, OrExpression):
                    sequent_a.con[con.left] = old_sequent.con[con] + 1
                    sequent_a.con[con.right] = old_sequent.con[con] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(con, ImpExpression):
                    sequent_a.pre[con.left] = old_sequent.con[con] + 1
                    sequent_a.con[con.right] = old_sequent.con[con] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(con, EquiExpression):
                    # sequent_a.pre[con.left] = old_sequent.con[con] + 1
                    sequent_a.con[con.right] = old_sequent.con[con] + 1
                    # sequent_a.pre[con.right] = old_sequent.con[con] + 1
                    sequent_a.con[con.left] = old_sequent.con[con] + 1
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
