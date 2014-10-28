import logging


OPERATERS = {
    'negation':    '-',
    'con':         '&',
    'dis':         '|',
    'implication': '->',
    'equivalence': '<->'
    }
facts = {}
atom_facts = {}
con_fact = None


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
    negative = None  # TODO
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
            next_char = raw_str[index+1] if index + 1 < len(raw_str) else ''
            cur_and_next = current_char + next_char

            if self.left_child is None:
                if parenthesis == 0:
                    if current_char.isalpha():
                        self.left_child = get_atom_fact(current_char)
                    elif current_char == '-' and next_char.isalpha():
                        self.left_child = get_atom_fact(cur_and_next)
                    elif current_char == '(':
                        left_parent = index
                        parenthesis += 1
                elif current_char == ')' and parenthesis == 1:
                    char = raw_str[self.left_child+1:index]
                    self.left_child = get_atom_fact(char)
                    parenthesis -= 1
            elif self.operater is None:
                if current_char in OPERATERS:
                    self.operater = char
                elif cur_and_next in OPERATERS:
                    self.operater = char + current_char
            elif self.right_child is None:
                if parenthesis == 0:
                    if current_char.isalpha():
                        self.right_child = get_atom_fact(current_char)
                    elif current_char == '-' and next_char.isalpha():
                        self.right_child = get_atom_fact(cur_and_next)
                    elif current_char == '(':
                        left_parent = index
                        parenthesis += 1
                elif current_char == ')' and parenthesis == 1:
                    char = raw_str[self.left_child+1:index]
                    self.right_child = get_atom_fact(char)
                    parenthesis -= 1


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
            fact1 = premises[0]
            fact2 = premises[1]
            if fact1.negative and not fact2.negative:
                pass
            elif not fact1.negative and fact2.negative:
                fact1, fact2 = fact2, fact1
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
        if len(premises) == 2:
            fact1 = premises[0]
            fact2 = premises[1]
            if fact1 is fact2.left_child:
                pass
            elif fact2 is fact1.left_child:
                fact1, fact2 = fact2, fact1
            else:
                return False
            if fact2.operater is OPERATERS.get('implication', default=None):
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


class RulesForPredicate(object):
    pass


class Node(object):
    """
    Node of graph
    """
    entry = []

    def __init__(self):
        pass


class Deduction(object):
    def RuleP(self):
        pass

    def RuleT(self):
        pass

    def RuleCP(self):
        pass


def make_graph():
    pass


def make_road():
    pass


def test_road():
    pass


def premises_filter(premises_str):
    premises_str.replace(' ', '')
    premises_list = premises_str.split(',')
    for premise in premises_list:
        facts[premise] = Fact(premise)


def main():
    logging.info('Running...')
    premises_str = input("Please enter premises(seperate with ',')")
    premises_filter(premises_str)
    conclusion_str = input("Please enter conclusion")
    con_fact = Fact(conclusion_str)
    # TODO: input premises and conclusion
    # make graph
    # make road
    # test road

if __name__ == "__main__":
    main()
