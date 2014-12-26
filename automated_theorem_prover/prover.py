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

    def _premises(self):
        return ', '.join([str(premise) for premise in self.pres])

    def _conclusion(self):
        return ', '.join([str(conclusion) for conclusion in self.cons])

    def __str__(self):
        return self._premises() + ' => ' + self._conclusion()

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
        bcolors.print_ok('[%d] %s' % (sequent.depth, sequent))

    def prove(self):
        """BFS
        :rtype: bool
        """
        while True:
            cur_sequent = None
            while (self.conclusion and
                   (not cur_sequent or cur_sequent in self.premises)):
                cur_sequent = self.conclusion.pop(0)
            if not cur_sequent:
                return True
            self._output_sequent(cur_sequent)
            if set(cur_sequent.pres.keys()) & set(cur_sequent.cons.keys()):
                """current sequent's premises and conclusions overlap,
                then go on next sequent""" 
                self.premises.add(cur_sequent)
                continue

            while True:
                pre = None
                pre_depth = None
                for expression, depth in cur_sequent.pres.items():
                    if not pre_depth or pre_depth > depth:
                        if not isinstance(expression, AtomExpression):
                            pre = expression
                            pre_depth = depth
                con = None
                con_depth = None
                for expression, depth in cur_sequent.cons.items():
                    if not con_depth or con_depth > depth:
                        if not isinstance(expression, AtomExpression):
                            con = expression
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
                    """current sequent's premises and conclusions don't overlap
                    and they are all AtomExpression, then it could not be proven"""
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
                        # (not G => ) to ( => G)
                        sequent_a.cons[pre.expression] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(pre, AndExpression):
                        # (A and B => ) to (A, B =>)
                        sequent_a.pres[pre.left] = cur_sequent.pres[pre] + 1
                        sequent_a.pres[pre.right] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(pre, OrExpression):
                        # (A or B => ) to (A => ) and (B => )
                        sequent_a.pres[pre.left] = cur_sequent.pres[pre] + 1
                        sequent_b.pres[pre.right] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        self.conclusion.append(sequent_b)
                        break
                    elif isinstance(pre, ImpExpression):
                        # transfer ImpExpression to OrExpression
                        # (A -> B => ) to ((not A) => ) and (B => )
                        temp = NotExpression(pre.left)
                        sequent_a.pres[temp] = cur_sequent.pres[pre] + 1
                        sequent_b.pres[pre.right] = cur_sequent.pres[pre] + 1
                        self.conclusion.append(sequent_a)
                        self.conclusion.append(sequent_b)
                        break
                    elif isinstance(pre, EquiExpression):
                        # transfer EquiExpression to ImpExpression
                        # (A <-> B => ) to (A -> B, B->A => )
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
                        # ( => not A) to (A => )
                        sequent_a.pres[con.expression] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(con, AndExpression):
                        # ( => A and B) to ( => A) and ( => B)
                        sequent_a.cons[con.left] = cur_sequent.cons[con] + 1
                        sequent_b.cons[con.right] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        self.conclusion.append(sequent_b)
                        break
                    elif isinstance(con, OrExpression):
                        # ( => A or B) to ( => A, B)
                        sequent_a.cons[con.left] = cur_sequent.cons[con] + 1
                        sequent_a.cons[con.right] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(con, ImpExpression):
                        # Rule CP: Conditional proof
                        # ( => A -> B) to (A => B)
                        sequent_a.pres[con.left] = cur_sequent.cons[con] + 1
                        sequent_a.cons[con.right] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
                    elif isinstance(con, EquiExpression):
                        # transfer EquiExpression to ImpExpression
                        # ( => A <-> B) to ( => A -> B, B -> A)
                        temp = ImpExpression(con.left, con.right)
                        sequent_a.cons[temp] = cur_sequent.cons[con] + 1
                        temp = ImpExpression(con.right, con.left)
                        sequent_a.cons[temp] = cur_sequent.cons[con] + 1
                        self.conclusion.append(sequent_a)
                        break
