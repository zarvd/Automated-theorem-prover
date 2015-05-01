package theoremProver

sealed abstract class Expression

object NoneExpression extends Expression {
  override def toString = "None Expression"
}

final case class Atom(expr: String) extends Expression {
  override def toString = expr
}

case class Not(expr: Expression) extends Expression {
  override def toString = "¬" + expr
}

sealed abstract class BinaryExpr() extends Expression {
  def lExpr: Expression
  def rExpr: Expression
  def operator: String
  final override def toString = "(" + lExpr + " " + operator + " " + rExpr + ")"
}

sealed trait Brother {
  val lExpr: Expression
  val rExpr: Expression
  final def brother(child: Any): Expression =
    child match {
      case `lExpr` => rExpr
      case `rExpr` => lExpr
      case _ => NoneExpression
    }
}

case class And(lExpr: Expression, rExpr: Expression) extends BinaryExpr with Brother {
  val operator = "∧"
}

case class Or(lExpr: Expression, rExpr: Expression) extends BinaryExpr with Brother {
  val operator = "∨"
}

case class Equiv(lExpr: Expression, rExpr: Expression) extends BinaryExpr with Brother {
  val operator = "↔"
}

case class Implies(lExpr: Expression, rExpr: Expression) extends BinaryExpr {
  val operator = "→"
}

sealed abstract class Quantifier extends Expression {
  def atom: Atom
  def expr: Expression
  def symbol: String
  override def toString = "(" + symbol + Atom + ")(" + expr + ")"
}

case class Forall(atom: Atom, expr: Expression) extends Quantifier {
  val symbol = "∀"
}

case class Exist(atom: Atom, expr: Expression) extends Quantifier {
  val symbol = "∃"
}
