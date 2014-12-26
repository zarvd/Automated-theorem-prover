from render import bcolors
from expression import (Proposition, NotExpression,
                        AndExpression, OrExpression,
                        ImpExpression, EquiExpression)


class Sequent:
    def __init__(self, premises, conclusion, depth):
        self.pres = premises
        self.cons = conclusion
        self.depth = depth

    def __eq__(self, other):
        for pre in self.pres:
            if pre not in other.pres:
                return False
        for pre in other.pres:
            if pre not in self.pres:
                return False
        for con in self.cons:
            if con not in other.cons:
                return False
        for pre in other.cons:
            if con not in self.cons:
                return False
        return True

    def __str__(self):
        premises = ', '.join([str(premise) for premise in self.pres])
        conclusion = ', '.join([str(conclusion) for conclusion in self.cons])
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
        if len(set(old_sequent.pres.keys()) & set(old_sequent.cons.keys())):
            premises.add(old_sequent)
            continue

        while True:
            pre = None
            pre_depth = None
            for formula, depth in old_sequent.pres.items():
                if not pre_depth or pre_depth > depth:
                    if not isinstance(formula, Proposition):
                        pre = formula
                        pre_depth = depth
            con = None
            con_depth = None
            for formula, depth in old_sequent.cons.items():
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
                old_sequent.pres.copy(),
                old_sequent.cons.copy(),
                old_sequent.depth + 1
            )
            sequent_b = Sequent(
                old_sequent.pres.copy(),
                old_sequent.cons.copy(),
                old_sequent.depth + 1
            )
            if apply_pre:
                del sequent_a.pres[pre]
                del sequent_b.pres[pre]

                if isinstance(pre, NotExpression):
                    sequent_a.cons[pre.formula] = old_sequent.pres[pre] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(pre, AndExpression):
                    sequent_a.pres[pre.left] = old_sequent.pres[pre] + 1
                    sequent_a.pres[pre.right] = old_sequent.pres[pre] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(pre, OrExpression):
                    sequent_a.pres[pre.left] = old_sequent.pres[pre] + 1
                    sequent_b.pres[pre.right] = old_sequent.pres[pre] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(pre, ImpExpression):
                    # transfer ImpExpression to OrExpression
                    sequent_a.pres[NotExpression(pre.left)] = old_sequent.pres[pre] + 1
                    sequent_b.pres[pre.right] = old_sequent.pres[pre] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(pre, EquiExpression):
                    # transfer EquiExpression to ImpExpression
                    temp = ImpExpression(pre.left, pre.right)
                    sequent_a.pres[temp] = old_sequent.pres[pre] + 1
                    temp = ImpExpression(pre.right, pre.left)
                    sequent_a.pres[temp] = old_sequent.pres[pre] + 1
                    conclusion.append(sequent_a)
                    break
            else:
                del sequent_a.cons[con]
                del sequent_b.cons[con]
                if isinstance(con, NotExpression):
                    sequent_a.pres[con.formula] = old_sequent.cons[con] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(con, AndExpression):
                    sequent_a.cons[con.left] = old_sequent.cons[con] + 1
                    sequent_b.cons[con.right] = old_sequent.cons[con] + 1
                    conclusion.append(sequent_a)
                    conclusion.append(sequent_b)
                    break
                elif isinstance(con, OrExpression):
                    sequent_a.cons[con.left] = old_sequent.cons[con] + 1
                    sequent_a.cons[con.right] = old_sequent.cons[con] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(con, ImpExpression):
                    # Rule CP
                    sequent_a.pres[con.left] = old_sequent.cons[con] + 1
                    sequent_a.cons[con.right] = old_sequent.cons[con] + 1
                    conclusion.append(sequent_a)
                    break
                elif isinstance(con, EquiExpression):
                    # transfer EquiExpression to ImpExpression
                    temp = ImpExpression(con.left, con.right)
                    sequent_a.cons[temp] = old_sequent.cons[con] + 1
                    temp = ImpExpression(con.right, con.left)
                    sequent_a.cons[temp] = old_sequent.cons[con] + 1
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
