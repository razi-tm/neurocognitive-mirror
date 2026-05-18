from __future__ import annotations

import streamlit.components.v1 as components


def reaction_time_component() -> None:
    components.html(r"""
<div><h3>Simple Reaction Time</h3><button id="rtbtn" onclick="startRT()">Start</button><p id="rtmsg">Wait for green, then press Space or click.</p></div>
<script>
let rtStart=0, armed=false, rts=[];
function startRT(){rts=[]; nextRT();}
function nextRT(){armed=false; document.body.style.background=''; document.getElementById('rtmsg').innerText='Wait...'; setTimeout(()=>{armed=true; rtStart=performance.now(); document.body.style.background='#d1fae5'; document.getElementById('rtmsg').innerText='GO';}, 700+Math.random()*1800);}
function hit(){if(!armed)return; const rt=performance.now()-rtStart; rts.push(rt); armed=false; document.body.style.background=''; if(rts.length>=8){document.getElementById('rtmsg').innerText='Done. Copy result: '+JSON.stringify({reaction_time_ms:rts.reduce((a,b)=>a+b,0)/rts.length, reaction_events:rts});} else nextRT();}
document.addEventListener('keydown', e=>{if(e.code==='Space')hit();}); document.addEventListener('click', hit);
</script>
""", height=230)
