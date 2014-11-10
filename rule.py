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
            if fact.operater is OPERATERS['con']:
                if fact.left_child is conclusion:
                    return 'I1'
                if fact.right_child is conclusion:
                    return 'I2'
        return False

    def _addition(self, premises, conclusion):
        """
        G => (G || H)
        """
        if len(premises) == 1:
            fact = premises[0]
            if conclusion.operater is OPERATERS['dis']:
                if conclusion.left_child is fact:
                    return 'I3'
                if conclusion.right_child is fact:
                    return 'I4'
        return False

    def _disjunctive_syllogism(self, premises, conclusion):
        """
        !G, (G || H) => H
        """
        if len(premises) == 2:
            fact1 = premises[0]
            fact2 = premises[1]
            if fact1.negative and not fact2.negative:
                pass
            elif not fact1.negative and fact2.negative:
                fact1, fact2 = fact2, fact1
            else:
                return False
            fact1_neg = fact1.negative()
            if fact1.negative and fact2.operater is OPERATERS['dis']:
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
        if len(premises) == 2:
            fact1 = premises[0]
            fact2 = premises[1]
            if fact1 is fact2.left_child:
                pass
            elif fact2 is fact1.left_child:
                fact1, fact2 = fact2, fact1
            else:
                return False
            if fact2.operater is OPERATERS['implication']:
                if conclusion is fact2.right_child:
                    return 'I12'
        return False

    def _modus_tollens(self, premises, conclusion):
        """
        !H, (G -> H) => !G
        """
        if len(premises) == 2:
            fact1 = premises[0]
            fact2 = premises[1]
            if fact1.negative and not fact2.negative:
                pass
            elif not fact1.negative and fact2.negative:
                fact1, fact2 = fact2, fact1
            else:
                return False
            fact1_neg = fact1.negative()
            con_neg = conclusion.negative()
            if fact1_neg is fact2.right_child and fact2.left_child is con_neg:
                return 'I13'
        return False

    def _hypothetical_syllogism(self, premises, conclusion):
        """
        (G -> H), (H -> I) => (G -> I)
        """
        if len(premises) == 2:
            fact1 = premises[0]
            fact2 = premises[1]
            fact1_left = fact1.left_child
            fact1_right = fact1.right_child
            fact2_left = fact2.left_child
            fact2_right = fact2.right_child
            if fact1_right is fact2_left and fact2_right is conclusion:
                return 'I14'
            elif fact2_right is fact1_left and fact1_right is conclusion:
                return 'I14'
        return False

    def _dilemma(self, premises, conclusion):
        """
        (G || H), (G -> I), (H -> I) => I
        """
        if len(premises) == 3:
            fact1 = None
            fact2 = None
            fact3 = None
            for fact in premises:
                if fact.operater is OPERATERS['dis'] and not fact1:
                    fact1 = fact
                elif fact.operater is OPERATERS['implication']:
                    if not fact2:
                        fact2 = fact
                    elif not fact3:
                        fact3 = fact
                    else:
                        return False
            fact1_left = fact1.left_child
            fact1_right = fact1.right_child
            fact2_left = fact2.left_child
            fact2_right = fact2.right_child
            fact3_left = fact3.left_child
            fact3_right = fact3.right_child
            if fact2_right is fact3_right is conclusion.right_child:
                if fact1_left is fact2_left and fact1_right is fact3_left:
                    return 'I15'
                elif fact1_left is fact3_left and fact1_right is fact3_right:
                    return 'I15'
        return False
