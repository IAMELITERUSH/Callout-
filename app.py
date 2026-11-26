#!/usr/bin/env python3
"""
Callout - a voice-activated score counter (1 to 5 counters).

Run it on your computer:   python app.py
On Vercel:                 push to GitHub; Vercel serves the `app` below.

No extra packages needed. Use Chrome or Safari for voice control.
"""

import webbrowser
from wsgiref.simple_server import WSGIRequestHandler, make_server

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1">
<title>Callout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html,body{height:100%;background:#070912;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
button,input,select{font:inherit;color:inherit}
button{cursor:pointer;border:0;touch-action:manipulation;user-select:none;-webkit-user-select:none}
[hidden]{display:none!important}
.screen{height:100vh;height:100dvh;display:flex;flex-direction:column;
  padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
#home,#rules{background:radial-gradient(circle at 8% 10%,#1f6fffa6,transparent 42%),radial-gradient(circle at 96% 44%,#8b3dff73,transparent 38%),radial-gradient(circle at 25% 96%,#ff3b4d8c,transparent 44%),#070912}

/* Liquid Glass: see-through tint, blur, bright rim and a soft springy press */
.glass{--c:rgba(255,255,255,.12);position:relative;isolation:isolate;border-radius:999px;font-weight:650;
  background:var(--c);border:1px solid rgba(255,255,255,.28);
  -webkit-backdrop-filter:blur(16px) saturate(190%);backdrop-filter:blur(16px) saturate(190%);
  box-shadow:inset 1.5px 1.5px 1px -.5px rgba(255,255,255,.75),inset -1.5px -1.5px 1px -.5px rgba(255,255,255,.45),
    inset 0 0 14px rgba(255,255,255,.18),0 8px 24px rgba(0,0,0,.28);
  text-shadow:0 1px 3px rgba(0,0,0,.35);transition:transform .35s cubic-bezier(.3,2.2,.5,1),filter .2s}
.glass::after{content:"";position:absolute;inset:1px;border-radius:inherit;z-index:-1;pointer-events:none;
  background:linear-gradient(165deg,rgba(255,255,255,.38),rgba(255,255,255,.04) 38%,transparent 62%,rgba(255,255,255,.16))}
.glass:active{transform:scale(.93);filter:brightness(1.18)}
.primary{--c:rgba(31,111,255,.68)}
.pane{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);
  -webkit-backdrop-filter:blur(24px) saturate(170%);backdrop-filter:blur(24px) saturate(170%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 14px 36px rgba(0,0,0,.25)}

/* Start screen */
#home{align-items:center;justify-content:center;gap:18px;text-align:center}
.logo{width:108px;height:108px;border-radius:30px;display:grid;place-items:center;
  background:linear-gradient(90deg,#1f6fff 0 50%,#ff3b4d 50% 100%);box-shadow:0 20px 50px #0009,inset 0 1px 2px #fffc,inset 0 0 22px #fff5}
.logo svg{width:58px;height:58px}
h1{font-size:56px;font-weight:800;letter-spacing:-2px}
.tag{color:#c3c9de;margin-top:-12px;margin-bottom:20px}
.menu{width:min(320px,84vw);display:flex;flex-direction:column;gap:14px}
.menu .glass{padding:18px;font-size:19px}

/* Rules page */
header{display:flex;align-items:center;gap:14px;padding:12px 16px}
header h2{font-size:28px;letter-spacing:-.5px}
.back{padding:10px 18px}
.scroll{flex:1;overflow-y:auto;padding:4px 16px 20px;width:100%;max-width:620px;margin:0 auto}
details{border-radius:26px;margin-bottom:12px}
summary{list-style:none;cursor:pointer;padding:18px 20px;font-weight:700;font-size:18px;display:flex;justify-content:space-between}
summary::-webkit-details-marker{display:none}
summary::after{content:"▾";color:#b4bcd8;transition:transform .2s}
details[open] summary::after{transform:rotate(180deg)}
.body{padding:0 20px 18px;display:flex;flex-direction:column;gap:13px}
label.row{display:flex;justify-content:space-between;align-items:center;gap:12px}
select,input{background:rgba(0,0,0,.34);border:1px solid rgba(255,255,255,.2);border-radius:14px;padding:11px 13px;font-size:16px;min-width:0}
option{background:#171b2c}
label.row select,label.row input{width:55%}
.name{display:flex;align-items:center;gap:10px}
.dot{width:22px;height:22px;border-radius:50%;flex:none;box-shadow:inset 0 1px 2px #fffa}
.name input{flex:1}
.hint{color:#b4bcd8;font-size:13px;line-height:1.45}
.say{padding:13px}
.bar{padding:12px 16px;width:100%;max-width:620px;margin:0 auto}
.bar .glass{width:100%;padding:17px;font-size:19px}
.error{color:#ffb0b6;font-size:14px;text-align:center;min-height:18px;margin-bottom:5px}

/* Game: counters always side by side, split evenly */
#status{display:flex;justify-content:space-between;gap:8px;padding:8px 14px;font-size:13px;color:#c3c9de;min-height:34px}
#heard{overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
#info{white-space:nowrap}
#board{flex:1;min-height:0;display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);grid-template-rows:minmax(0,1fr);gap:5px;padding:0 5px}
.side{container-type:size;position:relative;border-radius:30px;overflow:hidden;min-width:0;min-height:0;
  background:radial-gradient(circle at 20% 8%,color-mix(in srgb,var(--p) 55%,#fff),transparent 55%),
    radial-gradient(circle at 85% 72%,color-mix(in srgb,var(--p) 60%,#fff),transparent 45%),
    linear-gradient(170deg,var(--p),color-mix(in srgb,var(--p) 68%,#000));box-shadow:inset 0 1px 1px #fff7}
.side.flash{animation:flash .45s}
@keyframes flash{40%{filter:brightness(1.35)}}
.inner{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3cqh;padding:2cqh 5cqw}
.inner>*{flex:none}
.who{font-weight:700;font-size:clamp(14px,min(7cqh,13cqw),34px);max-width:100%;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;line-height:1.2}
.score{font-family:ui-rounded,"SF Pro Rounded",-apple-system,"Segoe UI",Roboto,sans-serif;font-weight:800;line-height:.95;
  font-variant-numeric:tabular-nums;font-size:min(36cqh,calc(135cqw / var(--len)));text-shadow:0 6px 20px #0004}
.pm{display:flex;gap:min(5cqw,16px);width:min(92cqw,340px)}
.pm .glass{flex:1;height:clamp(52px,18cqh,92px);font-size:clamp(30px,10cqh,50px);line-height:1}
/* narrow columns: plus on top, minus below */
@container (max-width:150px){
  .pm{flex-direction:column-reverse;width:100%;gap:2cqh}
  .pm .glass{flex:none;width:100%;height:clamp(44px,14cqh,72px)}
}
nav{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;padding:10px 8px;width:100%;max-width:640px;margin:0 auto}
nav .glass{height:52px;font-size:13px}
#mic.on{--c:rgba(20,200,110,.7);animation:pulse 1.6s infinite}
@keyframes pulse{50%{box-shadow:0 0 0 6px #13c46f44,inset 1.5px 1.5px 1px -.5px #fffa}}

/* Pop-ups */
.modal{position:fixed;inset:0;background:#0007;display:grid;place-items:center;padding:20px;z-index:10}
.card{border-radius:36px;padding:24px;width:min(380px,100%);max-height:86vh;overflow:auto;display:flex;flex-direction:column;gap:12px;text-align:center;background:rgba(24,28,48,.62)}
.card h2{font-size:28px;overflow-wrap:anywhere}
.card .glass{padding:14px;flex:none}
.card ul{text-align:left;list-style:none;font-size:15px;line-height:1.9}
</style>
</head>
<body>

<section id="home" class="screen">
  <div class="logo"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round">
    <rect x="9" y="2.5" width="6" height="11" rx="3" fill="#fff"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/></svg></div>
  <h1>Callout</h1>
  <p class="tag">Say it. Score it.</p>
  <div class="menu">
    <button class="glass primary" id="goNew">New Game</button>
    <button class="glass" id="goResume">Resume Game</button>
    <button class="glass" id="goHelp">Voice Commands</button>
  </div>
</section>

<section id="rules" class="screen" hidden>
  <header><button class="glass back" id="rulesBack">Back</button><h2>Rules</h2></header>
  <div class="scroll">
    <details class="pane" open><summary>Counters &amp; names</summary><div class="body">
      <label class="row">How many counters<select id="count"></select></label>
      <div id="names" class="body" style="padding:0"></div>
    </div></details>

    <details class="pane" open><summary>Score</summary><div class="body">
      <label class="row">Starting at<input id="start" type="number" inputmode="numeric" step="1"></label>
      <label class="row">Until<input id="target" type="number" inputmode="numeric" step="1" placeholder="No limit"></label>
      <button class="glass say" id="sayRules">Speak the rules</button>
      <p class="hint" id="sayHint">Say "until 20" or "starting at 5". If Until is lower than Starting at, the game counts down.</p>
      <label class="row">Points per tap<select id="step"></select></label>
      <label class="row">Below zero<select id="negative"></select></label>
      <label class="row">Win by 2<select id="winBy2"></select></label>
    </div></details>

    <details class="pane"><summary>Sound &amp; screen</summary><div class="body">
      <label class="row">Voice control<select id="voice"></select></label>
      <label class="row">Read score aloud<select id="announce"></select></label>
      <label class="row">Tap sounds<select id="sound"></select></label>
      <label class="row">Vibration<select id="vibrate"></select></label>
      <label class="row">Keep screen on<select id="awake"></select></label>
      <label class="row">Game timer<select id="timer"></select></label>
    </div></details>
  </div>
  <div class="bar"><div class="error" id="error"></div><button class="glass primary" id="startGame">Start Game</button></div>
</section>

<section id="game" class="screen" hidden>
  <div id="status"><span id="heard">Tap Mic to use voice</span><span id="info"></span></div>
  <div id="board"></div>
  <nav>
    <button class="glass" id="home2">Home</button>
    <button class="glass" id="undo">Undo</button>
    <button class="glass" id="mic">Mic off</button>
    <button class="glass" id="swap">Swap</button>
    <button class="glass" id="more">More</button>
  </nav>
</section>

<div class="modal" id="modal" hidden><div class="card pane" id="card"></div></div>

<script>
"use strict";
const $ = id => document.getElementById(id);
const COLORS = [
  {name:"Blue",  panel:"#1565f0", btn:"rgba(255,38,56,.78)"},
  {name:"Red",   panel:"#e0212f", btn:"rgba(24,104,255,.78)"},
  {name:"Green", panel:"#0f8a52", btn:"rgba(232,48,138,.76)"},
  {name:"Orange",panel:"#e46a05", btn:"rgba(30,82,225,.76)"},
  {name:"Purple",panel:"#6d3fe0", btn:"rgba(235,166,0,.76)"}
];
const DEFAULTS = {count:2,names:["","","","",""],start:0,target:20,step:1,negative:0,winBy2:0,
  voice:1,announce:1,sound:1,vibrate:1,awake:1,timer:1};
const ONOFF = [[1,"On"],[0,"Off"]];
const OPTIONS = {
  count:[1,2,3,4,5].map(n=>[n,String(n)]),
  step:[1,2,3,5,10].map(n=>[n,"+"+n]),
  negative:[[0,"Not allowed"],[1,"Allowed"]],
  winBy2:[[0,"Off"],[1,"On"]],
  voice:ONOFF,announce:ONOFF,sound:ONOFF,vibrate:ONOFF,awake:ONOFF,timer:ONOFF
};

/* ---------- saved on this device: your last rules and any unfinished game ---------- */
let cfg = {...DEFAULTS, names:[...DEFAULTS.names]}, G = null, undoStack = [];
try{ const d = JSON.parse(localStorage.getItem("callout.v3")); if(d){ cfg = {...cfg,...d.cfg}; G = d.G; undoStack = d.undo || []; } }catch(e){}
function save(){ try{ localStorage.setItem("callout.v3",JSON.stringify({cfg,G,undo:undoStack.slice(-40)})); }catch(e){} }

/* ---------- voice command reader ---------- */
const ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(" ");
const TENS = {twenty:20,thirty:30,forty:40,fifty:50,sixty:60,seventy:70,eighty:80,ninety:90};
function wordsToDigits(words){
  const out=[]; let n=null, last="";
  const flush=()=>{ if(n!==null) out.push(String(n)); n=null; last=""; };
  for(const w of words){
    const o=ONES.indexOf(w), t=TENS[w];
    if(w==="hundred" && n!==null && n<10){ n*=100; last="h"; }
    else if(w==="hundred" && n===null){ n=100; last="h"; }
    else if(t!==undefined){ if(last==="h") n+=t; else { flush(); n=t; } last="t"; }
    else if(o>=0){
      if(last==="h" || (last==="t" && o>0 && o<10)) n+=o; else { flush(); n=o; }
      last="o";
    } else { flush(); out.push(w); }
  }
  flush(); return out;
}
function clean(text){
  let s = text.toLowerCase().replace(/['’]/g,"").replace(/[^\p{L}\p{N}\s]/gu," ").trim();
  s = s.replace(/\b(points?) (four|fore|4|two|too|2)\b(?! points?)/g,"$1 for");
  return wordsToDigits(s.split(/\s+/)).join(" ");
}
function distance(a,b){
  let prev=[...Array(b.length+1).keys()];
  for(let i=1;i<=a.length;i++){
    const row=[i];
    for(let j=1;j<=b.length;j++) row[j]=Math.min(prev[j]+1,row[j-1]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1));
    prev=row;
  }
  return prev[b.length];
}
const KEYWORDS = new Set("point points for from to add plus minus take remove subtract deduct score scores a an and".split(" "));
function findPlayer(words,names){
  const found=[];
  names.forEach((name,i)=>{
    [[clean(name),false],[COLORS[i].name.toLowerCase(),true]].forEach(([target,isColor])=>{
      const len=target.split(" ").length;
      for(let k=0;k+len<=words.length;k++){
        const piece=words.slice(k,k+len).join(" "), d=distance(piece,target);
        const allowed = isColor || target.length<3 ? 0 : target.length<=5 ? 1 : 2;
        if(d<=allowed && (d===0 || !KEYWORDS.has(piece))) found.push({i,score:d+(isColor?.5:0),k,len});
      }
    });
  });
  found.sort((a,b)=>a.score-b.score || b.len-a.len);
  if(!found.length) return null;
  if(found.some(f=>f.i!==found[0].i && f.score===found[0].score)) return null;
  return found[0];
}
function parseCommand(text,names,step){
  const s=clean(text), words=s.split(" ");
  if(/\b(undo|go back)\b/.test(s)) return {type:"undo"};
  if(/\b(stop listening|mic off)\b/.test(s)) return {type:"stop"};
  if(/\bnext (match|game)\b/.test(s)) return {type:"next"};
  if(/\breset (the )?(game|scores?)\b/.test(s)) return {type:"reset"};
  if(/^(whats|what is|say|read|tell me) the score$/.test(s)) return {type:"say"};
  const minus=/\b(minus|subtract|remove|take|deduct)\b/.test(s);
  const plus=/\b(points?|plus|add|scores?)\b/.test(s);
  if(!minus && !plus) return null;
  let who=findPlayer(words,names);
  if(!who && names.length===1) who={i:0,k:0,len:0};
  if(!who) return null;
  const rest=words.filter((_,k)=>k<who.k || k>=who.k+who.len);
  const num=rest.find(w=>/^\d+$/.test(w));
  const amount=num===undefined?step:Number(num);
  if(amount<1 || amount>10000) return null;
  return {type:"score",player:who.i,delta:minus?-amount:amount};
}
function parseRules(text){
  const s=clean(text), out={};
  const a=s.match(/\b(?:start|starts|starting)(?: (?:at|from|with))? (\d+)/);
  const b=s.match(/\b(?:until|till|til|up to|play to|playing to|first to|go to) (\d+)/);
  if(a) out.start=Number(a[1]);
  if(b) out.target=Number(b[1]);
  return out;
}

/* ---------- screens ---------- */
function show(id){
  ["home","rules","game"].forEach(s=>$(s).hidden = s!==id);
  $("goResume").hidden = !G;
  if(id!=="game"){ stopListening(); hush(); releaseWake(); }
}
function popup(title,html,buttons){
  const c=$("card"); c.innerHTML="";
  const h=document.createElement("h2"); h.textContent=title; c.appendChild(h);
  if(html){ const d=document.createElement("div"); d.innerHTML=html; c.appendChild(d); }
  for(const [label,fn,color] of buttons){
    const b=document.createElement("button"); b.className="glass"; b.textContent=label;
    if(color) b.style.setProperty("--c",color);
    b.onclick=()=>{ $("modal").hidden=true; fn&&fn(); }; c.appendChild(b);
  }
  $("modal").hidden=false;
}
const esc = t => String(t).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));
function help(){
  popup("Voice commands",`<ul><li>"Point for Mark"</li><li>"Add 3 to Mark"</li><li>"Minus point Mark"</li>
  <li>"Point for blue"</li><li>"What's the score"</li><li>"Undo"</li><li>"Next match" (after a win)</li><li>"Reset game"</li><li>"Stop listening"</li></ul>
  <p class="hint">Use the names you typed. Pause briefly between commands.</p>`,[["Got it",null,"rgba(31,111,255,.75)"]]);
}

/* ---------- rules page ---------- */
const NUMBERS=["start","target"];
for(const [id,opts] of Object.entries(OPTIONS))
  for(const [v,l] of opts) $(id).add(new Option(l,v));
function fillRules(){
  for(const id of Object.keys(OPTIONS)) $(id).value=cfg[id];
  for(const id of NUMBERS) $(id).value=cfg[id]??"";
  drawNames(); $("error").textContent="";
}
function drawNames(){
  const box=$("names"); box.innerHTML="";
  for(let i=0;i<cfg.count;i++){
    const row=document.createElement("div"); row.className="name";
    row.innerHTML=`<span class="dot" style="background:${COLORS[i].panel}"></span>`;
    const inp=document.createElement("input"); inp.maxLength=18; inp.value=cfg.names[i]||"";
    inp.placeholder=`${COLORS[i].name} name`; inp.setAttribute("aria-label",inp.placeholder);
    inp.oninput=()=>{ cfg.names[i]=inp.value; save(); };
    row.appendChild(inp); box.appendChild(row);
  }
}
for(const id of Object.keys(OPTIONS)) $(id).onchange=e=>{
  cfg[id]=Number(e.target.value);
  if(id==="count") drawNames();
  save();
};
for(const id of NUMBERS) $(id).oninput=e=>{
  const v=e.target.value.trim();
  cfg[id] = v==="" ? (id==="start"?0:null) : Math.trunc(Number(v));
  save();
};
function startGame(){
  const {start,target}=cfg, err=m=>$("error").textContent=m;
  if(target!==null && target===start) return err("Starting at and Until must be different.");
  const names=Array.from({length:cfg.count},(_,i)=>(cfg.names[i]||"").trim()||COLORS[i].name);
  if(new Set(names.map(clean)).size!==names.length) return err("Give each counter a different name.");
  if(names.some(n=>!clean(n))) return err("Names need at least one letter or number.");
  G={rules:{...cfg,names:[...cfg.names]},names,scores:names.map(()=>start),order:names.map((_,i)=>i),winner:null,seconds:0};
  undoStack=[]; save(); openGame();
}
function openGame(){
  show("game"); render(); wake();
  speak(scoreCall());
  if(G.rules.voice) startListening(); else { stopListening(); note("Voice is off. Tap Mic to turn it on"); }
  if(G.winner!==null) winnerPopup();
}
const scoreCall=()=>G.names.map((n,i)=>`${n} ${G.scores[i]}`).join(", ");

/* ---------- scoring ---------- */
const snapshot=()=>{ undoStack.push(JSON.stringify(G)); if(undoStack.length>200) undoStack.shift(); };
function findWinner(){
  const r=G.rules, t=r.target; if(t===null) return -1;
  const down=t<r.start;
  return G.scores.findIndex((s,i)=>{
    if(down) return s<=t;
    if(s<t) return false;
    if(!r.winBy2 || G.scores.length<2) return true;
    return s-Math.max(...G.scores.filter((_,j)=>j!==i))>=2;
  });
}
function change(i,delta){
  if(!G || G.winner!==null) return false;
  const r=G.rules, t=r.target, down=t!==null && t<r.start;
  let next=G.scores[i]+delta;
  if(down){
    if(next<t){ const m=`Bust. ${G.names[i]} can't go below ${t}`; note(m); speak(`${m}. ${scoreCall()}`); return false; }
    next=Math.min(next,r.start);
  } else if(!r.negative) next=Math.max(next,Math.min(0,r.start));
  if(next===G.scores[i]) return false;
  snapshot();
  const up=next>G.scores[i]; G.scores[i]=next;
  const w=findWinner(); if(w>=0){ G.winner=w; undoStack=[]; }
  save(); render();
  const el=document.querySelector(`.side[data-i="${i}"]`); if(el) el.classList.add("flash");
  feedback(up);
  if(w>=0){ speak(`${G.names[w]} wins. ${scoreCall()}`); winnerPopup(); }
  else speak(scoreCall());
  return true;
}
function undo(){
  if(G && G.winner!==null) return;
  if(!undoStack.length) return note("Nothing to undo");
  const secs=G.seconds; G=JSON.parse(undoStack.pop()); G.seconds=secs;
  save(); render(); note("Undone"); speak(`Undone. ${scoreCall()}`);
}
function reset(){
  snapshot(); G.scores=G.names.map(()=>G.rules.start); G.seconds=0;
  save(); render(); note("Reset. Say undo to bring it back"); speak(`Reset. ${scoreCall()}`);
}
/* The match is over: go back to the rules page, filled in exactly as last time. */
function leaveMatch(screen){
  if(!G) return;
  cfg={...G.rules,names:[...G.rules.names]}; G=null; undoStack=[]; save();
  $("modal").hidden=true;
  if(screen==="rules") fillRules();
  show(screen);
}
const nextMatch=()=>leaveMatch("rules");
function winnerPopup(){
  const tally=G.names.map((n,i)=>`${esc(n)}: ${G.scores[i]}`).join("<br>");
  popup(`${G.names[G.winner]} wins!`,tally,[["Next Match",nextMatch,"rgba(31,111,255,.75)"],["Home",()=>leaveMatch("home")]]);
}

function render(){
  const r=G.rules, board=$("board"); board.innerHTML="";
  for(const i of G.order){
    const c=COLORS[i], el=document.createElement("div");
    el.className="side"; el.dataset.i=i; el.style.setProperty("--p",c.panel);
    el.innerHTML=`<div class="inner"><div class="who">${esc(G.names[i])}</div>
      <div class="score" style="--len:${Math.max(2,String(G.scores[i]).length)}">${G.scores[i]}</div>
      <div class="pm"><button class="glass" style="--c:${c.btn}" data-d="-1">−</button>
      <button class="glass" style="--c:${c.btn}" data-d="1">+</button></div></div>`;
    el.querySelectorAll("button").forEach(b=>{
      b.setAttribute("aria-label",`${b.dataset.d>0?"Add to":"Subtract from"} ${G.names[i]}`);
      b.onclick=()=>change(i,Number(b.dataset.d)*r.step);
    });
    board.appendChild(el);
  }
  info();
}
function info(){
  if(!G) return;
  const t=G.rules.target, m=String(Math.floor(G.seconds/60)), s=String(G.seconds%60).padStart(2,"0");
  $("info").textContent=[t===null?"No limit":`Until ${t}`, G.rules.timer?`${m}:${s}`:""].filter(Boolean).join("  ·  ");
}
setInterval(()=>{ if(G && !$("game").hidden && G.winner===null && !document.hidden){ G.seconds++; info(); if(G.seconds%10===0) save(); } },1000);
const note=msg=>$("heard").textContent=msg;

/* ---------- sound, speech, screen ---------- */
let audio=null;
function feedback(up){
  const r=G.rules;
  if(r.vibrate && navigator.vibrate) navigator.vibrate(35);
  if(!r.sound) return;
  try{
    audio=audio||new (window.AudioContext||window.webkitAudioContext)(); audio.resume();
    const o=audio.createOscillator(), g=audio.createGain(), t=audio.currentTime;
    o.frequency.value=up?880:330; g.gain.setValueAtTime(.12,t); g.gain.exponentialRampToValueAtTime(.001,t+.13);
    o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t+.14);
  }catch(e){}
}
let speaking=false, speakTimer=null;
function speak(text){
  if(!G.rules.announce || !window.speechSynthesis) return;
  hush(); speaking=true; if(rec) try{rec.abort()}catch(e){}   // don't let the app hear itself
  const u=new SpeechSynthesisUtterance(text); u.lang="en-US";
  const done=()=>{ if(current!==u) return; current=null; speaking=false; clearTimeout(speakTimer); if(wantMic) beginRec(); };
  current=u; u.onend=u.onerror=done; speakTimer=setTimeout(done,Math.max(4500,text.length*120)); speechSynthesis.speak(u);
}
function hush(){ current=null; speaking=false; clearTimeout(speakTimer); if(window.speechSynthesis) speechSynthesis.cancel(); }
let current=null, lock=null;
async function wake(){ try{ if(G&&G.rules.awake&&navigator.wakeLock&&!lock){ lock=await navigator.wakeLock.request("screen"); lock.onrelease=()=>lock=null; } }catch(e){} }
function releaseWake(){ if(lock){ lock.release().catch(()=>{}); lock=null; } }
document.addEventListener("visibilitychange",()=>{ if(!document.hidden && !$("game").hidden) wake(); });

/* ---------- microphone ---------- */
const Speech=window.SpeechRecognition||window.webkitSpeechRecognition;
let rec=null, wantMic=false;
function micLabel(){ $("mic").textContent=wantMic?"Listening":"Mic off"; $("mic").classList.toggle("on",wantMic); }
function startListening(){
  if(!Speech) return note("Voice isn't supported here. Try Chrome or Safari");
  wantMic=true; micLabel(); note('Say "point for '+G.names[0]+'"'); beginRec();
}
function stopListening(){ wantMic=false; micLabel(); if(rec) try{rec.abort()}catch(e){} rec=null; }
function beginRec(){
  if(!wantMic || rec || speaking) return;
  const r=new Speech(), done={}, timers={};
  r.lang="en-US"; r.continuous=true; r.interimResults=true; r.maxAlternatives=3;
  r.onresult=e=>{
    for(let k=e.resultIndex;k<e.results.length;k++){
      if(done[k]) continue;
      const res=e.results[k], texts=Array.from(res,a=>a.transcript);
      clearTimeout(timers[k]);
      if(res.isFinal){ done[k]=true; heard(texts); }
      // Some phones are slow to finish a phrase, so act after a short silence.
      else timers[k]=setTimeout(()=>{ done[k]=true; heard(texts); try{r.abort()}catch(x){} },1200);
    }
  };
  r.onerror=e=>{
    const msg={"not-allowed":"Microphone blocked. Allow it in browser settings",
      "service-not-allowed":"Voice blocked. On iPhone, turn on Siri and Dictation",
      "audio-capture":"No microphone found","network":"Voice needs an internet connection"}[e.error];
    if(msg){ wantMic=false; micLabel(); note(msg); }
  };
  r.onend=()=>{ Object.values(timers).forEach(clearTimeout); if(rec===r) rec=null; if(wantMic) setTimeout(beginRec,250); };
  rec=r; try{ r.start(); }catch(e){ rec=null; wantMic=false; micLabel(); note("Tap Mic to start voice"); }
}
function heard(texts){
  if($("game").hidden || speaking) return;
  let cmd=null, text=texts[0];
  for(const t of texts){ cmd=parseCommand(t,G.names,G.rules.step); if(cmd){ text=t; break; } }
  note(`Heard: "${text.trim()}"${cmd?"":" (no command)"}`);
  if(!cmd) return;
  if(G.winner!==null && cmd.type!=="next" && cmd.type!=="say" && cmd.type!=="stop") return;
  if(cmd.type==="score") change(cmd.player,cmd.delta);
  else if(cmd.type==="undo") undo();
  else if(cmd.type==="next"){ if(G.winner!==null) nextMatch(); }
  else if(cmd.type==="reset") reset();
  else if(cmd.type==="say") speak(scoreCall());
  else if(cmd.type==="stop"){ stopListening(); note("Voice off"); }
}
$("sayRules").onclick=()=>{
  const hint=$("sayHint");
  if(!Speech) return hint.textContent="Voice isn't supported in this browser. Type the numbers instead.";
  const r=new Speech(); r.lang="en-US"; hint.textContent="Listening…";
  let got=false;
  r.onresult=e=>{
    got=true; const text=e.results[0][0].transcript, out=parseRules(text);
    if(Object.keys(out).length){ Object.assign(cfg,out); save(); fillRules(); hint.textContent=`Set from "${text}"`; }
    else hint.textContent=`Heard "${text}". Try "until 20" or "starting at 5".`;
  };
  r.onerror=()=>{ got=true; hint.textContent="Couldn't use the microphone. Check permission, or type the numbers."; };
  r.onend=()=>{ if(!got) hint.textContent="Didn't catch that. Tap and try again."; };
  try{ r.start(); }catch(e){ hint.textContent="Tap again in a moment."; }
};

/* ---------- buttons ---------- */
$("goNew").onclick=()=>{ fillRules(); show("rules"); };
$("goResume").onclick=openGame;
$("goHelp").onclick=help;
$("rulesBack").onclick=()=>show("home");
$("startGame").onclick=startGame;
$("home2").onclick=()=>{ save(); show("home"); };
$("undo").onclick=undo;
$("mic").onclick=()=>{ if(wantMic){ stopListening(); note("Voice off"); } else { hush(); startListening(); } };
$("swap").onclick=()=>{ G.order.reverse(); save(); render(); };
$("more").onclick=()=>popup("Menu","",[
  ["Say the score",()=>speak(scoreCall())],
  ["Voice commands",help],
  ["Reset scores",()=>popup("Reset scores?","",[["Yes, reset",reset,"rgba(255,38,56,.75)"],["Cancel"]])],
  ["Change rules",()=>{ fillRules(); show("rules"); }],
  ["Close",null,"rgba(31,111,255,.75)"]
]);
show("home");
</script>
</body>
</html>
"""


def app(environ, start_response):
    """The web app (standard WSGI). Vercel runs this for every request."""
    if environ.get("PATH_INFO", "/") in ("", "/", "/index.html"):
        status, kind, body = "200 OK", "text/html", PAGE.encode("utf-8")
    else:
        status, kind, body = "404 Not Found", "text/plain", b"Not found"
    start_response(status, [
        ("Content-Type", f"{kind}; charset=utf-8"),
        ("Content-Length", str(len(body))),
        ("Cache-Control", "no-cache"),
    ])
    return [body]


class QuietHandler(WSGIRequestHandler):
    def log_message(self, *args):
        pass


def main(port=8765):
    try:
        server = make_server("127.0.0.1", port, app, handler_class=QuietHandler)
    except OSError:  # port busy: pick another
        server = make_server("127.0.0.1", 0, app, handler_class=QuietHandler)
    url = f"http://localhost:{server.server_port}"
    print(f"Callout is running at {url}\nPress Ctrl+C to stop.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
