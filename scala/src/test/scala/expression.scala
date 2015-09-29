import org.scalatest.{FlatSpec, Matchers}
import theoremProver._

class AtomExprSpec extends FlatSpec with Matchers {
  behavior of "A"

  it should "equals to A itself" in {
    val exp = new Atom("A")
    assert(exp == exp)
  }

  it should "equals to a copy of A" in {
    val exp1 = new Atom("A")
    val exp2 = new Atom("A")
    assert(exp1 == exp2)
  }

  it should "not equals to anything else" in {
    val exp = new Atom("A")
    val exp2 = new Atom("B")
    val exp3 = new Atom("C")
    val exp4 = new And(exp2, exp3)
    assert(exp != NoneExpression)
    assert(exp != exp2)
    assert(exp != exp3)
    assert(exp != exp4)
  }

  it should "be found in set(A)" in {
    val expr1 = new Atom("A")
    val expr2 = new Atom("A")
    val expr3 = new Atom("B")
    val s = Set(expr1)
    assert(s contains expr1)
    assert(s contains expr2)
    assert((s contains expr3) == false)
  }
}

class NotExprSpec extends FlatSpec with Matchers {
  behavior of "Not"

  it should "equals to itself" in {
    val g = new Atom("G")
    val expr = new Not(g)
    assert(g == g)
  }
}

class NoneExprSpec extends FlatSpec with Matchers {
  behavior of "NoneExpression"

  it should "equals to itself" in {
    assert(NoneExpression == NoneExpression)
  }
}

class AndExprSpec extends FlatSpec with Matchers {
  behavior of "A and B"

  it should "equals to (A and B) itself" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val exp = new And(atom1, atom2)
    assert(exp == exp)
  }

  it should "equals to a copy of (A and B)" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val exp1 = new And(atom1, atom2)
    val exp2 = new And(atom1, atom2)
    assert(exp1 == exp2)
  }

  it should "not equals to anything else" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val exp1 = new And(atom1, atom2)
    val exp2 = new And(atom1, atom1)
    val exp3 = new And(atom2, atom2)
    assert(exp1 != exp2)
    assert(exp1 != exp3)
  }

  it should "have two child" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val atom3 = new Atom("C")
    val atom4 = new Atom("A")
    val expr = new And(atom1, atom2)
    assert(expr.brother(atom1) == atom2)
    assert(expr.brother(atom2) == atom1)
    assert(expr.brother(atom3) == NoneExpression)
    assert(expr.brother(atom4) == atom2)
  }
}


class OrExprSpec extends FlatSpec with Matchers {
  behavior of "A or B"

  it should "equals to (A or B) itself" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val expr = new Or(atom1, atom2)
    assert(expr == expr)
  }

  it should "equals to a copy of (A or B)" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val expr1 = new Or(atom1, atom2)
    val expr2 = new Or(atom1, atom2)
    assert(expr1 == expr2)
  }

  it should "not equals to anything else" in {
    val atom1 = new Atom("A")
    val atom2 = new Atom("B")
    val exp1 = new Or(atom1, atom2)
    val exp2 = new Or(atom1, atom1)
    val exp3 = new Or(atom2, atom2)
    assert((exp1 == exp2) == false)
    assert((exp1 == exp3) == false)
    assert(exp1 != exp2)
    assert(exp1 != exp3)
  }
}
