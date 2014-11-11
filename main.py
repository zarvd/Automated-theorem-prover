import logging


facts = {}
atom_facts = {}
con_fact = None
result = []


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
