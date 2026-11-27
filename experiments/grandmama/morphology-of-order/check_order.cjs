// Exercise the actual population and adjacency routines embedded in the instrument.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const source = html.match(/<script id="math">([\s\S]*?)<\/script>/)[1];
const {population, neighbours} = vm.runInNewContext(source + '\n;({population,neighbours})');
for (let n = 4; n <= 9; n++) {
  const db = population(n);
  const pairs = [];
  const keys = Object.keys(db.orders);
  for (const [i, key] of keys.entries()) {
    const words = db.orders[key];
    assert.equal(new Set(words).size, 2**n);
    assert.equal(neighbours(words, words), 2**n);
    for (const other of keys.slice(i + 1)) {
      const seen = new Set(words.map((w,j) => [w, words[(j+1)%words.length]].sort().join(':')));
      const second = db.orders[other];
      const shared = second.filter((w,j) => seen.has([w, second[(j+1)%second.length]].sort().join(':'))).length;
      assert.equal(neighbours(words, second), shared);
      pairs.push(key+'-'+other+'='+shared);
    }
  }
  const cycles = new Map;
  for (const w of db.words) {
    const {row,packet} = db.info.get(w);
    assert.equal(w.slice(1), db.orders.time[(db.rank.time.get(w)+1)%db.size].slice(0,-1));
    const b = packet.last[row];
    const lf = (b==='1' ? [...packet.last].filter(c=>c==='0').length : 0) + [...packet.last.slice(0,row)].filter(c=>c===b).length;
    assert.equal(packet.rows[lf], w.slice(-1)+w.slice(0,-1));
    assert.equal(packet.rows[row],w);
    const bits=[...packet.root];
    assert.equal(packet.frontier, bits.filter((bit,i)=>bit==='1'&&bits[(i+1)%bits.length]==='0').length);
    const stable=packet.rows.map(r=>packet.rows.indexOf(r.slice(-1)+r.slice(0,-1)));
    const peak=Math.max(...stable.map((_,cut)=>stable.slice(0,cut+1).filter(x=>x>cut).length));
    assert.equal(peak,packet.frontier);
    if(cycles.has(packet.last))assert.equal(cycles.get(packet.last),packet.root);
    cycles.set(packet.last,packet.root);
  }
  console.log('n='+n, 'windows='+db.size, 'packets='+cycles.size, ...pairs);
}
