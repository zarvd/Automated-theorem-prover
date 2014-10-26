import logging
import re


OPERATERS = ['&', '|', '->']
facts = {}
atom_facts = {}


class AtomFact(object):
    """
    AtomFact
    """
    negative = None
    value = None

    def __init__(self, char):
        if len(char) == 1 and char.isalpha():
            self.value = char
            self.negative = False
        elif len(char) == 2 and char[0] == '-' and char[1].isalpha():
            self.value = char[1]
            self.negative = True


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
        def get_atom_fact(char):
            atom = atom_facts.get(char, default=None)
            if atom is None:
                atom = AtomFact(char) if len(char) <= 2 else Fact(char)
                atom_facts[char] = atom
            return atom

        parenthesis = 0
        left_parent = 0
        for index in range(raw_str):
            current_char = raw_str[index]
            next_char = raw_str[index+1] if index + 1 < len(raw_str) else None

            if self.left_child is None:
                if parenthesis == 0:
                    if current_char.isalpha():
                        self.left_child = get_atom_fact(current_char)
                    elif current_char == '-' and next_char.isalpha():
                        self.left_child = get_atom_fact(current_char + next_char)
                    elif current_char == '(':
                        left_parent = index
                        parenthesis += 1
                elif current_char == ')' and parenthesis == 1:
                    self.left_child = self.get_atom_fact(raw_str[left_child+1:index])
                    parenthesis -= 1
            elif self.operater is None:
                if current_char in OPERATERS:
                    self.operater = char
                elif current_char + next_char in OPERATERS:
                    self.operater = char + current_char
            elif self.right_child is None:
                if parenthesis == 0:
                    if current_char.isalpha():
                        self.right_child = get_atom_fact(current_char)
                    elif current_char == '-' and next_char.isalpha():
                        self.right_child = get_atom_fact(current_char + next_char)
                    elif current_char == '(':
                        left_parent = index
                        parenthesis += 1
                elif current_char == ')' and parenthesis == 1:
                    self.right_child = self.get_atom_fact(raw_str[left_child+1:index])
                    parenthesis -= 1


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
