from __future__ import annotations

import streamlit.components.v1 as components


def stroop_component() -> None:
    components.html(r"""
<div class="card">
  <div class="title">🎨 Stroop Task</div>
  <p class="hint">Press <b>R/G/B/Y</b> for the <b>ink color</b>, not the word text.</p>
  <button class="btn" onclick="startStroop()">Start</button>
  <h1 id="word">READY</h1>
  <p id="smsg" class="msg">Press start to begin 16 trials.</p>
</div>
<style>
body { font-family: Inter, system-ui, sans-serif; }
.card { border:1px solid #e6eaf0; border-radius:14px; padding:14px; background:#fff; }
.title { font-size:18px; font-weight:700; margin-bottom:4px; }
.hint,.msg { color:#4b5563; }
.btn { background:#7c3aed; color:#fff; border:none; padding:10px 14px; border-radius:10px; cursor:pointer; font-weight:600; }
#word { margin:12px 0 8px; font-size:44px; letter-spacing:1px; min-height:56px; }
</style>
<script>
const items=[['RED','red','R'],['GREEN','green','G'],['BLUE','blue','B'],['YELLOW','goldenrod','Y']];
let si=0, stStart=0, events=[];
function pick(){let w=items[Math.floor(Math.random()*4)], c=items[Math.floor(Math.random()*4)]; return {word:w[0], color:c[1], key:c[2], congruent:w[0]===c[0]};}
function show(){let t=pick(); window.current=t; document.getElementById('word').innerText=t.word; document.getElementById('word').style.color=t.color; stStart=performance.now(); document.getElementById('smsg').innerText=`Trial ${si+1}/16`;}
function startStroop(){si=0; events=[]; show();}
document.addEventListener('keydown', e=>{let k=e.key.toUpperCase(); if(!['R','G','B','Y'].includes(k) || !window.current)return; let rt=performance.now()-stStart; events.push({...window.current, pressed:k, correct:k===window.current.key, rt_ms:rt}); si++; if(si>=16){let acc=events.filter(x=>x.correct).length/events.length; let cong=events.filter(x=>x.congruent).map(x=>x.rt_ms); let incong=events.filter(x=>!x.congruent).map(x=>x.rt_ms); let avg=a=>a.reduce((x,y)=>x+y,0)/Math.max(1,a.length); document.getElementById('smsg').innerText='Done ✅ Copy result JSON: '+JSON.stringify({stroop_accuracy:acc, stroop_interference_ms:avg(incong)-avg(cong), stroop_events:events}); window.current=null;} else show();});
</script>
""", height=320)
