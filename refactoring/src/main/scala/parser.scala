package theoremProver

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
  // TODO Exception handler
  var pres: Array[Expression] = Array()
  var cons: Array[Expression] = Array()

  /**
    * parse command and compute the result
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
            pres :+= exp
            println("Premise added: " + exp)
          }
          case Token.AddCon => {}
          case Token.Remove => {}
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
      Prover.prove(pres, expression) match {
        case true => println("Expression proven: " + expression)
        case false => println("Expression unprovable: " + expression)
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
      println("Empty expression")
      NoneExpression
    }
    else {
      var pos = -1
      var op = ""
      var depth = 0
      var i = -1
      var break = false
      while(i+1 < tokens.length && break == false) {
        i += 1
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
          case x => {}
        }
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
}
