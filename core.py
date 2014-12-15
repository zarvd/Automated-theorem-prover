def search_node(ser_node, nodes, facts, result):
    for fact in facts.values():
        if not ser_node:
            break
        nodes_buffer = nodes
        ser_node_buffer = ser_node
        facts_buffer = facts
        if fact.atom:
            if fact.value == ser_node.value:
                # -G, G or G, G
                nodes_buffer.append(fact)
                ser_node_buffer = None
                del facts_buffer[fact.value]
        else:
            if fact.right_child.value == ser_node.value:
                # H*G, G or H*(-G), G
                nodes_buffer.append(fact)
                ser_node_buffer = fact.left_child
                del facts_buffer[fact.value]
            elif fact.left_child.value == ser_node.value:
                # G*H, G or (-G)*H, G
                nodes_buffer.append(fact)
                ser_node_buffer = fact.right_child
                del facts_buffer[fact.value]
            elif ser_node.value in fact.value:
                # FIXME Both situation may turn up at the same time
                # (H*R)*(G*R), R
                if ser_node.value in fact.left_child.value:
                    # (H*R)*G, R
                    nodes_buffer.append(fact)
                    ser_node_buffer = fact.right_child
                    del facts_buffer[fact.value]
                elif ser_node.value in fact.right_child.value:
                    # G*(H*R), R
                    nodes_buffer.append(fact)
                    ser_node_buffer = fact.left_child
                    del facts_buffer[fact.value]
        if ser_node != ser_node_buffer:
            result_buffer = search_node(ser_node_buffer, nodes_buffer, facts_buffer, result)
            if result_buffer:
                return result_buffer
            else:
                continue

    result_temp = result
    nodes, facts, result = test_node(nodes, facts, result)
    if result_temp is result:
        return False
    ser_node = nodes[-1].left_child
    result_buffer = search_node(ser_node, nodes, facts, result)
    if result_buffer:
        return result_buffer
    ser_node = nodes[-1].right_child
    if ser_node:
        result_buffer = search_node(ser_node, nodes, facts, result)
        if result_buffer:
            return result_buffer
    return False
        
        

def test_node(nodes, facts, result)
    result_buffer = result
    facts_buffer = facts
    nodes_buffer = nodes
    nodes_buffer.reverse()
    while True:
        nodes_temp = nodes_buffer

        if len(nodes_buffer) >= 2:
            cur_node = nodes_buffer[0]
            next_node = nodes_buffer[1]
            # 1 premise
            if cur_node is next_node:
                # G, G
                if cur_node is con_fact:
                    result_buffer.append({
                        'fact': cur_node,
                        'rule': 'P'
                        })
                    return result_buffer
                else:
                    return False
            # 2 premises
            pre = [cur_node, next_node]
            con = None
            if cur_node.atom:
                if cur_node.value == next_node.left_child.value:
                    # G, G*H or -G, G*H
                    con = next_node.right_child
                elif cur_node.value == next_node.right_child.value:
                    # G, H*G or -G, H*G
                    con = next_node.left_child
            else:
                if cur_node.right_child.value == next_node.left_child.value:
                    # I14: G->H, H->I => G->I
                    con = Fact(cur_node.left_child.value + '->' + next_node.right_child.value)
                elif cur_node.left_child.value == next_node.right_child.value:
                    con = Fact(next_node.left_child.value + '->' + cur_node.right_child.value)
            if con:
                rule = IRules().handler(pre, con)
                if rule:
                    result_buffer.append({
                        'fact': con,
                        'rule': rule
                        })
                    for item in pre:
                        nodes_buffer.remove(item)
                    facts_buffer.append(con)  # new fact
                    nodes_buffer.append(con)  # new node
                    continue

        if nodes_temp == nodes_buffer:
            return nodes_buffer, facts_buffer, result_buffer
