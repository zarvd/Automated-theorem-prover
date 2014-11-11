import logging


facts = {}  # Premises
atom_facts = {}
con_fact = None  # Conclusion
result = []


def seek_pre(fact):
    # 如果结论存在于前提中
    if con_fact in facts:
        result.append({
            'fact': con_fact,
            'premises_id': [],
            'rule': rule.P
            })
        return
    while True:
        pass

def dfs():
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
