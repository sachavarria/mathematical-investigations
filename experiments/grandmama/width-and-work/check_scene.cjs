// Check the calculation actually embedded in the static scene.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const html = fs.readFileSync(path.join(__dirname, "index.html"),"utf8");
const code = html.match(/<script id="math">([\s\S]*?)<\/script>/)[1];
const {cutCensus,cutProfile} = vm.runInNewContext(code+"\n;({cutCensus,cutProfile})");

let cases=0, columns=0;
for(let p=1;p<=9;p++) {
  const words=Array.from({length:2**p},(_,j)=>j.toString(2).padStart(p,"0"));
  const primitive=new Map;
  for(const w of words) {
    const rows=Array.from({length:p},(_,j)=>w.slice(j)+w.slice(0,j)).sort();
    if(rows[0]!==w || new Set(rows).size!==p)continue;
    primitive.set(rows.map(r=>r.at(-1)).join(""),[...w].reverse().join(""));
  }
  const checked=new Set;
  for(const b of primitive.keys()) {
    let inversions=0;
    for(let u=0;u<p;u++)for(let v=u+1;v<p;v++)inversions+=(b[u]==="1"&&b[v]==="0");
    assert.equal(cutProfile(b).reduce((s,x)=>s+x,0),inversions);
    assert.equal(inversions%2,(p-1)%2);
    for(let i=0;i<=p;i++) {
      const prefix=b.slice(0,i),z=b.split("0").length-1,key=z+" "+prefix;
      if(checked.has(key))continue;
      checked.add(key);
      const possible=words.filter(x=>x.startsWith(prefix)&&x.split("0").length-1===z);
      const passing=possible.filter(x=>primitive.has(x));
      for(const query of ["","10","101","11","111"].filter(x=>x.length<=p)) {
        const census=cutCensus(b,i,query);
        assert.equal(census.rows.length,possible.length);
        assert.equal(census.connected,passing.length);
        assert.equal(census.yes,passing.filter(x=>primitive.get(x).startsWith(query)).length);
        const reads=possible.reduce((total,x)=>{
          const occurrences=[...x].map((bit,row)=>({bit,row})).sort((u,v)=>u.bit.localeCompare(v.bit)||u.row-v.row);
          const indices=occurrences.map(o=>o.row);
          let row=0,length=0;
          do{row=indices.indexOf(row);length++}while(row!==0);
          return total+length;
        },0);
        assert.equal(census.reads,reads);
        cases++;columns+=possible.length;
      }
    }
  }
}
console.log("Distinct prefix/density/query comparisons",cases,"columns across comparisons",columns);
for(const q of ["101","111"])for(let i=0;i<=8;i++){
  const r=cutCensus("10011010",i,q);
  console.log(q,i,r.rows.length,r.connected,r.yes,r.reads);
}
