package theoremProver

sealed abstract class Expression

object NoneExpression extends Expression {
  override def toString = "None Expression"
}

case class Atom(expr: String) extends Expression {
  override def toString = expr
}

case class Not(expr: Expression) extends Expression {
  override def toString = "¬" + expr
}

sealed abstract class BinaryExpr(lExpr: Expression, rExpr: Expression) extends Expression {
  def operator: String
  override def toString = "(" + lExpr + " " + operator + " " + rExpr + ")"
}

sealed abstract class BrotherExpr(lExpr: Expression, rExpr: Expression) extends BinaryExpr(lExpr, rExpr) {
  final def brother(child: Any): Expression =
    child match {
      case `lExpr` => rExpr
      case `rExpr` => lExpr
      case _ => NoneExpression
    }
}

case class And(lExpr: Expression, rExpr: Expression) extends BrotherExpr(lExpr, rExpr) {
  val operator = "∧"
}

case class Or(lExpr: Expression, rExpr: Expression) extends BrotherExpr(lExpr, rExpr) {
  val operator = "∨"
}

case class Equiv(lExpr: Expression, rExpr: Expression) extends BrotherExpr(lExpr, rExpr) {
  val operator = "↔"
}

case class Implies(lExpr: Expression, rExpr: Expression) extends BinaryExpr(lExpr, rExpr) {
  val operator = "→"
}
