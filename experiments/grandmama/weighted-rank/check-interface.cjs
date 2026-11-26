// Execute the actual standalone page script with minimal text and band elements.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, 'Index-Study.html'), 'utf8');
function element() {
  return {style:{}, children:[], replaceChildren(){this.children=[]},
    setAttribute(){}, append(...v){this.children.push(...v)}};
}
const nodes = new Map();
const dom = {createElement: element, getElementById(id){
  if (!nodes.has(id)) nodes.set(id,element());
  return nodes.get(id);
}};
dom.getElementById('depth').value=4;
dom.getElementById('word').value='00010111';
const context = vm.createContext({document:dom});
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
assert.match(dom.getElementById('answer').textContent,/171 = 155 stored \+ 16 counted/);
for(let n=2;n<=8;n++){
  const masses=new Map();
  for(let i=0;i<2**n;i++){
    const w=i.toString(2).padStart(n,'0');
    const rep=Array.from(w,(_,j)=>w.slice(j)+w.slice(0,j)).sort()[0];
    masses.set(rep,(masses.get(rep)||0)+1);
  }
  for(let k=0;k<=n;k++){
    let phase=0;
    const index=context.prepare(n,k);
    for(let j=0;j<2**n;j++){
      const w=context.candidate(j,n), r=context.query(index,w);
      assert.equal(r.saved+r.extra,phase);
      assert.equal(r.key-r.start,j%2**(n-k));
      phase+=masses.get(w)||0;
    }
  }
}
dom.getElementById('clear').onclick();
dom.getElementById('run').onclick();
dom.getElementById('run').onclick();
assert.equal(dom.getElementById('ledger').children[1].textContent,0);
console.log('Passed all thresholds and index depths for orders 2 through 8, plus cache reset and reuse.');
