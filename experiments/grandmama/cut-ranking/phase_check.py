"""End-to-end check against a literally concatenated Grandmama clock."""
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys
from collections import Counter
from check import words, orbit
from cut_rank import rank

def main(archive):
    sys.path.insert(0,str(archive))
    spec=spec_from_file_location("archived_decoder",archive/"decode.py")
    decoder=module_from_spec(spec)
    spec.loader.exec_module(decoder)
    decoder.ranks=rank
    print("order,windows")
    for n in range(1,8):
        mass=Counter(min(orbit(w)) for w in words(n))
        clock="".join(w[:mass[w]] for w in sorted(mass,key=lambda w:w[::-1]))
        for i in range(1<<n):
            w=(clock+clock)[i:i+n]
            assert decoder.decode(w)==i
        print(n,1<<n,sep=",")

if __name__=="__main__":
    main(Path(sys.argv[1]) if sys.argv[1:] else Path(__file__).resolve().parent.parent/"return-ranking")
