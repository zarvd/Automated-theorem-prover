from render import bcolors
from expression import (Proposition, NotExpression,
                        AndExpression, OrExpression,
                        ImpExpression)


class Result:
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


def proveResult(result):
    conclusion = [result]

    premises = {result}

    while True:
        # get the next result
        old_result = None
        while conclusion and (not old_result or old_result in premises):
            old_result = conclusion.pop(0)
        if not old_result:
            break
        bcolors.print_ok('[%s] %s' % (old_result.depth, old_result))

        # check if this result is axiomatically true without unification
        if len(set(old_result.pre.keys()) & set(old_result.con.keys())):
            premises.add(old_result)
            continue

        while True:
            # determine which formula to expand
            left_formula = None
            left_depth = None
            for formula, depth in old_result.pre.items():
                if not left_depth or left_depth > depth:
                    if not isinstance(formula, Proposition):
                        left_formula = formula
                        left_depth = depth
            right_formula = None
            right_depth = None
            for formula, depth in old_result.con.items():
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

            result_a = Result(
                old_result.pre.copy(),
                old_result.con.copy(),
                old_result.depth + 1
            )
            result_b = Result(
                old_result.pre.copy(),
                old_result.con.copy(),
                old_result.depth + 1
            )
            # apply a left rule
            if apply_left:
                del result_a.pre[left_formula]
                del result_b.pre[left_formula]

                if isinstance(left_formula, NotExpression):
                    result_a.con[left_formula.formula] = \
                        old_result.pre[left_formula] + 1
                    conclusion.append(result_a)
                    break
                elif isinstance(left_formula, AndExpression):
                    result_a.pre[left_formula.left] = \
                        old_result.pre[left_formula] + 1
                    result_a.pre[left_formula.right] = \
                        old_result.pre[left_formula] + 1
                    conclusion.append(result_a)
                    break
                elif isinstance(left_formula, OrExpression):
                    result_a.pre[left_formula.left] = \
                        old_result.pre[left_formula] + 1
                    result_b.pre[left_formula.right] = \
                        old_result.pre[left_formula] + 1
                    conclusion.append(result_a)
                    conclusion.append(result_b)
                    break
                elif isinstance(left_formula, ImpExpression):
                    result_a.con[left_formula.left] = \
                        old_result.pre[left_formula] + 1
                    result_b.pre[left_formula.right] = \
                        old_result.pre[left_formula] + 1
                    conclusion.append(result_a)
                    conclusion.append(result_b)
                    break

            # apply a right rule
            elif apply_right:
                del result_a.con[right_formula]
                del result_b.con[right_formula]
                if isinstance(right_formula, NotExpression):
                    result_a.pre[right_formula.formula] = \
                        old_result.con[right_formula] + 1
                    conclusion.append(result_a)
                    break
                elif isinstance(right_formula, AndExpression):
                    result_a.con[right_formula.left] = \
                        old_result.con[right_formula] + 1
                    result_b.con[right_formula.right] = \
                        old_result.con[right_formula] + 1
                    conclusion.append(result_a)
                    conclusion.append(result_b)
                    break
                elif isinstance(right_formula, OrExpression):
                    result_a.con[right_formula.left] = \
                        old_result.con[right_formula] + 1
                    result_a.con[right_formula.right] = \
                        old_result.con[right_formula] + 1
                    conclusion.append(result_a)
                    break
                elif isinstance(right_formula, ImpExpression):
                    result_a.pre[right_formula.left] = \
                        old_result.con[right_formula] + 1
                    result_a.con[right_formula.right] = \
                        old_result.con[right_formula] + 1
                    conclusion.append(result_a)
                    break
    return True


def proveFormula(premises, conclusion):
    """
    :return bool: true if it's provable
    """
    return proveResult(Result(
        {premise: 0 for premise in premises},
        {conclusion: 0},
        0
    ))
