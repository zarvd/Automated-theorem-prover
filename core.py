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
    results = None

    while True:
        results = search_node(con_fact['fact'], [con_fact['fact']], pre_facts, results)
        if not result:
            return False
        elif result[-1]['fact'] is con_fact['fact']:
            return result


def search_node(ser_node, nodes, facts, results):
    """ Search nodes that related to ser_node in DFS, and test the nodes then store the result, if the nodes pass the test, return results instead of False.

    :param ser_node: target node, a Fact instance
    :param nodes:    store nodes which are related, a list of Fact instances
    :param facts:    source, a list
    :param results:   current results, a list
    """
    if not ser_node:
        return False

    for c_fact in facts:
        if c_fact['fact'] in nodes:
            # avoid duplicated related nodes
            continue
        fact = c_fact['fact']
        fact_type = c_fact['type']  # type could be 'input' or 'result'
        # set temp variable
        facts_buffer = facts.copy()
        ser_node_buffer = ser_node
        nodes_buffer = nodes.copy()
        result_buffer = result

        if ser_node.value == fact.value:
            # G == G, -G == G
            pass
        elif ser_node.value in fact.value:
            # G, G*H
            nodes_buffer.append(fact)  # store current fact
            if ser_node.value in fact.left_child.value:
                ser_node_buffer = fact.right_child
            else:
                ser_node_buffer = fact.left_child
        elif fact.value in ser_node.value:
            # G*H, G
            pass

        if ser_node != ser_node_buffer:
            # nodes update, search next node
            result = search_node(ser_node_buffer, nodes_buffer, facts, results)
            if result:
                return result

    result = test_node(nodes, facts, results)
    if result:
        return result
    return False


def test_node(nodes, facts, result):
    # return nodes, facts, result
