package theoremProver

object Token {
  // Command
  val AddPre = "pre"
  val AddCon = "con"
  val ListPre = "pres"
  val ListCon = "cons"
  val Remove = "remove"
  val Reset = "reset"
  val NoParaComs = Set(ListPre, ListCon, Reset)
  val WithParaComs = Set(AddPre, AddCon, Remove)

  // Punctuation
  val Dot = "."
  val Open = "("
  val Close = ")"
  val Comma = ","

  // Operation
  val Not = Set("not", "-", "!")
  val And = Set("and", "&")
  val Or = Set("or", "|")
  val Implies = Set("implies", "->")
  val Equiv = Set("equiv", "<->")

  // Quantifier
  val Forall = Set("forall")
  val Exist = Set("exist")
  val Quantifier = Forall ++ Exist

  // Collection of tokens
  val Commands = NoParaComs ++ WithParaComs
  val BinOps = And ++ Or ++ Implies ++ Equiv  // Binary operations
  val Puncts = Array(Dot, Open, Close, Comma)
  val Tokens = Commands ++ BinOps ++ Puncts ++ Not  // All tokens
  val Symbols = Tokens filter (_.matches("^[-\\.(),!&^|>=<]*$"))
}

class IllegalPremisesException(msg: String) extends IllegalArgumentException {
  println(msg)
}
class MissingExpressionExcetion(msg: String) extends IllegalArgumentException {
  println(msg)
}

abstract class Parser {
  var pres: Set[Expression] = Set()
  var cons: Set[Expression] = Set()

  /**
    * parse and excute the command
    *
    * @param command the input command line
    */
  def parse(command: String) {
    val args = fromString(command)
    if(Token.Commands contains args(0)) {
      if(Token.WithParaComs contains args(0)) {
        if(args.length < 2)
          println("Empty Expression")
        else args(0) match {
          case Token.AddPre => {
            val exp = process(args drop 1)
            if(exp != NoneExpression) {
              pres += exp
              println("Premise added: " + exp)
            }
          }
          case Token.AddCon => {
            val expr = process(args drop 1)
            if(expr != NoneExpression) {
              Prover.prove(pres, expr) match {
                case true => {
                  println("Expression proven: " + expr)
                  cons += expr
                  println("Conclusion added: " + expr)
                }
                case false => {
                  println("Expression unprovable: " + expr)
                }
              }
            }
          }
          case Token.Remove => {
            // TODO
            val expr = process(args drop 1)
          }
        }
      }
      else if(args.length > 1)
        println("Unexpected parameters: " + args.drop(1).mkString(" "))
      else args(0) match {  // command with NO parameter
        case Token.ListPre => println(pres mkString("\n"))
        case Token.ListCon => println(cons mkString("\n"))
        case Token.Reset => {
          pres = Set()
          cons = Set()
          println("All reset")
        }
      }
    }
    else {
      // conclusion only
      val expr = process(args)
      if(expr != NoneExpression)
        Prover.prove(pres, expr) match {
          case true => println("Expression proven: " + expr)
          case false => println("Expression unprovable: " + expr)
        }
    }
  }

  /** convert string to array split by tokens
    *
    * @param command the string
    * @return a array of string split by tokens
    */
  def fromString(args: String): Array[String] = {
    var cmd = args replace ("<->", " equiv ") replace ("->", " implies ")
    Token.Symbols foreach { op =>
      cmd = cmd replace (op, " " + op + " ")
    }
    require(cmd.trim.length > 0, "Empty expression")
    cmd.trim split("\\s+")
  }

  def process(tokens: Array[String]): Expression
}

object PropParser extends Parser {
  def process(tokens: Array[String]): Expression = {
    require( ! tokens.isEmpty, "Empty expression")
    searchOp(tokens)
  }

  private def searchOp(tokens: Array[String], pos: Int = 0, depth: Int = 0): Expression = {
    if(pos == tokens.length) processAtom(tokens)
    else tokens(pos) match {
      case Token.Open => searchOp(tokens, pos+1, depth+1)
      case Token.Close => searchOp(tokens, pos+1, depth-1)
      case x if(depth == 0 && (Token.BinOps contains x)) => processBinary(tokens, pos)
      case _ => searchOp(tokens, pos+1, depth)
    }
  }

  private def processBinary(tokens: Array[String], opPos: Int): Expression = {
    if(opPos == tokens.length - 1)
      throw new MissingExpressionExcetion("Missing expression in " + tokens(opPos) + " connective")
    else {
      val lExpr = process(tokens take opPos)
      val rExpr = process(tokens drop opPos+1)
      tokens(opPos) match {
        case op if Token.Implies contains op => new Implies(lExpr, rExpr)
        case op if Token.Or contains op => new Or(lExpr, rExpr)
        case op if Token.And contains op => new And(lExpr, rExpr)
        case op if Token.Equiv contains op => new Equiv(lExpr, rExpr)
      }
    }
  }

  private def processAtom(tokens: Array[String]): Expression = tokens.head match {
    case not if Token.Not contains not => new Not(process(tokens.tail))
    case atom if atom.head.isUpper => new Atom(atom)
    case Token.Open => process(tokens.tail)
    case _ => throw new IllegalPremisesException("Unable to parse " + tokens.mkString(" "))
  }
}

// object FirstOrderParser {
//   def process(tokens: Array[String]): Expression = {
//     if(tokens.isEmpty)
//       throw new MissingExpressionExcetion("Empty expression")
//     else searchOp(tokens)
//   }

//   def searchOp(tokens: Array[String], pos: Int = 0, depth: Int = 0): Expression = {
//     if(pos == tokens.length) processAtom(tokens)
//     else tokens(pos) match {
//       case Token.Open => searchOp(tokens, pos+1, depth+1)
//       case Token.Close => searchOp(tokens, pos+1, depth-1)
//       case x if(depth == 0 && (Token.BinOps contains x)) => processBinary(tokens, pos)
//       case _ => searchOp(tokens, pos+1, depth)
//     }
//   }

  // def processQuantifier(tokens: Array[String]): Expression = {
  //   val dotPos = tokens indexOf Token.Dot
  //   val section: Array[Atom] =
  //     tokens take dotPos filter (_.head.isLower) map (new Atom(_))
  //   val expr = process(tokens drop dotPos+1)

  //   tokens.head match {
  //     case x if Token.Forall contains x => new Forall(section, expr)
  //     case x if Token.Exist contains x => new Exist(section, expr)
  //   }
  // }
// }
