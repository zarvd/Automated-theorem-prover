class RulesForProposition(object):
    """
    Rules of inference for proposition
    """
    
    def __init__(self):
        pass

    def simplification(self):
        """
        (G && H) => G
        """
        pass

    def addition(self):
        """
        G => (G || H)
        """
        pass

    def disjunctive_syllogism(self):
        """
        !G, (G || H) => H
        """
        pass

    def modus_ponens(self):
        """
        G, (G -> H) => H
        """
        pass

    def modus_tollens(self):
        """
        !H, (G -> H) => !G
        """
        pass

    def hypothetical_syllogism(self):
        """
        (G -> H), (H -> I) => (G -> I)
        """
        pass

    def dilemma(self):
        """
        (G || H), (G -> I), (H -> I) => I
        """
        pass


class RulesForPredicate(object):
    pass
