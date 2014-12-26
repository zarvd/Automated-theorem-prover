from optparse import OptionParser

from logic import LogicParser, Tokens
from render import bcolors


def process(line):
    tokens = LogicParser.fromstring(line)
    LogicParser.parse(tokens)


def readline():
    bcolors.print_header('Logic Theorem Prover')
    bcolors.print_ok('Terms:', 'green')
    bcolors.print_ok('  X                          (proposition)')
    bcolors.print_ok('Formulae:', 'green')
    bcolors.print_ok('  not P, -P, !P              (complement)')
    bcolors.print_ok('  P or Q, P|Q                (disjunction)')
    bcolors.print_ok('  P and Q, P&Q, P^Q          (conjunction)')
    bcolors.print_ok('  P implies Q, P->Q          (implication)')
    bcolors.print_ok('  P equi Q, P<->Q            (equivalence)')
    bcolors.print_ok('Enter formulae at the prompt. The following commands '
                     'are also available for manipulating premises:',
                     'green')
    bcolors.print_ok('  pres                       (list premises)')
    bcolors.print_ok('  cons                       (list conclusion)')
    bcolors.print_ok('  pre <formula>              (add an premise)')
    bcolors.print_ok('  con <formula>              '
                     '(prove and add a conclusion)')
    bcolors.print_ok('  remove <formula>           '
                     '(remove an premise or conclusion)')
    bcolors.print_ok('  reset                      '
                     '(remove all premises and conclusion)')

    while True:
        try:
            line = input('\n> ')
            process(line)
        except KeyboardInterrupt:
            continue
        except EOFError:
            bcolors.print_ok('')
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
        ['G->B', 'B->C', 'C->(A&(E->R))'],
        ['G<->B'],
        ['G->B', 'B->G']
        ]
    conclusion = [
        'B',
        'R implies B',
        'not C or C',
        'G',
        'G or R',
        'B',
        'B',
        'G implies (A&(E->R))',
        '((G->B) and (B->G)) or ((not G-> not B) and (not B -> not G))',
        'G<->B'
        ]
    for index in range(len(premises)):
        bcolors.print_ok('------------', 'green')
        for pre in premises[index]:
            process('pre ' + pre)
        process('con ' + conclusion[index])
        process('reset')


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-t", "--test", action="store_true",
                      dest="run_test", help="Run test")
    (options, args) = parser.parse_args()
    if options.run_test:
        test()
    else:
        readline()


if __name__ == '__main__':
    main()
