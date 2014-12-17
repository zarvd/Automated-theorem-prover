import logging
import core


pre_facts = {}  # Premises
con_fact = None
atom_facts = {}

result = []


class MissingPremiseError(Exception):
    def __init__(self, info):
        self.info = info
    def __str__(self):
        return repr(self.info)


class MissingConclusionError(Exception):
    def __init__(self, info):
        self.info = info
    def __str__(self):
        return repr(self.info)


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
    atom = False
    negative = None
    operater = None
    left_child = None  # object Fact
    right_child = None  # object Fact or None when operator is None too
    value = None  # describe fact in human readable string 

    def __init__(self, raw_str):
        self.value = raw_str
        self.seperate_propsition(raw_str)

    def seperate_propsition(self, raw_str):
        def get_atom_fact(char):
            atom = atom_facts.get(char, None)
            if not atom:
                atom = Fact(char)
                atom_facts[char] = atom
            return atom

        if len(raw_str) == 1 and raw_str.isalpha():
            # Ex: raw_str = "G"
            self.value = raw_str
            self.atom = True
            self.negative = False
            return
        elif len(raw_str) == 2 and raw_str[0] == Operator.negative and raw_str[1].isalpha():
            # Ex: raw_str = "-G"
            self.atom = True
            self.value = raw_str[1]
            self.negative = True
            return

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


def is_negative(this_fact, that_fact):
    if this_fact.value == that_fact.value and this_fact.negative != that_fact.negative:
        return True
    else:
        return False        


class ERules(object):
    """Equivalence relation of proposition
    """

    def __init__(self):
      pass  


class IRules(object):
    """
    Rules of inference for proposition
    """

    def __init__(self):
        pass

    def handler(self, premises, conclusion):
        if type(premises) == list:
            status = self._disjunctive_syllogism(premises, conclusion)
            if status:
                return status
            status = self._simplification(premises, conclusion)
            if status:
                return status
            status = self._addition(premises, conclusion)
            if status:
                return status

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
            if not (is_negative(fact1, fact2.left_child)
                 or is_negative(fact1, fact2.right_child)):
                return False
            elif (fact2.operater is Operator().dis
                  and (fact2.left_child is conclusion
                       or fact2.right_child is conclusion)):
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


def new_fact(raw_str):
    for char in raw_str:
        if char.isalpha() and not atom_facts.get(char, None):
            atom_facts[char] = Fact(char)
            char_neg = '-'+char
            atom_facts[char_neg] = Fact(char_neg)
    fact = atom_facts.get(raw_str, None)
    return Fact(raw_str) if not fact else fact


def read_line():
    """ Input premises and conclusion
    """
    print("Please enter the premises(seperate with multi line, finish in a new line with nothing)")
    order = 1

    global pre_facts
    global con_fact

    while not con_fact:
        in_buffer = input("%02d: " % order)
        in_buffer = in_buffer.replace(' ', '')  # remove whitespace
        if in_buffer:
            pre_facts[in_buffer] = new_fact(in_buffer)
            order += 1
        else:
            print("Please enter the conclusion (Note: it should be only one line)")
            in_buffer = input('conclusion: ')
            con_fact = {
                'string': in_buffer,
                'fact': new_fact(in_buffer)
                }

    if not pre_facts:
        raise MissingPremiseError("you did not enter any premises")
    if not con_fact:
        raise MissingConclusionError("you did not enter any conclusion")


def main():
    logging.info('Running...')
    global pre_facts
    global con_fact
    read_line()
    _IRules = IRules()

    result = core.dfs(pre_facts, con_fact, _IRules)
    if result:
        count = 1
        for step in result:
            print("[%02d] %-15s %s" % (count, step['fact'].value, step['rule']))
            count += 1
    else:
        print("No result!")
    # print('\nRESULT:\n')
    # for key in range(len(result)):
    #     print("[%02d] %-15s %s\n" % (key+1, result[key]['fact'], result[key]['rule']))


if __name__ == "__main__":
    main()
