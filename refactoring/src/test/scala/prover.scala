import scala.language.implicitConversions
import org.scalatest.{FlatSpec, Matchers}
import theoremProver._


class ProverSpec extends FlatSpec with Matchers {
  implicit def stringToExpr(s: String): Expression = Parser.process(Parser.fromString(s))

  def prove(expr: Expression): Boolean = Prover.prove(Array(), expr)

  "(not G)" should "be unprovable" in {
    val expr = "not G"
    assert(prove(expr) == false)
  }

  "G" should "be unprovable" in {
    val expr = "G"
    assert(prove(expr) == false)
  }

  "G or (not G)" should "be provable" in {
    val expr = "G or (not G)"
    assert(prove(expr) == true)
  }

  "Negation introduction" should "be provable" in {
    val expr1 = "((P -> Q) and (P -> (not Q))) -> (not P)"
    val expr2 = "((P -> Q) or (P -> (not Q))) -> (not P)"
    assert(prove(expr1) == true)
    assert(prove(expr2) == false)
  }

  "Negation elimination" should "be provable" in {
    val expr1 = "(not P) -> (P -> Q)"
    val expr2 = "P -> (P -> Q)"
    assert(prove(expr1) == true)
    assert(prove(expr2) == false)
  }

  "Double negative elimination" should "be provable" in {
    val expr1 = "(not (not P)) -> P"
    val expr2 = "(not P) -> P"
    assert(prove(expr1) == true)
    assert(prove(expr2) == false)
  }

  "Conjunction elimination" should "be provable" in {
    val expr1 = "(P and Q) -> P"
    val expr2 = "(P and Q) -> Q"
    val expr3 = "(P and Q) -> R"
    assert(prove(expr1) == true)
    assert(prove(expr2) == true)
    assert(prove(expr3) == false)
  }

  "Disjunction elimination" should "be provable" in {
    val expr1 = "((P or Q) and (P -> R) and (Q -> R)) -> R"
    val expr2 = "((P or Q) or ((P -> R) and (Q -> R))) -> R"
    assert(prove(expr1) == true)
    assert(prove(expr2) == false)
  }

  "Hypothetical syllogism" should "be provable" in {
    val expr = "((P -> Q) and (Q -> R)) -> (P -> R)"
    assert(prove(expr) == true)
  }

  "De Morgan's Theorem" should "be provable" in {
    val expr1 = "(not (P or Q)) -> ((not P) and (not Q))"
    val expr2 = "(not (P and Q)) -> ((not P) or (not Q))"
    assert(prove(expr1) == true)
    assert(prove(expr2) == true)
  }

  "Biconditional introduction" should "be provable" in {
    val expr = "((P -> Q) and (Q -> P)) -> (P <-> Q)"
    assert(prove(expr) == true)
  }

  "Biconditional elimination" should "be provable" in {
    val expr1 = "(P <-> Q) -> (P -> Q)"
    val expr2 = "(P <-> Q) -> (Q -> P)"
    assert(prove(expr1) == true)
    assert(prove(expr2) == true)
  }

  "Modus ponens" should "be provable" in {
    val expr = "(P and (P -> Q)) -> Q"
    assert(prove(expr) == true)
  }
}
