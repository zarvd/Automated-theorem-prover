import scala.io.StdIn.readLine
import theoremProver._

object Main {
  def print_help() {
    println("Automated Logic Prover")
    println("Terms:")
    println("  X                          (proposition)")
    println("Expression:")
    println("  not P, -P, !P              (complement)")
    println("  P or Q, P|Q                (disjunction)")
    println("  P and Q, P&Q, P^Q          (conjunction)")
    println("  P implies Q, P->Q          (implication)")
    println("  P equi Q, P<->Q            (equivalence)")
    println("Enter formulae at the prompt. The following commands " +
      "are also available for manipulating premises:")
    println("  pres                       (list premises)")
    println("  cons                       (list conclusion)")
    println("  pre <expression>           (add an premise)")
    println("  con <expression>           " +
      "(prove and add a conclusion)")
    println("  remove <expression>        " +
      "(remove an premise or conclusion)")
    println("  reset                      " +
      "(remove all premises and conclusion)")
    println("  help                       " +
      "(print help)")
    println("  exit                       " +
      "(exit)")
  }
  def init() {
    print_help()
    readCmd()
  }

  def readCmd(exit: Boolean = false, parser: Int = 1) {
    exit match {
      case true => println("exiting...")
      case flase => {
        val command = readLine("> ")
        command match {
          case "exit" => readCmd(true)
          case "help" => {
            print_help()
            readCmd()
          }
          case "1" => {
            println("Switch to propositional logic parser")
            readCmd(false, 1)
          }
          case "2" => {
            println("Switch to first-order logic parser")
            readCmd(false, 2)
          }
          case _ if parser == 1 => {
            PropParser.parse(command)
            readCmd()
          }
          case _ if parser == 2 => {
            PropParser.parse(command)
            readCmd()
          }
          case _ => println("Unable to parse")
        }
      }
    }
  }

  def main(args: Array[String]) {
    init()
  }
}
