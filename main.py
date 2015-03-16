from optparse import OptionParser

from logic import LogicParser
from render import bcolors


def process(line):
    tokens = LogicParser.fromstring(line)
    LogicParser.parse(tokens)


def readline():
    bcolors.print_header('Automated Logic Prover')
    bcolors.print_ok('Terms:', 'green')
    bcolors.print_ok('  X                          (proposition)')
    bcolors.print_ok('Expression:', 'green')
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
    bcolors.print_ok('  pre <expression>           (add an premise)')
    bcolors.print_ok('  con <expression>           '
                     '(prove and add a conclusion)')
    bcolors.print_ok('  remove <expression>        '
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
        ['-(P|Q)'],
        ['-(P&Q)'],
        ['P->Q', 'P->-Q'],
        ['-P'],
        ['--P'],
        ['P', 'Q'],
        ['P&Q'],
        ['P'],
        ['P|Q', 'P->R', 'Q->R'],
        ['P->Q', 'Q->P'],
        ['P<->Q'],
        ['P', 'P->Q']
        ]
    conclusion = [
        '-P&-Q',
        '-P|-Q',
        '-P',
        'P->R',
        'P',
        'P&Q',
        'P',
        'P|Q',
        'R',
        'P<->Q',
        'P->Q',
        'Q'
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
