from __future__ import annotations

import streamlit.components.v1 as components


def stroop_component() -> None:
    components.html(r"""
<div><h3>Stroop Task</h3><p>Press R/G/B/Y for the ink color, not the word.</p><button onclick="startStroop()">Start</button><h1 id="word"></h1><p id="smsg"></p></div>
<script>
const items=[['RED','red','R'],['GREEN','green','G'],['BLUE','blue','B'],['YELLOW','gold','Y']]; let si=0, stStart=0, events=[];
function pick(){let w=items[Math.floor(Math.random()*4)], c=items[Math.floor(Math.random()*4)]; return {word:w[0], color:c[1], key:c[2], congruent:w[0]===c[0]};}
function show(){let t=pick(); window.current=t; document.getElementById('word').innerText=t.word; document.getElementById('word').style.color=t.color; stStart=performance.now();}
function startStroop(){si=0; events=[]; show();}
document.addEventListener('keydown', e=>{let k=e.key.toUpperCase(); if(!['R','G','B','Y'].includes(k) || !window.current)return; let rt=performance.now()-stStart; events.push({...window.current, pressed:k, correct:k===window.current.key, rt_ms:rt}); si++; if(si>=16){let acc=events.filter(x=>x.correct).length/events.length; let cong=events.filter(x=>x.congruent).map(x=>x.rt_ms); let incong=events.filter(x=>!x.congruent).map(x=>x.rt_ms); let avg=a=>a.reduce((x,y)=>x+y,0)/Math.max(1,a.length); document.getElementById('smsg').innerText='Done. Copy result: '+JSON.stringify({stroop_accuracy:acc, stroop_interference_ms:avg(incong)-avg(cong), stroop_events:events}); window.current=null;} else show();});
</script>
""", height=320)
