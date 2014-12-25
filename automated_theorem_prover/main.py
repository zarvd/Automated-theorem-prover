from optparse import OptionParser

from logic import LogicParser, Tokens


premises = set()
conclusion = {}

def process(line):
    global premises
    global conclusion
    tokens = LogicParser.fromstring(line)
    LogicParser.parse(tokens)
    


def readline():
    print('Logic Theorem Prover\n')
    print('Terms:\n')
    print('  x                  (variable)')
    print('  f(term, ...)       (function)\n')
    print('Formulae:\n')
    print('  P(term)            (predicate)')
    print('  not P              (complement)')
    print('  P or Q             (disjunction)')
    print('  P and Q            (conjunction)')
    print('  P implies Q        (implication)\n')
    print('Enter formulae at the prompt. The following commands ' \
        'are also available for manipulating premises:\n')
    print('  pres                    (list premises)')
    print('  con                     (list conclusion)')
    print('  pre <formula>           (add an premise)')
    print('  con <formula>           (prove and add a conclusion)')
    print('  remove <formula>        (remove an premise or conclusion)')
    print('  reset                   (remove all premises and conclusion)')


    while True:
        try:
            line = input('\n> ')
            process(line)
        except KeyboardInterrupt:
            continue
        except EOFError:
            print('')
            return


def test():
    premises = [
        ['not G or B', 'G'],
        ['G implies B', 'R implies G'],
        ['G implies C', 'not G or B', 'not B'],
        ['B implies (C implies G)', 'B', 'C'],
        ['(B and ((R or G) and D))'],
        ['F'],
        ['(-G|B)', 'G'],
        ['G->B', 'B->C', 'C->(A&(E->R))']
        ]
    conclusion = [
        'B',
        'R implies B',
        'not C or C',
        'G',
        'G or R',
        'B',
        'B',
        'G implies (A&(E->R))'
        ]
    for index in range(len(premises)):
        print('------------')
        for pre in premises[index]:
            process('pre ' + pre)
        process('con ' + conclusion[index])
        process('reset')

        
def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-t", "--test",
                      action="store_true", dest="run_test",
                      help="Run test")
    (options, args) = parser.parse_args()
    if options.run_test:
        test()
    else:
        readline()


if __name__ == '__main__':
    main()
