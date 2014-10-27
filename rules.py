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
        pass

    def _disjunctive_syllogism(self):
        """
        !G, (G || H) => H
        """
        pass

    def _modus_ponens(self):
        """
        G, (G -> H) => H
        """
        pass

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
