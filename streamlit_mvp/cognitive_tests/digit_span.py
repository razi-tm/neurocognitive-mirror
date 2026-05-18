from __future__ import annotations

import streamlit.components.v1 as components


def digit_span_component() -> None:
    components.html(r"""
<div id="ds"><h3>Digit Span</h3><p id="prompt">Press Start. Type the digits you saw and press Enter.</p><button onclick="startDS()">Start</button><input id="answer" autofocus /></div>
<script>
let dsLevel=4, dsSeq='', dsStart=0, dsResults=[];
function makeSeq(n){return Array.from({length:n},()=>Math.floor(Math.random()*10)).join('');}
function trial(){dsSeq=makeSeq(dsLevel); document.getElementById('prompt').innerText=dsSeq; document.getElementById('answer').value=''; setTimeout(()=>{document.getElementById('prompt').innerText='Enter sequence'; dsStart=performance.now();}, 900+dsLevel*180);}
function startDS(){dsLevel=4; dsResults=[]; trial();}
document.getElementById('answer').addEventListener('keydown', e=>{if(e.key==='Enter'){let rt=performance.now()-dsStart; let ok=e.target.value.trim()===dsSeq; dsResults.push({level:dsLevel,correct:ok,rt_ms:rt}); dsLevel=Math.max(3, dsLevel+(ok?1:-1)); if(dsResults.length>=7){document.getElementById('prompt').innerText='Done. Copy result: '+JSON.stringify({digit_span:Math.max(...dsResults.filter(r=>r.correct).map(r=>r.level),0), digit_span_events:dsResults});} else trial();}});
</script>
""", height=260)
