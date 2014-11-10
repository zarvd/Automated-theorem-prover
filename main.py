import logging


facts = {}
atom_facts = {}
con_fact = None
result = []


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


def seek_pre(fact):
    while True:
        pass
    for index in range(len(result)):
        if fact is result[index]:
            # TODO
            break
    elif fact in facts:
        # TODO
        result.append({
            'fact': fact
            'value': fact.value,
            'rule': ''
            })
        pass
    elif fact.left_child not in facts:
        # TODO
        seek_pre(fact.left_child)
    elif fact.right_child not in facts:
        # TODO
        seek_pre(fact.right_child)


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
