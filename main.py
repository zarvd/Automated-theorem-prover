import logging
import re


class Fact(object):
    """
    Fact
    """
    left_child = None
    right_child = None

    def __init__(self, raw_str):
        # TODO: seperate compound proposition
        pass


class Node(object):
    """
    Node of graph
    """
    entry = []

    def __init__(self):
        pass


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


class Deduction(object):
    def RuleP(object):
        pass

    def RuleT(object):
        pass

    def RuleCP(object):
        pass


def make_graph():
    pass

def make_road():
    pass

def test_road():
    pass

def main():
    logging.info('Running...')
    premises = raw_input("Please enter predicates(seperate with ',')")
    premises = premises.split(',')
    # TODO: input premises and conclusion
    # instantinate Face object
    # make graph
    # make road
    # test road

if __name__ == "__main__":
    main()
