"""Number of distinct future response functions at an arbitrary cut, mask 4 or 2."""
from bisect import bisect_right
from collections import defaultdict
from check_ladder import classes


def count_responses(site, time, known, mask=4):
    """Known initial coordinates arrive before the cut. Time and site are fixed."""
    if min(site,time)<0 or mask not in (2,4):
        raise ValueError("expected nonnegative site/time and mask 2 or 4")
    # Complement conjugates mask 2 to mask 4, with a fixed-one ghost.
    r=(site+int(mask==4))//2
    active=[j for j in range(1,r+1) if j&time==j]
    known_gates=[j for j in range(1,r+1) if site-2*j+1 in known]
    unseen_gates=[j for j in range(1,r+1) if site-2*j+1 not in known]
    h_values=unseen_gates+[r+1]
    groups=defaultdict(dict)
    for stop in known_gates+[r+1]:
        unknown_data=[]
        free={0} if site in known else set() # first h coordinate of all-ones vector
        shift=None
        for j in active:
            if j>=stop:
                break
            first=bisect_right(h_values,j) # position where step vector becomes 1
            v=site-2*j
            if v<0:
                shift=first # mask 4 only: d_j = 1, a forced offset
            elif v in known:
                free.add(first)
            else:
                unknown_data.append(j)
        # For each shift only the largest nested coordinate subspace matters.
        groups[tuple(unknown_data)][shift]=free
    total=0
    for kinds in groups.values():
        if len(kinds)==1:
            total+=1<<len(next(iter(kinds.values())))
            continue
        # The only nonzero offset is the possible last, fixed ghost term.
        shifted=next(k for k in kinds if k is not None)
        large=kinds[shifted]
        small=kinds[None]
        assert small<=large
        total+=1<<len(large)
        if shifted not in large:
            total+=1<<len(small)
    return total


if __name__=='__main__':
    comparisons=0
    for mask in (2,4):
        for m in range(1,9):
            states=list(range(1<<m))
            valid=(1<<m)-1
            p=1<<(m//2).bit_length()
            for t in range(p):
                vals=[x>>(m-1) for x in states]
                for subset in range(1<<m):
                    obs=[k for k in range(m) if subset>>k&1]
                    rest=[k for k in range(m) if k not in obs]
                    assert count_responses(m-1,t,set(obs),mask)==classes(vals,obs,rest),(mask,m,t,obs)
                    comparisons+=1
                states=[(x^(((x<<1)&~(x<<2)) if mask==4 else (~(x<<1)&(x<<2))))&valid for x in states]
    print("All masked rules 2/4, all cut subsets, m<=8, times 0..P4(m)-1:",comparisons)
    for mask in (2,4):
        site=128
        t=63
        for name,known in [('first half',set(range(65))),('all even',set(range(0,129,2))),
                           ('all odd',set(range(1,129,2)))]:
            print("mask",mask,"m=129, t=63",name,count_responses(site,t,known,mask))
