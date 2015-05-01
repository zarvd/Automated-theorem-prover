package theoremProver

import scala.language.implicitConversions

class Sequent {
  var premises: Set[Expression] = _
  var conclusions: Set[Expression] = _
  var depth: Int = _

  def isOverlap: Boolean =
    ! (premises & conclusions).isEmpty

  override def toString =
    premises.mkString(", ") + " => " + conclusions.mkString(", ")
}

object Prover {
  implicit def expToBool(exp: Expression): Boolean = NoneExpression != exp

  var premises: Set[Sequent] = Set()
  var conclusion: List[Sequent] = List()

  def prove(pres: Array[Expression], con: Expression): Boolean = {
    val seq = new Sequent {
      premises = pres.toSet
      conclusions = Set(con)
      depth = 0
    }
    premises = Set(seq)
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
      printSequent(curSeq)
      if(curSeq.isOverlap) {
        premises += curSeq
        scan()
      }
      else process(curSeq)
    }
  }

  def process(seq: Sequent): Boolean = {

    var applyPre = false

    var preDepth: Int = 0
    var pre: Expression = NoneExpression
    for(expr <- seq.premises) {
      if(! expr.isInstanceOf[Atom]) {
        pre = expr
        applyPre = true
      }
    }
    var conDepth: Int = 0
    var con: Expression = NoneExpression
    for(expr <- seq.conclusions) {
      if(! expr.isInstanceOf[Atom]) {
        con = expr
        applyPre = false
      }
    }
    if( ! (pre || con)) false
    else {
      val seqA = new Sequent {
        premises = seq.premises
        conclusions = seq.conclusions
        depth = seq.depth + 1
      }
      val seqB = new Sequent {
        premises = seq.premises
        conclusions = seq.conclusions
        depth = seq.depth + 1
      }

      applyPre match {
        case true => {
          seqA.premises -= pre
          seqB.premises -= pre

          pre match {
            case x: Not => {
              seqA.conclusions += x.expr
              conclusion :+= seqA
              scan()
            }
            case x: And => {
              seqA.premises += x.lExpr
              seqA.premises += x.rExpr
              conclusion :+= seqA
              scan()
            }
            case x: Or => {
              seqA.premises += x.lExpr
              seqB.premises += x.rExpr
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case x: Implies => {
              val temp = new Not(x.lExpr)
              seqA.premises += temp
              seqB.premises += x.rExpr
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case x: Equiv => {
              val tempA = new Implies(x.lExpr, x.rExpr)
              val tempB = new Implies(x.rExpr, x.lExpr)
              seqA.premises += tempA
              seqA.premises += tempB
              conclusion :+= seqA
              scan()
            }
            case _ => process(seq)
          }
        }
        case false => {
          seqA.conclusions -= con
          seqB.conclusions -= con

          con match {
            case x: Not => {
              seqA.premises += x.expr
              conclusion :+= seqA
              scan()
            }
            case x: And => {
              seqA.conclusions += x.lExpr
              seqB.conclusions += x.rExpr
              conclusion :+= seqA
              conclusion :+= seqB
              scan()
            }
            case x: Or => {
              seqA.conclusions += x.lExpr
              seqA.conclusions += x.rExpr
              conclusion :+= seqA
              scan()
            }
            case x: Implies => {
              seqA.premises += x.lExpr
              seqA.conclusions += x.rExpr
              conclusion :+= seqA
              scan()
            }
            case x: Equiv => {
              val tempA = new Implies(x.lExpr, x.rExpr)
              val tempB = new Implies(x.rExpr, x.lExpr)
              seqA.conclusions += tempA
              seqA.conclusions += tempB
              conclusion :+= seqA
              scan()
            }
            case _ => process(seq)
          }
        }
      }
    }
  }

  def printSequent(seq: Sequent) {
    println("[" + seq.depth + "]" + " " + seq)
  }
}
