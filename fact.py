import operater.Operator


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
