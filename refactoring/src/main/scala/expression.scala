package theoremProver

trait Expression {
  def ==[T <: Expression](that: T): Boolean
  def log(msg: String): String = "(" + msg + ")"
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

  override def toString = log("¬ " + expression)
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

  override def toString = log(left + " ∧ " + right)
}

class OrExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) with Brother {
  def ==[T <: Expression](that: T) = that match {
    case x: OrExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }

  override def toString = log(left + " ∨ " + right)
}

class ImpExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) {
  def ==[T <: Expression](that: T) = that match {
    case x: ImpExpression =>
      x.left == left && x.right == right
    case _ => false
  }

  override def toString = log(left + " → " + right)
}

class EquiExpression(lExp: Expression, rExp: Expression) extends BinaryExpression(lExp, rExp) {
  def ==[T <: Expression](that: T) = that match {
    case x: EquiExpression =>
      (x.left == left && x.right == right) || (x.left == right && x.right == left)
    case _ => false
  }

  override def toString = log(left + " ↔ " + right)
}


// object Expression {
//   def atom(token: String) = new AtomExpression(token)
//   def not(token: Expression) = new NotExpression(token)
//   def and(lExp: Expression, rExp: Expression) = new AndExpression(lExp, rExp)
//   def or(lExp: Expression, rExp: Expression) = new OrExpression(lExp, rExp)
//   def imp(lExp: Expression, rExp: Expression) = new ImpExpression(lExp, rExp)
//   def equi(lExp: Expression, rExp: Expression) = new EquiExpression(lExp, rExp)
// }
