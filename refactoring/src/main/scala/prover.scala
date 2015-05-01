package theoremProver

import scala.language.implicitConversions

class Sequent(var pres: Set[Expression], var cons: Set[Expression], var depth: Int) {

  def isOverlap: Boolean = ! (pres & cons).isEmpty

  override def toString = "[" + depth + "]" + " " + pres.mkString(", ") + " => " + cons.mkString(", ")
}

object Prover {
  implicit def expToBool(expr: Expression): Boolean = NoneExpression != expr

  var premises: Set[Sequent] = Set()
  var conclusion: List[Sequent] = List()

  def prove(pre: Set[Expression], con: Expression): Boolean = {
    val seq = new Sequent(pre, Set(con), 0)
    conclusion = List(seq)
    scan()
  }

  def scan(): Boolean = {
    if(conclusion.isEmpty) true
    else {
      val (overlap, con) = conclusion span (premises contains _)
      val curSeq =
        if(con.isEmpty) overlap.last
        else {
          val seq = con.head
          conclusion = con drop 1
          seq
        }
      println(curSeq)
      if(curSeq.isOverlap) {
        premises += curSeq
        scan()
      }
      else process(curSeq)
    }
  }

  def process(seq: Sequent): Boolean = {

    var pre = (seq.pres find (! _.isInstanceOf[Atom])) getOrElse NoneExpression
    var con = (seq.cons find (! _.isInstanceOf[Atom])) getOrElse NoneExpression

    if( ! (pre || con)) false
    else {

      val applyPre = if(con) false else true

      val seqA = new Sequent(seq.pres, seq.cons, seq.depth + 1)
      val seqB = new Sequent(seq.pres, seq.cons, seq.depth + 1)

      applyPre match {
        case true => {
          seqA.pres -= pre
          seqB.pres -= pre

          pre match {
            case x: Not => {
              seqA.cons += x.expr
              conclusion :+= seqA
              scan()
            }
            case x: And => {
              seqA.pres += x.lExpr
              seqA.pres += x.rExpr
              conclusion :+= seqA
              scan()
            }
            case x: Or => {
              seqA.pres += x.lExpr
              seqB.pres += x.rExpr
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case x: Implies => {
              seqA.pres += new Not(x.lExpr)
              seqB.pres += x.rExpr
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case x: Equiv => {
              seqA.pres += new Implies(x.lExpr, x.rExpr)
              seqA.pres += new Implies(x.rExpr, x.lExpr)
              conclusion :+= seqA
              scan()
            }
            case _ => process(seq)
          }
        }
        case false => {
          seqA.cons -= con
          seqB.cons -= con

          con match {
            case x: Not => {
              seqA.pres += x.expr
              conclusion :+= seqA
              scan()
            }
            case x: And => {
              seqA.cons += x.lExpr
              seqB.cons += x.rExpr
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case x: Or => {
              seqA.cons += x.lExpr
              seqA.cons += x.rExpr
              conclusion :+= seqA
              scan()
            }
            case x: Implies => {
              seqA.pres += x.lExpr
              seqA.cons += x.rExpr
              conclusion :+= seqA
              scan()
            }
            case x: Equiv => {
              seqA.cons += new Implies(x.lExpr, x.rExpr)
              seqB.cons += new Implies(x.rExpr, x.lExpr)
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case _ => process(seq)
          }
        }
      }
    }
  }
}
