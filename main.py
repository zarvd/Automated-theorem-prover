import logging
import re


class Fact(object):
    """
    Fact
    """
    left_child = None
    operater = None
    right_child = None

    def __init__(self, raw_str):
        # TODO: seperate compound proposition
        
        pass

    def seperate_propsition(self, raw_str):
        if len(raw_str) <= 2 and raw_str[0] == '-' and raw_str[1].isalpha():
            self.left_child = raw_str[0]
            return
        
        parenthesis = 0
        if raw_str[0].isalpha():
            self.left_child = Fact(raw_str[0])
        elif raw_str[0] == '(':
            parenthesis += 1

        for i in range(len(raw_str)):
            if raw_str[i].isalpha():
                if i > 0 and raw_str[i-1] == '-':
                    self.left_child = Fact(raw_str[0])
                else
                pass


class Node(object):
    """
    Node of graph
    """
    entry = []

    def __init__(self):
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
    premises_str = raw_input("Please enter predicates(seperate with ',')")
    premises_list = premises.split(',')
    premises = []
    for premise in premise_list:
        premises.append(Fact(premise))
    # TODO: input premises and conclusion
    # instantinate Face object
    # make graph
    # make road
    # test road

if __name__ == "__main__":
    main()
