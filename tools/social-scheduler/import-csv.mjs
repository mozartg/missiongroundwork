import fs from 'node:fs';
import path from 'node:path';
const [,,input='content/social-queue.csv',output='content/social-queue.json']=process.argv;
function parseCSV(s){const rows=[];let row=[],cell='',q=false;for(let i=0;i<s.length;i++){const c=s[i];if(q){if(c==='"'&&s[i+1]==='"'){cell+='"';i++;}else if(c==='"')q=false;else cell+=c;}else if(c==='"')q=true;else if(c===','){row.push(cell);cell='';}else if(c==='\n'){row.push(cell.replace(/\r$/,''));rows.push(row);row=[];cell='';}else cell+=c;}if(cell||row.length){row.push(cell);rows.push(row);}return rows;}
const rows=parseCSV(fs.readFileSync(input,'utf8'));const headers=rows.shift().map(x=>x.trim());
const posts=rows.filter(r=>r.some(Boolean)).map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]??'']))).map(p=>Object.fromEntries(Object.entries(p).filter(([,v])=>v!=='')));
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(posts,null,2)+'\n');console.log(`Imported ${posts.length} posts to ${output}`);
