package theoremProver

sealed abstract class Expression {}

object NoneExpression extends Expression {
  override def toString = "None Expression"
}

case class Atom(expression: String) extends Expression

case class Not(expression: Expression) extends Expression

sealed abstract class BinaryExpr(lExpr: Expression, rExpr: Expression) extends Expression

sealed abstract class BrotherExpr(lExpr: Expression, rExpr: Expression) extends BinaryExpr(lExpr, rExpr) {
  final def brother(child: Any): Expression =
    child match {
      case `lExpr` => rExpr
      case `rExpr` => lExpr
      case _ => NoneExpression
    }
}

case class And(lExpr: Expression, rExpr: Expression) extends BrotherExpr(lExpr, rExpr)

case class Or(lExpr: Expression, rExpr: Expression) extends BrotherExpr(lExpr, rExpr)

case class Equiv(lExpr: Expression, rExpr: Expression) extends BrotherExpr(lExpr, rExpr)

case class Implies(lExpr: Expression, rExpr: Expression) extends BinaryExpr(lExpr, rExpr)
