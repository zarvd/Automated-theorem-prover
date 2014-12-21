import pdb

con_fact = None
IRules = None


def dfs(_pre_facts, _con_fact, _IRules):
    # TODO seperate con_fact, Eg: H => G|H or worse
    global con_fact
    global IRules
    pre_facts = _pre_facts
    con_fact = _con_fact
    IRules = _IRules

    ser_node = con_fact['fact']
    nodes = [ser_node]
    facts = pre_facts
    results = []
    while True:
        results_temp = results.copy()
        ser_node, nodes, facts, results = search_node(ser_node, nodes, facts, results)
        if not results or results_temp == results:
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
        return ser_node, nodes, facts, results

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
            s, n, f, r = search_node(ser_node_buffer, nodes_buffer, facts_buffer, results)
            if r != results:
                return s, n, f, r

    return test_node(nodes, facts, results)


def test_node(nodes, facts, result):
    # return ser_node, nodes, facts, result
    pass
