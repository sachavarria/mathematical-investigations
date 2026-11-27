"""Resolve exactly two conflicting origins at a given minimum binary prefix."""
from itertools import product

def returns(u):
    mark="1"+u
    bad=["1"+u[:j]+"0" for j,b in enumerate(u) if b=="1"]
    prefs={mark[:j] for j in range(len(mark)+1)}
    for p in bad:
        prefs.update(p[:j] for j in range(len(p)+1))
    transition={}
    for p in prefs:
        for b in "01":
            t=p+b
            transition[p,b]=None if any(t.endswith(v) for v in bad) else max(
                (v for v in prefs if t.endswith(v)),key=len)
    return mark,transition

def pair_mass(a,u,density=None):
    """Accepted and rejected rooted masses among mixed cells with two marks."""
    n,h=len(a),len(u)
    mark,step=returns(u)
    yes=no=0
    def update(sign,i,b):
        if b==a[i] or abs(sign)>i: return sign
        return i+1 if b=="1" else -i-1
    for left in range(1,n):
        right=n-left
        states={(mark,mark,False,0,0,0):1}
        for t in range(max(left,right)):
            new={}
            for (p,q,smaller,c0,c1,ones),ways in states.items():
                for b,c in product("01" if t<left else ("",),"01" if t<right else ("",)):
                    s0,s1=c0,c1
                    if b and c and not smaller and b>c: continue
                    pp=step[p,b] if b else p
                    qq=step[q,c] if c else q
                    if pp is None or qq is None: continue
                    if b and (pp==mark)!=(t+1==left): continue
                    if c and (qq==mark)!=(t+1==right): continue
                    if b:
                        s0=update(s0,(h+t)%n,b)
                        s1=update(s1,(h+t-left)%n,b)
                    if c:
                        s0=update(s0,(h+left+t)%n,c)
                        s1=update(s1,(h+t)%n,c)
                    weight=0 if density is None else ones+(b=="1")+(c=="1")
                    if density is not None and weight>density: continue
                    key=(pp,qq,smaller or bool(b and c and b<c),s0,s1,weight)
                    new[key]=new.get(key,0)+ways
            states=new
        for (_,_,smaller,c0,c1,weight),ways in states.items():
            if not smaller or (c0<0)==(c1<0) or density is not None and weight!=density:
                continue
            if c0<0: yes+=n*ways
            else: no+=n*ways
    return yes,no
