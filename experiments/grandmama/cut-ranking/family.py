"""Evaluate a cut in the two-return family by a smaller fixed-density query."""
from math import comb
from cut_rank import rank

def expand(q,h):
    return q.replace("1","0"*h+"1")

def pullback(b,tokens,h):
    """First reversed token key whose expanded reversal reaches b's reversal."""
    left,right=0,1<<tokens
    target=b[::-1]
    while left<right:
        mid=(left+right)//2
        rev_token=format(mid,"0%db"%tokens)
        rev_expanded=rev_token.replace("1","1"+"0"*h)
        if rev_expanded<target:
            left=mid+1
        else:
            right=mid
    return left

def family_mass(b,tokens,ones,h):
    if h<1 or not 0<ones<tokens or len(b)!=tokens+h*ones or set(b)-set("01"):
        raise ValueError("inconsistent binary cut or family parameters")
    cutoff=pullback(b,tokens,h)
    if cutoff==1<<tokens:
        small_mass=comb(tokens,ones)
    else:
        a=format(cutoff,"0%db"%tokens)[::-1]
        small_mass=rank(a,density=ones)[0]
    numerator=len(b)*small_mass
    mass,remainder=divmod(numerator,tokens)
    assert remainder==0
    return mass

def next_layer_key(key,tokens,ones):
    """Least integer >= key with exactly ones set bits, or None."""
    if key.bit_count()==ones:
        return key
    # Choose the least significant feasible first upward difference.
    for bit in range(tokens):
        if (key>>bit)&1:
            continue
        prefix=(key>>(bit+1))<<1 | 1
        needed=ones-prefix.bit_count()
        if 0<=needed<=bit:
            return (prefix<<bit) | ((1<<needed)-1)
    return None

def rank_via_family(a):
    """Reduction to an arbitrary-cut family oracle at the single marker 000."""
    T=len(a)
    key=int(a[::-1],2)
    # Constant zero contributes one iff key>0. Constant one is never strictly below.
    result=int(key>0)
    for t in range(1,T):
        first=next_layer_key(key,T,t)
        if first is None:
            result+=comb(T,t)
        else:
            q=format(first,"0%db"%T)[::-1]
            ambient=family_mass(expand(q,3),T,t,3)
            part,remainder=divmod(T*ambient,T+3*t)
            assert remainder==0
            result+=part
    return result
