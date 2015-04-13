import scala.io.StdIn.readLine

trait Expression {
  def ==[T <: Expression](that: T): Boolean
  def toString: String
}

class AtomExpression(token: String) extends Expression {
  val expression = token

  def ==[T <: Expression](that: T) = that match {
    case x: AtomExpression =>
      if(x.expression == expression) true else false
    case _ => false
  }

  override def toString = expression
}

class NotExpression[T <: Expression](token: T) extends Expression {
  val expression = token

  def ==[T <: Expression](that: T) = that match {
    case x: NotExpression[_] =>
      if(x.expression == expression) true else false
    case _ => false
  }

  override def toString = "not " + expression
}

object Token {
  // Command
  val AddPre = "pre"
  val AddCon = "con"
  val ListPre = "pres"
  val ListCon = "cons"
  val Remove = "remove"
  val Reset = "Reset"
  val NoParaComs = Array(ListPre, ListCon, Reset)
  val WithParaComs = Array(AddPre, AddCon, Remove)

  // Punctuation
  val Dot = "."
  val Open = "("
  val Close = ")"
  val Comma = ","

  // Operation
  val Not = Array("not", "-", "!")
  val And = Array("and", "&")
  val Or = Array("or", "|")
  val Imp = Array("implies", "->")
  val Equi = Array("equi", "<->")

  // Collection of tokens
  val Commands = NoParaComs ++ WithParaComs
  val BinOps = And ++ Or ++ Imp ++ Equi  // Binary operations
  val Puncts = Array(Dot, Open, Close, Comma)
  val Tokens = Commands ++ BinOps ++ Puncts ++ Not  // All tokens
  val Symbols = Tokens filter (_.matches("^[-\\.(),!&^|>=<]*$"))
}

object Parser {
  /** convert string to array split by tokens
    *
    * @param command the string
    * @return a array of string split by tokens
    */
  def fromString(command: String): Array[String] = {
    var formatCommand = command.replace("<->", " equi ").replace("->", " implies ")
    for(symbol <- Token.Symbols) {
      formatCommand = formatCommand.replace(symbol, " " + symbol + " ")
    }
    formatCommand.split("\\s+")
  }

  def process() {}

  /**
    * parse command and compute the result
    *
    * @param command the input command line
    */
  def parse(command: String) {
    val args = fromString(command)
    if(Token.Commands contains args(0)) {
      if(Token.WithParaComs contains args(0)) {
      }
      else if(args.length > 1)
        println("Unexpected parameters: " + args.drop(1).mkString(" "))
      else {
      }
    }
    else
      println("Unexpected keyword: " + args(0))
  }
}

object Prover {
}

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
  def main(args: Array[String]) {
    val x = new AtomExpression("X")
    val y = new AtomExpression("Y")
    val a = new NotExpression(x)
    val b = new NotExpression(x)
    val c = new NotExpression(y)
    println(a == b)
    println(a == c)
    // init()
  }
}
