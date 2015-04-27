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
  val Imp = Set("implies", "->")
  val Equi = Set("equi", "<->")

  // Collection of tokens
  val Commands = NoParaComs ++ WithParaComs
  val BinOps = And ++ Or ++ Imp ++ Equi  // Binary operations
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

object Parser {
  // TODO Exception handler
  var pres: Array[Expression] = Array()
  var cons: Array[Expression] = Array()

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
              pres :+= exp
              println("Premise added: " + exp)
            }
          }
          case Token.AddCon => {
            val expr = process(args drop 1)
            if(expr != NoneExpression) {
              Prover.prove(pres, expr) match {
                case true => {
                  println("Expression proven: " + expr)
                  cons :+= expr
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
          pres = Array()
          cons = Array()
          println("All reset")
        }
      }
    }
    else {
      // conclusion only
      val expression = process(args)
      if(expression != NoneExpression) {
        Prover.prove(pres, expression) match {
          case true => println("Expression proven: " + expression)
          case false => println("Expression unprovable: " + expression)
        }
      }
    }
  }

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
    formatCommand.trim split("\\s+")
  }

  def process(tokens: Array[String]): Expression = {
    if(tokens.isEmpty) {
      throw new MissingExpressionExcetion("Empty expression")
      // NoneExpression
    }
    else {
      var op = ""
      var bracketDepth = 0
      var currentPos = -1
      var markPos = -1
      var isBinary = false
      while(currentPos+1 < tokens.length && isBinary == false) {
        currentPos += 1
        tokens(currentPos) match {
          case Token.Open => bracketDepth += 1
          case Token.Close => bracketDepth -= 1
          case x if(bracketDepth == 0) => {
            markPos = currentPos
            isBinary = true
            x match {
              case imp if Token.Imp contains imp => op = "imp"
              case or if Token.Or contains or => op = "or"
              case and if Token.And contains and => op = "and"
              case equi if Token.Equi contains equi => op = "equi"
              case _ => isBinary = false
            }
          }
          case _ => {}
        }
      }

      try {
        if(isBinary == true) {
          if( ! tokens(markPos+1).head.isUpper)
            throw new MissingExpressionExcetion("Missing expression in " + tokens(markPos) + " connective")
          else {
            val lExpr = process(tokens slice(0, markPos))
            val rExpr = process(tokens drop markPos+1)
            op match {
              case "imp" => new ImpExpression(lExpr, rExpr)
              case "or" => new OrExpression(lExpr, rExpr)
              case "and" => new AndExpression(lExpr, rExpr)
              case "equi" => new EquiExpression(lExpr, rExpr)
            }
          }
        }
        else tokens.head match {
          case not if Token.Not contains not => {
            if(tokens.length < 2)
              throw new MissingExpressionExcetion("Missing expression in Not connective")
            else
              new NotExpression(process(tokens drop 1))
          }
          case atom if atom.head.isUpper => {
            if(atom.length == 1) new AtomExpression(atom)
            else NoneExpression
          }
          case Token.Open => {
            if(tokens.last != Token.Close) {
              throw new MissingExpressionExcetion("Missing ')'")
            }
            if(tokens.length == 2) {
              throw new MissingExpressionExcetion("Missing expression in parenthetical group")
            }
            process(tokens slice(1, tokens.length))
          }
          case _ => throw new IllegalPremisesException("Unable to parse " + tokens.mkString(" "))
        }
      } catch {
        case e: IllegalPremisesException => NoneExpression
        case e: MissingExpressionExcetion => NoneExpression
      }
    }
  }
}
