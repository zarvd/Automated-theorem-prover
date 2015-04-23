import org.scalatest.{FlatSpec, Matchers}
import theoremProver._


class ProverSpec extends FlatSpec with Matchers {
  implicit def stringToExpr(s: String): Expression = Parser.process(Parser.fromString(s))

  def prove(expr: Expression): Boolean =
    Prover.prove(Array(), expr)

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

  "((P->Q) and (P->(not Q))) -> (not P)" should "be provable" in {
    val expr = "((P->Q) and (P->(not Q))) -> (not P)"
    assert(prove(expr) == true)
  }

  "(not P) -> (P -> Q)" should "be provable" in {
    val expr = "(not P) -> (P -> Q)"
    assert(prove(expr) == true)
  }

  "(not (not P)) -> P" should "be provable" in {
    val expr = "(not (not P)) -> P"
    assert(prove(expr) == true)
  }

  "(P and Q) -> (P or Q)" should "be provable" in {
    val expr = "(P and Q) -> (P or Q)"
    assert(prove(expr) == true)
  }

  "((P or Q) and (P -> R) and (Q -> R)) -> R" should "be provable" in {
    val expr = "((P or Q) and (P -> R) and (Q -> R)) -> R"
    assert(prove(expr) == true)
  }
}
