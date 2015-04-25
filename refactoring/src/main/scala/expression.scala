package theoremProver

sealed abstract class Expression {
  def log(msg: String): String = "(" + msg + ")"
}

object NoneExpression extends Expression {
  override def toString = "None Expression"
}

final class AtomExpression(token: String) extends Expression {
  val expression = token

  override def equals(that: Any): Boolean = that match {
    case x: AtomExpression => x.expression == expression
    case _ => false
  }

  override def hashCode = token.hashCode

  override def toString = expression
}

final class NotExpression(token: Expression) extends Expression {
  val expression = token

  override def equals(that: Any): Boolean = that match {
    case x: NotExpression => x.expression == expression
    case _ => false
  }

  override def toString = log("¬ " + expression)
}

sealed abstract class BinaryExpression(lExp: Expression, rExp: Expression) extends Expression{
  val left = lExp
  val right = rExp

  val operator: String

  final override def toString = log(left + " " + operator + " " + right)
}

sealed abstract class BrotherExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) {
  final def brother(child: Any): Expression =
    child match {
      case `left` => right
      case `right` => left
      case _ => NoneExpression
    }
}

final class AndExpression(lExp: Expression, rExp: Expression) extends BrotherExpression(lExp, rExp) {

  val operator = "∧"

  override def equals(that: Any) = that match {
    case x: AndExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }
}

final class OrExpression(lExp: Expression, rExp: Expression) extends BrotherExpression(lExp, rExp) {

  val operator = "∨"

  override def equals(that: Any) = that match {
    case x: OrExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }
}

final class ImpExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) {

  val operator = "→"

  override def equals(that: Any) = that match {
    case x: ImpExpression =>
      x.left == left && x.right == right
    case _ => false
  }
}

final class EquiExpression(lExp: Expression, rExp: Expression) extends BrotherExpression(lExp, rExp) {

  val operator = "↔"

  override def equals(that: Any) = that match {
    case x: EquiExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }
}
