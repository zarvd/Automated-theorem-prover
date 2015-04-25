import org.scalatest.{FlatSpec, Matchers}
import theoremProver._

class AtomExprSpec extends FlatSpec with Matchers {
  behavior of "A"

  it should "equals to A itself" in {
    val exp = new AtomExpression("A")
    assert(exp == exp)
  }

  it should "equals to a copy of A" in {
    val exp1 = new AtomExpression("A")
    val exp2 = new AtomExpression("A")
    assert(exp1 == exp2)
  }

  it should "not equals to anything else" in {
    val exp = new AtomExpression("A")
    val exp2 = new AtomExpression("B")
    val exp3 = new AtomExpression("C")
    val exp4 = new AndExpression(exp2, exp3)
    assert(exp != NoneExpression)
    assert(exp != exp2)
    assert(exp != exp3)
    assert(exp != exp4)
  }

  it should "be found in set(A)" in {
    val expr1 = new AtomExpression("A")
    val expr2 = new AtomExpression("A")
    val expr3 = new AtomExpression("B")
    val s = Set(expr1)
    assert(s contains expr1)
    assert(s contains expr2)
    assert((s contains expr3) == false)
  }
}

class NotExprSpec extends FlatSpec with Matchers {
  behavior of "NotExpression"

  it should "equals to itself" in {
    val g = new AtomExpression("G")
    val expr = new NotExpression(g)
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
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val exp = new AndExpression(atom1, atom2)
    assert(exp == exp)
  }

  it should "equals to a copy of (A and B)" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val exp1 = new AndExpression(atom1, atom2)
    val exp2 = new AndExpression(atom1, atom2)
    assert(exp1 == exp2)
  }

  it should "equals to (B and A)" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val exp1 = new AndExpression(atom1, atom2)
    val exp2 = new AndExpression(atom2, atom1)
    assert(exp1 == exp2)
    assert((exp1 != exp2) == false)
  }

  it should "not equals to anything else" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val exp1 = new AndExpression(atom1, atom2)
    val exp2 = new AndExpression(atom1, atom1)
    val exp3 = new AndExpression(atom2, atom2)
    assert(exp1 != exp2)
    assert(exp1 != exp3)
  }

  it should "have two child" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val atom3 = new AtomExpression("C")
    val atom4 = new AtomExpression("A")
    val expr = new AndExpression(atom1, atom2)
    assert(expr.brother(atom1) == atom2)
    assert(expr.brother(atom2) == atom1)
    assert(expr.brother(atom3) == NoneExpression)
    assert(expr.brother(atom4) == atom2)
  }
}


class OrExprSpec extends FlatSpec with Matchers {
  behavior of "A or B"

  it should "equals to (A or B) itself" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val expr = new OrExpression(atom1, atom2)
    assert(expr == expr)
  }

  it should "equals to a copy of (A or B)" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val expr1 = new OrExpression(atom1, atom2)
    val expr2 = new OrExpression(atom1, atom2)
    assert(expr1 == expr2)
  }

  it should "equals to (B or A)" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val expr1 = new OrExpression(atom1, atom2)
    val expr2 = new OrExpression(atom2, atom1)
    assert(expr1 == expr2)
  }

  it should "not equals to anything else" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val exp1 = new OrExpression(atom1, atom2)
    val exp2 = new OrExpression(atom1, atom1)
    val exp3 = new OrExpression(atom2, atom2)
    assert((exp1 == exp2) == false)
    assert((exp1 == exp3) == false)
    assert(exp1 != exp2)
    assert(exp1 != exp3)
  }
}
