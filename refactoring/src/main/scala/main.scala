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
    var exit = false
    while(exit == false) {
      val command = readLine("> ")
      command match {
        case "exit" => {
          exit = true
          println("exiting...")
        }
        case "help" => print_help()
        case _ => Parser.parse(command)
      }
    }
  }

  def test() {
    val x = new AtomExpression("X")
    val y = new AtomExpression("Y")
    val a = new NotExpression(x)
    val b = new NotExpression(x)
    val c = new NotExpression(y)
    val d = new AndExpression(a, b)
    val e = new AndExpression(b, a)
    println(a == b)
    println(a == c)
    println(d == e)
    println(NoneExpression == NoneExpression)
    println(d brother a)
    println(d brother c)
  }

  def main(args: Array[String]) {
    init()
  }
}
