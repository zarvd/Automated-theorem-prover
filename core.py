import pdb

pre_facts = None
temp_facts = []
con_fact = None
IRules = None

def dfs(_pre_facts, _con_fact, _IRules):
    # TODO seperate con_fact, Eg: H => G|H or worse
    global pre_facts
    global con_fact
    global IRules
    pre_facts = _pre_facts
    con_fact = _con_fact
    IRules = _IRules
    ser_node = con_fact['fact']
    nodes = [con_fact['fact']]
    facts = pre_facts
    result = search_node(ser_node, nodes, facts, [])
    return result


def search_node(ser_node, nodes, facts, results):
    """ Search nodes that related to ser_node in DFS, and test the nodes then store the result, if the nodes pass the test, return results instead of False.

    :param ser_node: target node, a Fact instance
    :param nodes:    store nodes which are related, a list of Fact instances
    :param facts:    source, a dict of Fact instances
    :param result:   current result, a dict
    """
    if not ser_node:
        return False

    # set temp variable
    facts_buffer = facts.copy()
    ser_node_buffer = ser_node
    nodes_buffer = nodes.copy()
    result_buffer = result

    for fact in facts:
        if ser_node.value == fact.value:
            # G == G, -G == G
            pass
            
            

def test_node(nodes, facts, result):
    # return nodes, facts, result
