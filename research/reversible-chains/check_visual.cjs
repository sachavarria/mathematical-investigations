// Exercise the actual model embedded in the self-contained study.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(__dirname + '/index.html', 'utf8').match(/<script id="math">([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({});
vm.runInContext(source + ';this.study = {advance, response}', context);
const { advance, response } = context.study;
let calls = 0, evolutions = 0;
for (let n = 4; n <= 7; n++) {
  const sites = Array.from({length:n}, (_, i) => i);
  for (let r = 0; r < 16; r++) for (const t of [0,1,3,7]) {
    const population = [];
    for (let x = 0; x < 2**n; x++) {
      const initial = sites.map(i => Math.floor(x/2**i)%2);
      let current = initial, actual = x;
      for (let j = 0; j < t; j++) {
        current = current.map((v,i) => v ^ (Math.floor(r/2**(2*(current[i-1]||0)+(current[i-2]||0)))%2));
        actual = advance(actual,n,r);
        assert.equal(actual,current.reduce((s,v,i)=>s+v*2**i,0));
        evolutions++;
      }
      const a = current.at(-1), b = current.at(-2);
      const odd = sites.filter(i => i%2);
      const answers = [a, a^b, 2*b+a, 2*initial.at(-1)+a,
        odd.reduce((s,i)=>s^current[i],0),
        odd.reduce((s,i)=>s^initial[i]^current[i],initial.at(-1))];
      population.push({initial,answers});
    }
    const k = Math.floor(n/2);
    const odds = sites.filter(i=>i%2), evens = sites.filter(i=>!(i%2));
    [sites,sites.slice().reverse(),evens.concat(odds),odds.concat(evens)].forEach((order,o)=>{
      for(let q=0;q<6;q++) {
        const rows = new Map();
        for(const {initial,answers} of population) {
          const key=order.slice(0,k).map(i=>initial[i]).join('');
          const suffix=order.slice(k).map(i=>initial[i]).join('');
          if(!rows.has(key)) rows.set(key,new Map());
          rows.get(key).set(suffix,answers[q]);
        }
        // Independent canonicalization by ordinary string order, invariant under the drawing's common Gray permutation.
        const classes=new Map();
        for (const row of rows.values()) {
          const signature=Array.from(row).sort((a,b)=>a[0].localeCompare(b[0])).map(a=>a[1]).join('');
          classes.set(signature,(classes.get(signature)||0)+1);
        }
        const hist=Array.from(classes.values()).sort((a,b)=>a-b);
        assert.deepEqual(Array.from(response(n,r,t,k,o,q),v=>v[1]).sort((a,b)=>a-b),hist);
        calls++;
      }
    });
  }
}
assert.equal(response(9,4,7,5,2,0).length,32);
assert.equal(response(9,4,7,4,3,0).length,5);
assert.equal(response(8,6,1,4,2,5).length,2);
assert.equal(response(8,14,1,4,2,5).length,16);
console.log('Cell evolution comparisons:',evolutions);
console.log('Residual class multiplicity histograms:',calls);
console.log('Nine-cell landmark: 32 even first, 5 odd first. Eight-cell change check: 2 versus 16.');
