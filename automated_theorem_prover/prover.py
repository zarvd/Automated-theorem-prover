from render import bcolors
from expression import (AtomExpression, NotExpression,
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

    def premises(self):
        return ', '.join([str(premise) for premise in self.pres])

    def conclusion(self):
        return ', '.join([str(conclusion) for conclusion in self.cons])

    def __str__(self):
        return self.premises() + ' => ' + self.conclusion()

    def __hash__(self):
        return hash(str(self))


class Prover(object):
    def __init__(self, premises, conclusion):
        sequent = Sequent(
            {premise: 0 for premise in premises},
            {conclusion: 0},
            0) 
        self.premises = {sequent}
        self.conclusion = [sequent]

    def _output_sequent(self, sequent):
            bcolors.print_ok('[%d] %-30s => %-30s' % (sequent.depth, sequent.premises(), sequent.conclusion()))

    def prove(self):
        while True:
            cur_sequent = None
            while self.conclusion and (not cur_sequent or cur_sequent in self.premises):
                cur_sequent = self.conclusion.pop(0)
            if not cur_sequent:
                break
            self._output_sequent(cur_sequent)
            if len(set(cur_sequent.pres.keys()) & set(cur_sequent.cons.keys())):
                self.premises.add(cur_sequent)
                continue

            while True:
                pre = None
                pre_depth = None
                for formula, depth in cur_sequent.pres.items():
                    if not pre_depth or pre_depth > depth:
                        if not isinstance(formula, AtomExpression):
                            pre = formula
                            pre_depth = depth
                con = None
                con_depth = None
                for formula, depth in cur_sequent.cons.items():
                    if not con_depth or con_depth > depth:
                        if not isinstance(formula, AtomExpression):
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
                    cur_sequent.pres.copy(),
                    cur_sequent.cons.copy(),
                    cur_sequent.depth + 1
                )
                sequent_b = Sequent(
                    cur_sequent.pres.copy(),
                    cur_sequent.cons.copy(),
                    cur_sequent.depth + 1
                )
                if apply_pre:
                    del sequent_a.pres[pre]
                    del sequent_b.pres[pre]

                    if isinstance(pre, NotExpression):
                        sequent_a.cons[pre.formula] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(pre, AndExpression):
                        sequent_a.pres[pre.left] = cur_sequent.pres[pre] + 1
                        sequent_a.pres[pre.right] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(pre, OrExpression):
                        sequent_a.pres[pre.left] = cur_sequent.pres[pre] + 1
                        sequent_b.pres[pre.right] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        self.conclusion.append(sequent_b)
                        break
                    elif isinstance(pre, ImpExpression):
                        # transfer ImpExpression to OrExpression
                        sequent_a.pres[NotExpression(pre.left)] = cur_sequent.pres[pre] + 1
                        sequent_b.pres[pre.right] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        self.conclusion.append(sequent_b)
                        break
                    elif isinstance(pre, EquiExpression):
                        # transfer EquiExpression to ImpExpression
                        temp = ImpExpression(pre.left, pre.right)
                        sequent_a.pres[temp] = cur_sequent.pres[pre] + 1
                        temp = ImpExpression(pre.right, pre.left)
                        sequent_a.pres[temp] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        break
                else:
                    del sequent_a.cons[con]
                    del sequent_b.cons[con]
                    if isinstance(con, NotExpression):
                        sequent_a.pres[con.formula] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(con, AndExpression):
                        sequent_a.cons[con.left] = cur_sequent.cons[con] + 1
                        sequent_b.cons[con.right] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        self.conclusion.append(sequent_b)
                        break
                    elif isinstance(con, OrExpression):
                        sequent_a.cons[con.left] = cur_sequent.cons[con] + 1
                        sequent_a.cons[con.right] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(con, ImpExpression):
                        # Rule CP: Conditional proof
                        sequent_a.pres[con.left] = cur_sequent.cons[con] + 1
                        sequent_a.cons[con.right] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(con, EquiExpression):
                        # transfer EquiExpression to ImpExpression
                        temp = ImpExpression(con.left, con.right)
                        sequent_a.cons[temp] = cur_sequent.cons[con] + 1
                        temp = ImpExpression(con.right, con.left)
                        sequent_a.cons[temp] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
        return True
