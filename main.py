import logging


facts = {}  # Premises
atom_facts = {}
con_fact = None  # Conclusion
result = []


class Operator(object):
    negative    = '-'
    con         = '&'
    dis         = '|'
    implication = '->'
    equivalence = '<->'

    @staticmethod
    def equal(this, that):
        if this is that:
            return True
        else:
            return False

    @staticmethod
    def items():
        return [Operator.negative,
                Operator.con,
                Operator.dis,
                Operator.implication,
                Operator.equivalence
                ]


class Fact(object):
    """
    Fact
    """
    negative = None
    left_child = None
    operater = None
    right_child = None
    value = None

    def __init__(self, raw_str):
        self.value = raw_str
        self.seperate_propsition(raw_str)

    def seperate_propsition(self, raw_str):
        def get_atom_fact(char):
            atom = atom_facts.get(char, None)
            if atom is None:
                atom = Fact(char)
                atom_facts[char] = atom
            return atom

        if len(raw_str) == 1 and raw_str.isalpha():
            # Ex: raw_str = "G"
            self.value = char
            self.negative = False
        elif len(raw_str) == 2 and raw_str[0] == Operator.negative and raw_str[1].isalpha():
            # Ex: raw_str = "-G"
            self.value = char[1]
            self.negative = True

        parenthesis = 0
        left_parent = 0
        for index in range(len(raw_str)):
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
                    char = raw_str[left_parent+1:index]
                    self.left_child = get_atom_fact(char)
                    parenthesis -= 1
            elif self.operater is None:
                # TODO: '<->' operater
                for op in Operator.items():
                    if current_char == op or cur_and_next == op:
                        self.operater = op
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
                    char = raw_str[left_parent+1:index]
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


def main():
    logging.info('Running...')
    premises_str = input("Please enter premises(seperate with ','):\n")
    premises_filter(premises_str)
    conclusion_str = input("Please enter conclusion:\n")
    con_fact = Fact(conclusion_str)  # Conclusion
    # make_graph()
    # TODO: input premises and conclusion
    # make graph
    # make road
    # test road

if __name__ == "__main__":
    main()
