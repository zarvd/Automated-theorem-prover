import org.scalatest.{FlatSpec, Matchers}
import theoremProver._

class AtomExprSpec extends FlatSpec with Matchers {
  "A" should "equals to A itself" in {
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
  // it should "equals to (not (not A))" in {
  //   val exp1 = new AtomExpression("A")
  //   val exp2 = new NotExpression(exp1)
  //   val exp3 = new NotExpression(exp2)
  //   assert(exp1 != exp2)
  //   assert(exp2 != exp3)
  //   assert(exp1 == exp3)
  // }
}

class NotExprSpec extends FlatSpec with Matchers {

}

class AndExprSpec extends FlatSpec with Matchers {
  "(A and B)" should "equals to (A and B) itself" in {
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
  }
  it should "not equals to anything else" in {
    val atom1 = new AtomExpression("A")
    val atom2 = new AtomExpression("B")
    val exp1 = new AndExpression(atom1, atom2)
    val exp2 = new AndExpression(atom1, atom1)
    val exp3 = new AndExpression(atom2, atom2)
    val exp4 = new AndExpression(atom2, atom1)
    assert(exp1 != exp2)
    assert(exp1 != exp3)
    assert(exp1 != exp4)
  }
  // "(A and (B and C))" should "equals to (B and (A and C))" in {
  //   val a = new AtomExpression("A")
  //   val b = new AtomExpression("B")
  //   val c = new AtomExpression("C")
  //   val and1 = new AndExpression(a, b)
  //   val and2 = new AndExpression(b, c)
  //   val and3 = new AndExpression(a, c)
  //   val exp1 = new AndExpression(a, and2)
  //   val exp2 = new AndExpression(b, and3)
  //   val exp3 = new AndExpression(c, and1)
  //   assert(exp1 == exp2)
  //   assert(exp1 == exp3)
  //   assert(exp2 == exp3)
  // }
}


class OrExprSpec extends FlatSpec with Matchers {
  "A or B" should "equals to (A or B) itself" in {
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
  }
}
