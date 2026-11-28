import Lean

namespace ChainObserver

-- A block of k+1 bits. The base entry is the distinguished boundary bit.
def Block : Nat → Type
  | 0 => Bool
  | k+1 => Bool × Block k

def bx (a b : Bool) := Bool.xor a b
def bor (a b : Bool) := a || b

private theorem swap4 (a b c d : Bool) :
    bx (bx a b) (bx c d) = bx (bx a c) (bx b d) := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

private theorem cancelL (a b c : Bool) (h : bx a b = bx a c) : b = c := by
  cases a <;> cases b <;> cases c <;> first | rfl | contradiction

private theorem cancelR (a b c : Bool) (h : bx a c = bx b c) : a = b := by
  cases a <;> cases b <;> cases c <;> first | rfl | contradiction

-- For q=k+1, the even block contains e_(q-1),...,e_0.
-- The odd block contains o_(q-2),...,o_0,o_(q-1).
-- Its base entry is the initial right edge. The exterior odd cell is false.
-- Each odd-site change is exactly g(e_j,o_(j-1)).
def response (g : Bool → Bool → Bool) :
    (k : Nat) → Block k → Block k → Bool
  | 0, e, edge => bx (g e false) edge
  | k+1, e, o => bx (g e.1 o.1) (response g k e.2 o.2)

def parity : (k : Nat) → Block k → Bool
  | 0, b => b
  | k+1, b => bx b.1 (parity k b.2)

def basis : (k : Nat) → Bool → Block k
  | 0, b => b
  | k+1, b => (false, basis k b)

theorem xorFactors (k : Nat) (e o : Block k) :
    response bx k e o = bx (parity k e) (parity k o) := by
  induction k with
  | zero => cases e <;> cases o <;> decide
  | succ k ih =>
    change bx (bx e.1 o.1) (response bx k e.2 o.2) = _
    rw [ih]
    exact swap4 _ _ _ _

theorem basisParity (k : Nat) (b : Bool) : parity k (basis k b) = b := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change bx false (parity k (basis k b)) = b
    rw [ih]
    cases b <;> rfl

theorem xorSameAnswers (k : Nat) (e f : Block k) :
    (∀ o, response bx k e o = response bx k f o) ↔ parity k e = parity k f := by
  constructor
  · intro h
    have w := h (basis k false)
    rw [xorFactors, xorFactors] at w
    exact cancelR _ _ _ w
  · intro h o
    rw [xorFactors, xorFactors, h]

theorem orDistinguishes (k : Nat) (e f : Block k)
    (h : ∀ o, response bor k e o = response bor k f o) : e = f := by
  induction k with
  | zero =>
    have w := h false
    cases e <;> cases f <;> first | rfl | contradiction
  | succ k ih =>
    rcases e with ⟨a, u⟩
    rcases f with ⟨b, v⟩
    have tailEq : u = v := by
      apply ih
      intro o
      have w := h (true, o)
      change bx (bor a true) (response bor k u o) =
             bx (bor b true) (response bor k v o) at w
      have one (s : Bool) : bor s true = true := by cases s <;> rfl
      rw [one, one] at w
      exact cancelL _ _ _ w
    subst v
    have w := h (false, basis k false)
    change bx (bor a false) _ = bx (bor b false) _ at w
    have bitEq := cancelR _ _ _ w
    have same : a = b := by
      cases a <;> cases b <;> first | rfl | contradiction
    cases same
    rfl

-- Every exact deterministic message scheme for OR must distinguish all blocks.
theorem orMessageInjective {M : Type} (k : Nat) (send : Block k → M)
    (answer : M → Block k → Bool)
    (correct : ∀ e o, answer (send e) o = response bor k e o)
    (e f : Block k) (h : send e = send f) : e = f := by
  apply orDistinguishes
  intro o
  rw [← correct, ← correct, h]

#print axioms ChainObserver.xorSameAnswers
#print axioms ChainObserver.basisParity
#print axioms ChainObserver.orMessageInjective
end ChainObserver
