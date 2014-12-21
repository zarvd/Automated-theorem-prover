""" Resolution in Propositional Logic

Basic steps for proving a proposition S:

1. Convert all propositions in premises to conjunctive normal form (CNF)
2. Negate S and convert result to CNF
3. Add negated S to premises
4. Repeat until contradiction or no progress is made:
   a. Select 2 clauses (call them parent clauses)
   b. Resolve them together
   c. If resolvent is the empty clause, a contradiction has been found
      (i.e., S follows from the premises)
   d. If not, add resolvent to the premises

"""
import logic


def clausify(expression):
    pass

def main():
    pass

def test():
    pass

if __name__ == '__main__':
    main()
