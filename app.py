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
      <p class="hint" id="sayHint">Say something like "names are Mark and Sara, first to 21, win by 2". If Until is lower than Starting at, the game counts down.</p>
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
/* ============================================================
   Smart voice: works out what you MEANT, not just fixed phrases.
   It runs right here on your device: free, instant, no AI account.
     1. tidy the words      ("um, can you give Sara two points")
     2. spot who and what   ("give @1 2 points")
     3. decide the intent   (add, take away, set, correct, ask, control)
   To avoid scoring from background chatter, a scoring sentence is
   only accepted when every word in it makes sense for scoring.
   ============================================================ */
const words = list => new Set(list.split(" "));
const UNIT   = words("point points pt pts goal goals run runs round rally");
const STRONG_ADD = words("add adds plus score scores scored award");
const WEAK_ADD   = words("give gives gave get gets got earn earns earned make makes made win wins won take takes took put have another more");
const STRONG_SUB = words("minus subtract deduct remove penalty penalize penalise");
const WEAK_SUB   = words("lose loses lost");
const NEUTRAL    = words("for to from on off away the a an of that this it his her their one extra bonus too also just back team side player both each with and");
const SCORE_WORDS = new Set([...UNIT,...STRONG_ADD,...WEAK_ADD,...STRONG_SUB,...WEAK_SUB,...NEUTRAL]);
// Words that are never mistaken for a name that merely sounds similar.
const RESERVED = new Set([...SCORE_WORDS, ..."set change make update correct at is should be been no not never dont was were i meant mean instead wrong sorry actually who whos what whats how many much does do did need needs winning ahead losing behind lead leads swap switch reset restart start stop next match game home undo again same cancel scratch listening talking mic left right first second third fourth fifth number everyone everybody all him them he she they".split(" ")]);

function soundsLike(word){
  return word.replace(/ph/g,"f").replace(/ck|c|q/g,"k").replace(/z/g,"s").replace(/(?!^)h/g,"")
    .replace(/ee|ea|ie|ey|y/g,"i").replace(/(.)\1+/g,"$1");
}
/* Which counter does the piece starting at word k refer to? */
function matchName(list,k,names){
  let best=[];
  names.forEach((name,i)=>{
    [[clean(name),false],[COLORS[i].name.toLowerCase(),true]].forEach(([target,isColor])=>{
      const len=target.split(" ").length;
      if(k+len>list.length) return;
      const piece=list.slice(k,k+len).join(" ");
      let score=null;
      if(piece===target) score=0;
      else if(piece===target+"s") score=.2;                      // "Mark's"
      else if(!isColor && target.length>=3 && !/\d/.test(piece) && !piece.split(" ").some(w=>RESERVED.has(w))){
        if(soundsLike(piece)===soundsLike(target)) score=.5;     // "Marc", "Sarah"
        else { const d=distance(piece,target); if(d<=(target.length<=5?1:2)) score=d; }
      }
      if(score!==null) best.push({i,len,score:score+(isColor?.1:0)});
    });
  });
  best.sort((a,b)=>a.score-b.score || b.len-a.len);
  if(!best.length || best.some(m=>m.i!==best[0].i && m.score===best[0].score && m.len===best[0].len)) return null;
  return best[0];
}
/* Turn speech into tidy words with players written as @0, @1 ... */
function understand(text,ctx){
  let raw=text.toLowerCase().replace(/\b(that|this) one\b/g,"$1").replace(/\banother one\b/g,"another");
  let s=clean(raw)
    .replace(/\b(um+|uh+|erm?|ah|okay|ok|alright|hey|callout|call out|please|yeah|yes|yep|well|now)\b/g," ")
    .replace(/\b(can|could|would|will) you\b/g," ").replace(/\blets\b/g," ")
    .replace(/\s+/g," ").trim();
  const list=s?s.split(" "):[], out=[], order=ctx.order||ctx.names.map((_,i)=>i);
  const ordinal={first:0,second:1,third:2,fourth:3,fifth:4};
  for(let k=0;k<list.length;k++){
    const w=list[k], n=list[k+1];
    if((w==="left"||w==="right") && /^(side|team|player|guy|one|1)$/.test(n||"") && order.length===2){ out.push("@"+order[w==="left"?0:1]); k++; continue; }
    if(w in ordinal && /^(team|player)$/.test(n||"") && ordinal[w]<order.length){ out.push("@"+order[ordinal[w]]); k++; continue; }
    if(/^(team|player|number)$/.test(w) && /^[1-5]$/.test(n||"") && Number(n)<=order.length){ out.push("@"+order[n-1]); k++; continue; }
    const m=matchName(list,k,ctx.names);
    if(m){ out.push("@"+m.i); k+=m.len-1; continue; }
    if(/^(him|her|them|he|she|they)$/.test(w) && ctx.last && ctx.last.changes.length===1){ out.push("@"+ctx.last.changes[0][0]); continue; }
    out.push(w);
  }
  return out.join(" ")
    .replace(/\b(everyone|everybody|all players|all teams|each player|each team|both players|both teams)\b/g,"@all")
    .replace(/\b(team|side) (@\d)/g,"$2").replace(/(@\d) (team|side)\b/g,"$1");
}
/* One scoring or "set the score" clause, e.g. "give @1 2 points". */
function readClause(c,ctx){
  let t=c.split(" ").filter(Boolean);
  const targets=t.filter(w=>w[0]==="@");
  if(!targets.length && t.includes("both") && ctx.names.length===2) targets.push("@all"), t.push("@all");
  if(!targets.length && ctx.names.length===1) targets.push("@0"), t.push("@0");
  if(targets.length!==1) return null;
  const players = targets[0]==="@all" ? ctx.names.map((_,i)=>i) : targets[0].slice(1).split("+").map(Number);
  const nums=t.filter(w=>/^\d+$/.test(w)); if(nums.length>1) return null;
  const num=nums.length?Number(nums[0]):null;
  const rest=t.filter(w=>w[0]!=="@" && !/^\d+$/.test(w));
  const has=set=>rest.some(w=>set.has(w)), s=t.join(" ");

  // "set Mark to 10", "change Sara's score to 5", "Mark should have 8", "make it 3 for Mark"
  const setting = num!==null && (/\b(set|change|update|correct)\b/.test(s) || /\bshould (be|have)\b/.test(s)
    || /@\S+ (score )?is at\b/.test(s) || (/\bmake\b/.test(s) && /\b(it|score)\b/.test(s)));
  if(setting){
    const ok=words("set change update correct make score to at is should be have has the it for s");
    if(!rest.every(w=>ok.has(w)) || num>100000) return null;
    return {type:"set",players,value:num};
  }
  if(!rest.every(w=>SCORE_WORDS.has(w))) return null;
  const away=/\b(from|off|away)\b/.test(s);
  const minus = has(STRONG_SUB) || (has(WEAK_SUB) && (num!==null||has(UNIT))) || (away && /\btakes?\b|\btook\b/.test(s));
  const plus = has(STRONG_ADD)
    || (has(WEAK_ADD) && (num!==null || has(UNIT) || rest.includes("another") || rest.includes("more")))
    || /\b(wins|won|takes|took) (that|it)\b/.test(s)
    || has(UNIT) || (num!==null && (rest.includes("for") || /^\d+ to @/.test(s)));
  if(!minus && !plus) return null;
  const amount=num===null?ctx.step:num;
  if(amount<1 || amount>10000) return null;
  return {type:"score",changes:players.map(p=>[p,minus?-amount:amount])};
}
function parseCommand(text,ctx){
  const s=understand(text,ctx), is=re=>re.test(s);
  if(!s) return null;
  // ---- controls ----
  if(is(/^(please )?(undo( that| it| the last( 1| point| score)?)?|go back|scratch that|take (that|it) back|cancel (that|the last (1|point))|revert( that)?|that (didnt|doesnt) count)$/)) return {type:"undo"};
  if(is(/^(same again|do (that|it) again|(1|one) more( time| point)?|another( point| 1)?|again please|repeat that)$/)) return {type:"repeat"};
  if(is(/^((stop|quit) listening|(turn )?(the )?(mic|microphone) off|(turn off|stop) (the )?(mic|microphone))$/)) return {type:"stop"};
  if(is(/^(be quiet|mute|stop talking|stop (reading|saying)( out)? the score(s)?)$/)) return {type:"voice",on:false};
  if(is(/^(unmute|start talking|talk (to me )?again|speak again|(read|say) the scores? (out )?again every time|start (reading|saying) the scores?( again)?)$/)) return {type:"voice",on:true};
  if(is(/^((swap|switch|flip|change)( the)? (sides|places|spots|positions)|swap( them)?)$/)) return {type:"swap"};
  if(is(/^((reset|restart)( (the|this))?( (game|match|score|scores|points|counters?))?|start (over|again)|start (the )?(game|match) (over|again)|clear (the )?(scores?|board)|zero (everything|the scores?))$/)) return {type:"reset"};
  if(is(/^((go (to )?(the )?)?next (match|game|1|round)|new (match|game)|play again|rematch|(lets )?go again)$/)) return {type:"next"};
  if(is(/^((go )?(back )?(to )?(the )?(home( screen| page)?|main menu))$/)) return {type:"home"};
  if(is(/^(help|what can i say|(show )?(the )?(voice )?commands)$/)) return {type:"help"};
  // ---- questions ----
  if(is(/^(whos|who is|who has)( currently)? (winning|ahead|in the lead|leading|in first|the most( points)?)\b|^who leads\b/)) return {type:"ask",ask:"leader"};
  if(is(/^(whos|who is|who has)( currently)? (losing|behind|trailing|in last|the (least|fewest)( points)?)\b/)) return {type:"ask",ask:"last"};
  let m=s.match(/^how (?:many|much)(?: more)?(?: points?)?(?: does| do)? @(\d) need\b|^how (?:close|far) is @(\d)\b|^what does @(\d) need\b/);
  if(m) return {type:"ask",ask:"need",player:Number(m[1]??m[2]??m[3])};
  m=s.match(/^how (?:many|much)(?: points?)? (?:does|has) @(\d)(?: have| got)?$|^(?:what does) @(\d) have$|^(?:whats|what is) @(\d)(?: s)?(?: score)?$|^@(\d) score$/);
  if(m) return {type:"ask",ask:"player",player:Number(m[1]??m[2]??m[3]??m[4])};
  if(is(/^(what(s| is| are)? (we )?(playing (to|until)|the (winning score|target|goal))|how (many|much) (points )?to win|what do (we|you) need to win)\b/)) return {type:"ask",ask:"target"};
  if(is(/^how long (have we been playing|has (it|this( game| match)?) been( going)?)/)) return {type:"ask",ask:"time"};
  if(is(/^((whats|what is|whats up with|say|read|tell me|give me|check)( me)?( the)? scores?( now| again)?|(the )?scores?|where are we( at)?|hows it looking|read it out)$/)) return {type:"ask",ask:"score"};
  // ---- "no, that was Sara" ----
  m=s.match(/\bnot @(\d) (?:(?:it|that) was |its |it is )?@(\d)$/);
  if(m) return {type:"correct",player:Number(m[2])};
  m=s.match(/@(\d)/);
  if(m && s.match(/@/g).length===1){
    const ok=words("no that thats was is it its i meant mean for instead point actually wrong player sorry should have been to give go goes gone one s");
    const rest=s.split(" ").filter(w=>w[0]!=="@");
    if(rest.every(w=>ok.has(w)) && (/\b(meant|instead|should have (been|gone)|wrong player)\b/.test(s)
        || /^(no|sorry|wrong)\b/.test(s) && !/\bpoint (for|to)\b/.test(s) && !/^no point\b/.test(s)
        || /\b(that|it)( point| one)? (was|should)\b/.test(s)))
      return {type:"correct",player:Number(m[1])};
  }
  // Never score from a "don't..." or a question.
  if(is(/\b(no|not|never|dont|doesnt|didnt|cant|isnt|wasnt|shouldnt)\b/) || is(/^(did|does|do|is|are|was|were|should|would|will|if|has|have|when|why|how|who|whos|what|whats)\b/)) return null;
  // ---- scoring, possibly several at once: "2 for Mark and 1 for Sara" ----
  let line=s.replace(/\bactually\b|\bjust\b|\balso\b/g," ").replace(/\s+/g," "), before;
  do{ before=line; line=line.replace(/@([\d+]+) (?:and )?@([\d+]+)/,"@$1+$2"); }while(line!==before);
  const acts=line.split(/\b(?:and|then)\b/).map(c=>c.trim()).filter(Boolean).map(c=>readClause(c,ctx));
  if(!acts.length || acts.some(a=>!a)) return null;
  return acts.length===1 ? acts[0] : {type:"many",acts};
}
/* Spoken setup: "3 players, first to 21, win by 2", "names are Mark and Sara". */
function parseRules(text){
  const s=clean(text), out={};
  const a=s.match(/\b(?:start|starts|starting)(?: everyone| off)?(?: (?:at|from|with|on))? (\d+)/);
  const b=s.match(/\b(?:until|till|til|up to|play to|playing to|play until|first to|first one to|go to|going to|go down to|going down to|down to|game to|games to|winning score is|win at|to win at) (\d+)/);
  if(a) out.start=Number(a[1]);
  if(b) out.target=Number(b[1]);
  if(/\b(no limit|no winning score|keep going forever|endless)\b/.test(s)) out.target=null;
  const c=s.match(/\b([1-5]) (?:players?|people|teams?|counters?|of us)\b/);
  if(c) out.count=Number(c[1]);
  if(/\b(no|dont|without)( need to)? win by (2|two|to)\b|\bwin by (2|two) off\b/.test(s)) out.winBy2=0;
  else if(/\bwin by (2|two|to|too)\b/.test(s)) out.winBy2=1;
  const d=s.match(/\b(?:count(?:ing)? by|go(?:ing)? up by|points? (?:are|is) worth|each (?:tap|point) is(?: worth)?) (1|2|3|5|10)s?\b/);
  if(d) out.step=Number(d[1]);
  if(/\b(allow negative|below zero (is )?(ok|allowed|on)|negative scores? (ok|allowed|on))\b/.test(s)) out.negative=1;
  const n=text.match(/\b(?:names are|players are|teams are|playing are|between)\s+(.+?)(?=[.;]|,?\s+(?:start|until|first|play to|playing to|up to|game to|win by|to \d)|$)/i);
  if(n){
    const names=n[1].split(/\s*(?:,|\band\b|&|\bversus\b|\bvs\b)\s*/i).map(x=>x.trim().slice(0,18)).filter(Boolean).slice(0,5)
      .map(x=>x.replace(/(^|\s)\p{L}/gu,ch=>ch.toUpperCase()));
    if(names.length){ out.names=names; out.count=Math.max(names.length,out.count||0); }
  }
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
  popup("Just talk",`<ul><li><b>Score:</b> "Give Sara two" · "Mark scores"</li>
  <li><b>Several:</b> "2 for Mark and 1 for Sara"</li><li><b>Take away:</b> "Take one from Mark"</li>
  <li><b>Set:</b> "Set Mark to 10"</li><li><b>Fix:</b> "No, that was Sara" · "Scratch that"</li>
  <li><b>Repeat:</b> "Same again"</li><li><b>Ask:</b> "Who's winning?" · "How many does Mark need?"</li>
  <li><b>Control:</b> "Swap sides" · "Start over" · "Be quiet" · "Next match" · "Stop listening"</li></ul>
  <p class="hint">Use the names you typed. Pause briefly between sentences.</p>`,[["Got it",null,"rgba(31,111,255,.75)"]]);
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
const change=(i,delta)=>apply([[i,delta]]);
/* Apply one or more [player, points] changes as a single step (one Undo). */
function apply(changes,isSet){
  if(!G || G.winner!==null) return false;
  const r=G.rules, t=r.target, down=t!==null && t<r.start, scores=[...G.scores], touched=[];
  let up=false, winner=-1;
  const before=JSON.stringify(G);
  for(const [i,delta] of changes){
    let next=G.scores[i]+delta;
    if(down){
      if(next<t){ const m=`Bust. ${G.names[i]} can't go below ${t}`; G.scores=scores; note(m); speak(`${m}. ${scoreCall()}`); return false; }
      next=Math.min(next,r.start);
    } else if(!r.negative) next=Math.max(next,Math.min(0,r.start));
    if(next===G.scores[i]) continue;
    up=up||next>G.scores[i]; G.scores[i]=next; touched.push(i);
    winner=findWinner(); if(winner>=0) break;
  }
  if(!touched.length) return false;
  undoStack.push(before); if(undoStack.length>200) undoStack.shift();
  G.last={changes,set:!!isSet};
  if(winner>=0){ G.winner=winner; undoStack=[]; }
  save(); render();
  for(const i of touched){ const el=document.querySelector(`.side[data-i="${i}"]`); if(el) el.classList.add("flash"); }
  feedback(up);
  if(winner>=0){ speak(`${G.names[winner]} wins. ${scoreCall()}`); winnerPopup(); }
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
  snapshot(); G.scores=G.names.map(()=>G.rules.start); G.seconds=0; G.last=null;
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
function speak(text,always){
  if((!always && !G.rules.announce) || !window.speechSynthesis) return;
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
      else timers[k]=setTimeout(()=>{ done[k]=true; heard(texts); try{r.abort()}catch(x){} },1500);
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
  const ctx={names:G.names,step:G.rules.step,order:G.order,last:G.last};
  let cmd=null, text=texts[0];
  for(const t of texts){ cmd=parseCommand(t,ctx); if(cmd){ text=t; break; } }
  note(`Heard: "${text.trim()}"${cmd?"":" (not sure what you meant)"}`);
  if(cmd) act(cmd);
}
function act(cmd){
  const over=G.winner!==null;
  if(over && !["next","home","ask","stop","voice"].includes(cmd.type)) return;
  switch(cmd.type){
    case "score": case "set": case "many": {
      const changes=[]; let isSet=false;
      for(const a of cmd.acts||[cmd]){
        if(a.type==="set"){ isSet=true; for(const p of a.players) changes.push([p,a.value-G.scores[p]]); }
        else changes.push(...a.changes);
      }
      apply(changes,isSet); break;
    }
    case "repeat":
      if(G.last && !G.last.set) apply(G.last.changes); else note("Nothing to repeat yet");
      break;
    case "correct": correct(cmd.player); break;
    case "ask": { const reply=answer(cmd); note(reply); speak(reply,true); break; }
    case "undo": undo(); break;
    case "reset": reset(); break;
    case "swap": G.order.reverse(); save(); render(); note("Swapped sides"); break;
    case "next": if(over) nextMatch(); else note('"Next match" works after someone wins'); break;
    case "home": if(over) leaveMatch("home"); else { save(); show("home"); } break;
    case "help": help(); break;
    case "voice":
      G.rules.announce=cfg.announce=cmd.on?1:0; save();
      if(cmd.on){ note("Score reading on"); speak(scoreCall()); } else { hush(); note("Score reading off"); if(wantMic) beginRec(); }
      break;
    case "stop": stopListening(); note("Voice off"); break;
  }
}
/* "No, that was Sara": move the last point to the right person. */
function correct(player){
  const last=G.last;
  if(!last || last.set || last.changes.length!==1 || !undoStack.length) return note("There's no single point to move");
  const [from,delta]=last.changes[0];
  if(from===player) return note(`That already went to ${G.names[player]}`);
  const keep=JSON.stringify(G), stack=[...undoStack], seconds=G.seconds;
  G=JSON.parse(undoStack.pop()); G.seconds=seconds;
  if(!apply([[player,delta]])){ G=JSON.parse(keep); undoStack=stack; save(); render(); }
}
/* Answers to questions about the game. */
function answer({ask,player}){
  const r=G.rules, t=r.target, down=t!==null && t<r.start, name=i=>G.names[i];
  if(ask==="score") return scoreCall();
  if(ask==="player") return `${name(player)} has ${G.scores[player]}`;
  if(ask==="target") return t===null?"There is no winning score":`Playing until ${t}${r.winBy2?", win by 2":""}`;
  if(ask==="time") return `${Math.floor(G.seconds/60)} minutes and ${G.seconds%60} seconds`;
  if(ask==="need"){
    if(t===null) return "There is no winning score";
    if(G.winner!==null) return `${name(G.winner)} already won`;
    let n=down?G.scores[player]-t:t-G.scores[player];
    if(!down && r.winBy2 && G.names.length>1) n=Math.max(n,Math.max(...G.scores.filter((_,j)=>j!==player))+2-G.scores[player]);
    return `${name(player)} needs ${n} more to win`;
  }
  if(G.names.length<2) return scoreCall();
  const dir=(down?-1:1)*(ask==="last"?-1:1);
  const sorted=G.names.map((_,i)=>i).sort((a,b)=>(G.scores[b]-G.scores[a])*dir);
  const top=sorted.filter(i=>G.scores[i]===G.scores[sorted[0]]);
  if(top.length===G.names.length) return `It's all tied at ${G.scores[top[0]]}`;
  if(top.length>1) return `${top.map(name).join(" and ")} are tied ${ask==="last"?"at the back":"for the lead"} at ${G.scores[top[0]]}`;
  const gap=Math.abs(G.scores[sorted[0]]-G.scores[sorted[1]]);
  return `${name(top[0])} is ${ask==="last"?"behind":"winning"} by ${gap}`;
}
$("sayRules").onclick=()=>{
  const hint=$("sayHint");
  if(!Speech) return hint.textContent="Voice isn't supported in this browser. Type the numbers instead.";
  const r=new Speech(); r.lang="en-US"; hint.textContent="Listening…";
  let got=false;
  r.onresult=e=>{
    got=true; const text=e.results[0][0].transcript, out=parseRules(text);
    if(Object.keys(out).length){
      const {names,...rest}=out; Object.assign(cfg,rest);
      if(names) cfg.names=[0,1,2,3,4].map(i=>names[i]||(i<cfg.count?cfg.names[i]||"":""));
      save(); fillRules(); hint.textContent=`Set from "${text}"`;
    }
    else hint.textContent=`Heard "${text}". Try "3 players, first to 21, win by 2".`;
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
