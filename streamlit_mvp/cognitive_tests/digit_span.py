from __future__ import annotations

import streamlit.components.v1 as components


def digit_span_component() -> None:
    components.html(r"""
<div class="card">
  <div class="title">🧠 Digit Span</div>
  <p class="hint">Memorize the sequence, then type it and press <b>Enter</b>.</p>
  <div id="prompt" class="prompt">Press Start when ready.</div>
  <div class="row">
    <button class="btn" onclick="startDS()">Start</button>
    <input id="answer" placeholder="Type digits here" autocomplete="off" />
  </div>
  <p id="msg" class="msg"></p>
</div>

<style>
body { font-family: Inter, system-ui, sans-serif; }
.card { border:1px solid #e6eaf0; border-radius:14px; padding:14px; background:#fff; }
.title { font-size:18px; font-weight:700; margin-bottom:4px; }
.hint,.msg { color:#4b5563; margin:6px 0; }
.prompt { font-size:28px; font-weight:700; letter-spacing:4px; text-align:center; padding:14px 8px; background:#f8fafc; border-radius:10px; min-height:50px; }
.row { display:flex; gap:10px; margin-top:12px; }
.btn { background:#2563eb; color:#fff; border:none; padding:10px 14px; border-radius:10px; cursor:pointer; font-weight:600; }
input { flex:1; padding:10px 12px; border-radius:10px; border:1px solid #cbd5e1; }
</style>

<script>
let dsLevel=4, dsSeq='', dsStart=0, dsResults=[];
function makeSeq(n){return Array.from({length:n},()=>Math.floor(Math.random()*10)).join('');}
function trial(){
  dsSeq=makeSeq(dsLevel);
  document.getElementById('prompt').innerText=dsSeq;
  document.getElementById('answer').value='';
  document.getElementById('msg').innerText='Watch carefully...';
  setTimeout(()=>{
    document.getElementById('prompt').innerText='Enter sequence';
    dsStart=performance.now();
    document.getElementById('answer').focus();
    document.getElementById('msg').innerText=`Level ${dsLevel} · press Enter to submit`;
  }, 900+dsLevel*180);
}
function startDS(){dsLevel=4; dsResults=[]; document.getElementById('msg').innerText='Started'; trial();}
document.getElementById('answer').addEventListener('keydown', e=>{if(e.key==='Enter'){
  let rt=performance.now()-dsStart;
  let ok=e.target.value.trim()===dsSeq;
  dsResults.push({level:dsLevel,correct:ok,rt_ms:rt});
  dsLevel=Math.max(3, dsLevel+(ok?1:-1));
  if(dsResults.length>=7){
    const payload={digit_span:Math.max(...dsResults.filter(r=>r.correct).map(r=>r.level),0), digit_span_events:dsResults};
    document.getElementById('prompt').innerText='Done ✅';
    document.getElementById('msg').innerText='Copy result JSON: '+JSON.stringify(payload);
  } else { trial(); }
}});
</script>
""", height=280)
