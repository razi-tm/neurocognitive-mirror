from __future__ import annotations

import streamlit.components.v1 as components


def reaction_time_component() -> None:
    components.html(r"""
<div id="rt-card" class="card">
  <div class="title">⚡ Simple Reaction Time</div>
  <p class="hint">Wait for GO, then press <b>Space</b> or click anywhere in this card.</p>
  <button class="btn" onclick="startRT()">Start</button>
  <div id="rtmsg" class="status">Ready.</div>
</div>

<style>
body { font-family: Inter, system-ui, sans-serif; }
.card { border:1px solid #e6eaf0; border-radius:14px; padding:14px; background:#fff; }
.title { font-size:18px; font-weight:700; margin-bottom:4px; }
.hint { color:#4b5563; margin:6px 0 10px; }
.btn { background:#0f766e; color:#fff; border:none; padding:10px 14px; border-radius:10px; cursor:pointer; font-weight:600; }
.status { margin-top:12px; padding:10px; border-radius:10px; background:#f8fafc; font-weight:600; }
.go { background:#dcfce7 !important; color:#166534; }
.wait { background:#fef3c7 !important; color:#92400e; }
</style>

<script>
let rtStart=0, armed=false, rts=[];
const card=document.getElementById('rt-card');
const msg=document.getElementById('rtmsg');
function startRT(){rts=[]; msg.innerText='Starting...'; nextRT();}
function nextRT(){
  armed=false;
  msg.className='status wait';
  msg.innerText='Wait...';
  setTimeout(()=>{
    armed=true;
    rtStart=performance.now();
    msg.className='status go';
    msg.innerText='GO!';
  }, 700+Math.random()*1800);
}
function hit(){
  if(!armed) return;
  const rt=performance.now()-rtStart;
  rts.push(rt);
  armed=false;
  if(rts.length>=8){
    msg.className='status';
    msg.innerText='Done ✅ Copy result JSON: '+JSON.stringify({reaction_time_ms:rts.reduce((a,b)=>a+b,0)/rts.length, reaction_events:rts});
  } else { nextRT(); }
}
document.addEventListener('keydown', e=>{if(e.code==='Space')hit();});
card.addEventListener('click', hit);
</script>
""", height=230)
