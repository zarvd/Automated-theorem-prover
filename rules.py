OPERATERS = {
    'negation':    '-',
    'con':         '&',
    'dis':         '|',
    'implication': '->',
    'equivalence': '<->'
    }


class RulesForProposition(object):
    """
    Rules of inference for proposition
    """

    def __init__(self):
        pass

    def handler(self, premises, conclusion):
        status = False

        def return_status():
            if status is not False:
                return status

        if type(premises) == list:
            status = self._simplification(premises, conclusion)
            return_status()

            status = self._addition(premises, conclusion)
            return_status()

    def _simplification(self, premises, conclusion):
        """
        (G && H) => G
        """
        if len(premises) == 1:
            fact = premises[0]
            if fact.operater == '&':
                if fact.left_child == conclusion:
                    return 'I1'
                if fact.right_child == conclusion:
                    return 'I2'
        return False

    def _addition(self, premises, conclusion):
        """
        G => (G || H)
        """
        if len(premises) == 1:
            fact = premises[0]
            if conclusion.operater == '|':
                if conclusion.left_child == fact:
                    return 'I3'
                if conclusion.right_child == fact:
                    return 'I4'
        return False

    def _disjunctive_syllogism(self, premises, conclusion):
        """
        !G, (G || H) => H
        """
        if len(premises) == 2:
            if fact1.negative and not fact2.negative:
                fact1 = premises[0]
                fact2 = premises[1]
            elif not fact1.negative and fact2.negative:
                fact1 = premises[1]
                fact2 = premises[0]
            else:
                return False
            fact1_neg = fact1.negative()
            if fact1.negative and fact2.operater == '|':
                if ((fact2.left_child is fact1_neg and
                     conclusion is fact2.right_child) or
                     (fact2.right_child is fact1_neg and
                      conclusion is fact2.left_child)):
                    return 'I10'
        return False

    def _modus_ponens(self, premises, conclusion):
        """
        G, (G -> H) => H
        """
        if  len(premises) == 2:
            if fact1 is fact2.left_child:
                fact1 = premises[0]
                fact2 = premises[1]
            elif fact2 is fact1.left_child:
                fact1 = premises[1]
                fact2 = premises[0]
            else:
                return False
            if fact2.operater is OPERATERS.get('implication', default=None):
                if conclusion is fact2.right_child:
                    return 'I12'
        return False

    def _modus_tollens(self):
        """
        !H, (G -> H) => !G
        """
        pass

    def _hypothetical_syllogism(self):
        """
        (G -> H), (H -> I) => (G -> I)
        """
        pass

    def _dilemma(self):
        """
        (G || H), (G -> I), (H -> I) => I
        """
        pass


class RulesForPredicate(object):
    pass
