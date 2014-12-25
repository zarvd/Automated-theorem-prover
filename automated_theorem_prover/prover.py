from Expression import (Proposition, NotExpression,
                        AndExpression, OrExpression,
                        ImpExpression)


class Sequent:
    def __init__(self, left, right, siblings, depth):
        self.left = left
        self.right = right
        self.siblings = siblings
        self.depth = depth

    def getUnifiablePairs(self):
        pairs = []
        for formula_left in self.left:
            for formula_right in self.right:
                if unify(formula_left, formula_right) is not None:
                    pairs.append((formula_left, formula_right))
        return pairs

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
    # returns True if the sequent is provable
    # returns False or loops forever if the sequent is not provable
    # reset the time for each formula in the sequent
    for formula in sequent.left:
        formula.setInstantiationTime(0)
    for formula in sequent.right:
        formula.setInstantiationTime(0)

    # sequents to be proven
    frontier = [sequent]

    # sequents which have been proven
    proven = { sequent }

    while True:
        # get the next sequent
        old_sequent = None
        while len(frontier) > 0 and (old_sequent is None or old_sequent in proven):
            old_sequent = frontier.pop(0)
        if old_sequent is None:
            break
        print('%s. %s' % (old_sequent.depth, old_sequent))

        # check if this sequent is axiomatically true without unification
        if len(set(old_sequent.left.keys()) & set(old_sequent.right.keys())) > 0:
            proven.add(old_sequent)
            continue

        # check if this sequent has unification terms
        if old_sequent.siblings is not None:
            # get the unifiable pairs for each sibling
            sibling_pair_lists = [sequent.getUnifiablePairs()
                for sequent in old_sequent.siblings]

            # check if there is a unifiable pair for each sibling
            if all([len(pair_list) > 0 for pair_list in sibling_pair_lists]):
                # iterate through all simultaneous choices of pairs from each sibling
                substitution = None
                index = [0] * len(sibling_pair_lists)
                while True:
                    # attempt to unify at the index
                    substitution = unify_list([sibling_pair_lists[i][index[i]]
                        for i in range(len(sibling_pair_lists))])
                    if substitution is not None:
                        break

                    # increment the index
                    pos = len(sibling_pair_lists) - 1
                    while pos >= 0:
                        index[pos] += 1
                        if index[pos] < len(sibling_pair_lists[pos]):
                            break
                        index[pos] = 0
                        pos -= 1
                    if pos < 0:
                        break
                if substitution is not None:
                    for k, v in substitution.items():
                        print('    %s = %s' % (k, v))
                    proven |= old_sequent.siblings
                    frontier = [sequent for sequent in frontier
                        if sequent not in old_sequent.siblings]
                    continue
            else:
                # unlink this sequent
                old_sequent.siblings.remove(old_sequent)

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
            if left_formula is not None and right_formula is None:
                apply_left = True
            if left_formula is None and right_formula is not None:
                apply_right = True
            if left_formula is not None and right_formula is not None:
                if left_depth < right_depth:
                    apply_left = True
                else:
                    apply_right = True
            if left_formula is None and right_formula is None:
                return False

            # apply a left rule
            if apply_left:
                if isinstance(left_formula, NotExpression):
                    new_sequent = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent.left[left_formula]
                    new_sequent.right[left_formula.formula] = \
                    old_sequent.left[left_formula] + 1
                    if new_sequent.siblings is not None:
                        new_sequent.siblings.add(new_sequent)
                    frontier.append(new_sequent)
                    break
                if isinstance(left_formula, AndExpression):
                    new_sequent = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent.left[left_formula]
                    new_sequent.left[left_formula.formula_a] = \
                        old_sequent.left[left_formula] + 1
                    new_sequent.left[left_formula.formula_b] = \
                    old_sequent.left[left_formula] + 1
                    if new_sequent.siblings is not None:
                        new_sequent.siblings.add(new_sequent)
                    frontier.append(new_sequent)
                    break
                if isinstance(left_formula, OrExpression):
                    new_sequent_a = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    new_sequent_b = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent_a.left[left_formula]
                    del new_sequent_b.left[left_formula]
                    new_sequent_a.left[left_formula.formula_a] = \
                        old_sequent.left[left_formula] + 1
                    new_sequent_b.left[left_formula.formula_b] = \
                    old_sequent.left[left_formula] + 1
                    if new_sequent_a.siblings is not None:
                        new_sequent_a.siblings.add(new_sequent_a)
                    frontier.append(new_sequent_a)
                    if new_sequent_b.siblings is not None:
                        new_sequent_b.siblings.add(new_sequent_b)
                    frontier.append(new_sequent_b)
                    break
                if isinstance(left_formula, ImpExpression):
                    new_sequent_a = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    new_sequent_b = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent_a.left[left_formula]
                    del new_sequent_b.left[left_formula]
                    new_sequent_a.right[left_formula.formula_a] = \
                        old_sequent.left[left_formula] + 1
                    new_sequent_b.left[left_formula.formula_b] = \
                    old_sequent.left[left_formula] + 1
                    if new_sequent_a.siblings is not None:
                        new_sequent_a.siblings.add(new_sequent_a)
                    frontier.append(new_sequent_a)
                    if new_sequent_b.siblings is not None:
                        new_sequent_b.siblings.add(new_sequent_b)
                    frontier.append(new_sequent_b)
                    break

            # apply a right rule
            if apply_right:
                if isinstance(right_formula, NotExpression):
                    new_sequent = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent.right[right_formula]
                    new_sequent.left[right_formula.formula] = \
                    old_sequent.right[right_formula] + 1
                    if new_sequent.siblings is not None:
                        new_sequent.siblings.add(new_sequent)
                    frontier.append(new_sequent)
                    break
                if isinstance(right_formula, AndExpression):
                    new_sequent_a = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    new_sequent_b = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent_a.right[right_formula]
                    del new_sequent_b.right[right_formula]
                    new_sequent_a.right[right_formula.formula_a] = \
                        old_sequent.right[right_formula] + 1
                    new_sequent_b.right[right_formula.formula_b] = \
                    old_sequent.right[right_formula] + 1
                    if new_sequent_a.siblings is not None:
                        new_sequent_a.siblings.add(new_sequent_a)
                    frontier.append(new_sequent_a)
                    if new_sequent_b.siblings is not None:
                        new_sequent_b.siblings.add(new_sequent_b)
                    frontier.append(new_sequent_b)
                    break
                if isinstance(right_formula, OrExpression):
                    new_sequent = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent.right[right_formula]
                    new_sequent.right[right_formula.formula_a] = \
                        old_sequent.right[right_formula] + 1
                    new_sequent.right[right_formula.formula_b] = \
                        old_sequent.right[right_formula] + 1
                    if new_sequent.siblings is not None:
                        new_sequent.siblings.add(new_sequent)
                    frontier.append(new_sequent)
                    break
                if isinstance(right_formula, ImpExpression):
                    new_sequent = Sequent(
                        old_sequent.left.copy(),
                        old_sequent.right.copy(),
                        old_sequent.siblings,
                        old_sequent.depth + 1
                    )
                    del new_sequent.right[right_formula]
                    new_sequent.left[right_formula.formula_a] = \
                        old_sequent.right[right_formula] + 1
                    new_sequent.right[right_formula.formula_b] = \
                        old_sequent.right[right_formula] + 1
                    if new_sequent.siblings is not None:
                        new_sequent.siblings.add(new_sequent)
                    frontier.append(new_sequent)
                    break

    # no more sequents to prove
    return True


def proveFormula(premises, conclusion):
    # returns True if the formula is provable
    # returns False or loops forever if the formula is not provable
    return proveSequent(Sequent(
        { premise: 0 for premise in premises },
        { conclusion: 0 },
        None,
        0
    ))
