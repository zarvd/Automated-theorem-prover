import scala.io.StdIn.readLine

trait Expression {
  def ==[T <: Expression](that: T): Boolean
  def toString: String
}

object NoneExpression extends Expression {
  def ==[T <: Expression](that: T) = that equals this
  override def toString = "None Expression"
}

class AtomExpression(token: String) extends Expression {
  val expression = token

  def ==[T <: Expression](that: T) = that match {
    case x: AtomExpression =>
      x.expression == expression
    case _ => false
  }

  override def toString = expression
}

class NotExpression[T <: Expression](token: T) extends Expression {
  val expression = token

  def ==[T <: Expression](that: T) = that match {
    case x: NotExpression[_] =>
      x.expression == expression
    case _ => false
  }

  override def toString = "¬ " + expression
}

trait Brother {
  val left: Expression
  val right: Expression
  def brother[T <: Expression](child: T) =
    if(child == left) right
    else if(child == right) left
    else NoneExpression
}

abstract class BinaryExpression(lExp: Expression, rExp: Expression) extends Expression{
  val left = lExp
  val right = rExp
}

class AndExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) with Brother {
  def ==[T <: Expression](that: T) = that match {
    case x: AndExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }

  override def toString = left + " ∧ " + right
}

class OrExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) with Brother {
  def ==[T <: Expression](that: T) = that match {
    case x: OrExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }

  override def toString = left + " ∨ " + right
}

class ImpExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) {
  def ==[T <: Expression](that: T) = that match {
    case x: ImpExpression =>
      x.left == left && x.right == right
    case _ => false
  }

  override def toString = left + " → " + right
}

class EquiExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) {
  def ==[T <: Expression](that: T) = that match {
    case x: EquiExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }

  override def toString = left + " ↔ " + right
}

// object Expression {
//   def atom(token: String) = new AtomExpression(token)
//   def not(token: Expression) = new NotExpression(token)
//   def and(lExp: Expression, rExp: Expression) = new AndExpression(lExp, rExp)
//   def or(lExp: Expression, rExp: Expression) = new OrExpression(lExp, rExp)
//   def imp(lExp: Expression, rExp: Expression) = new ImpExpression(lExp, rExp)
//   def equi(lExp: Expression, rExp: Expression) = new EquiExpression(lExp, rExp)
// }

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

  def process(tokens: Array[String]): Expression = {
    if(tokens.isEmpty) {
      println("Empty expression")
      NoneExpression
    }
    else {
      var pos: Int = -1
      var op = ""
      var depth = 0
      var i = 0
      var break = false
      while(i < tokens.length && break == false) {
        tokens(i) match {
          case Token.Open => depth += 1
          case Token.Close => depth -= 1
          case x if(depth == 0) => {
            pos = i
            break = true
            x match {
              case _ if Token.Imp contains x => op = "imp"
              case _ if Token.Or contains x => op = "or"
              case _ if Token.And contains x => op = "and"
              case _ if Token.Equi contains x => op = "equi"
              case _ => break = false
            }
          }
        }
        i += 1
      }

      if(break == true) {
        if(pos == tokens.length - 1) {
          println("Missing expression in " + tokens(pos) + " connective")
          NoneExpression
        }
        else op match {
          case "imp" =>
            new ImpExpression(process(tokens slice(0, pos)), process(tokens drop pos+1))
          case "or" =>
            new OrExpression(process(tokens slice(0, pos)), process(tokens drop pos+1))
          case "and" =>
            new AndExpression(process(tokens slice(0, pos)), process(tokens drop pos+1))
          case "equi" =>
            new EquiExpression(process(tokens slice(0, pos)), process(tokens drop pos+1))
        }
      }
      else tokens(0) match {
        case not if Token.Not contains not => {
          if(tokens.length < 2) {
            println("Missing expression in Not connective")
            NoneExpression
          }
          else new NotExpression(process(tokens drop 1))
        }
        case atom if atom forall(_.isUpper) => {
          if(atom.length == 1) new AtomExpression(atom)
          else NoneExpression
        }
        case Token.Open => {
          if(tokens.last != Token.Close) {
            println("Missing ')'")
            NoneExpression
          }
          if(tokens.length == 2) {
            println("Missing expression in parenthetical group")
            NoneExpression
          }
          process(tokens slice(1, tokens.length))
        }
        case _ => {
          println("Unable to parse " + tokens.mkString(" "))
          NoneExpression
        }
      }
    }
  }

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
        // command with NO parameter
      }
    }
    else
      println(process(args))
    // println("Unexpected keyword: " + args(0))
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
