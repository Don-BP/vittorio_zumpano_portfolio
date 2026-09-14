(function(){
"use strict";
const $=(s,c)=>(c||document).querySelector(s), $$=(s,c)=>[...(c||document).querySelectorAll(s)];
const pad=n=>String(n).padStart(2,"0");

/* ───────────────────────── language ───────────────────────── */
let lang="ja";
try{const s=localStorage.getItem("dv_lang"); if(s==="ja"||s==="en") lang=s;}catch(e){}

function applyLang(){
  document.documentElement.lang=lang;
  document.title = lang==="ja" ? "Vittorio Zumpano — ポートフォリオ" : "Vittorio Zumpano — Portfolio";
  $$("[data-i]").forEach(el=>{const v=T[el.dataset.i]; if(v) el.innerHTML=v[lang];});
  /* headlines reveal line by line: each <br>-separated line gets a masked wrapper */
  $$("h2.big").forEach(h=>{
    const lines=h.innerHTML.split(/<br\s*\/?>/i);
    h.innerHTML=lines.map(l=>'<span class="ln"><span class="li">'+l+'</span></span>').join("");
  });
  $$("#lang button").forEach(b=>b.classList.toggle("on",b.dataset.l===lang));
  $$("#rail button").forEach(b=>{const n=NAV[b.dataset.k]; if(n) $("span",b).textContent=n[lang];});
  $$("#drawer a").forEach(a=>{const n=NAV[a.dataset.k]; if(n) a.lastChild.textContent=n[lang];});
  const ul=$(".marq ul");
  if(ul){ const items=MARQ[lang].map(t=>`<li>${t}</li>`).join(""); ul.innerHTML=items+items; }
  $$("[data-vt]").forEach(el=>{const v=T[el.dataset.vt]; if(v) el.setAttribute("data-title",v[lang]);});
  if(typeof redrawCounts==="function") redrawCounts();
  try{localStorage.setItem("dv_lang",lang);}catch(e){}
}
$$("#lang button").forEach(b=>b.onclick=()=>{lang=b.dataset.l;applyLang();});

/* ───────────────────────── nav build ───────────────────────── */
const secs=$$("main section[data-k]");
const rail=$("#rail"), drawer=$("#drawer");
secs.forEach((s,i)=>{
  const b=document.createElement("button");
  b.dataset.k=s.dataset.k; b.appendChild(document.createElement("span"));
  b.onclick=()=>s.scrollIntoView({behavior:"smooth"});
  rail.appendChild(b);
  const a=document.createElement("a");
  a.href="#"+s.id; a.dataset.k=s.dataset.k;
  a.innerHTML='<i>'+pad(i+1)+'</i>'; a.appendChild(document.createTextNode(""));
  a.onclick=()=>document.body.classList.remove("menu");
  drawer.appendChild(a);
});
const railBtns=[...rail.children];
const PAL={
  hero:["#1b3f7a","#5a3410","#123a34"], intro:["#1b3f7a","#5a3410","#123a34"],
  flagship:["#2a2f7a","#5a3410","#1a2a5a"], labo:["#123c8a","#1f4a8a","#0e2f5a"],
  dash:["#1c2f7a","#3a2a7a","#0f2a4a"], ops:["#0f4a44","#1b3f7a","#123a34"],
  teach:["#1f5a2a","#3f5a10","#123a34"], td:["#0f2a5a","#6a3a10","#1b3f7a"],
  web:["#6a2a5a","#1f5a8a","#5a3410"], ai:["#4a1f7a","#6a1f5a","#1b3f7a"],
  video:["#7a1f1f","#6a3a10","#3a1f5a"], ppt:["#6a3a10","#7a5a10","#3a2a10"],
  mascot:["#6a2a5a","#123a34","#5a3410"], design:["#123c8a","#6a4a10","#1b3f7a"],
  event:["#6a1f6a","#3a1f7a","#1f3a6a"], hr:["#2a2f3a","#5a3410","#1b3f7a"],
  close:["#5a3410","#1b3f7a","#123a34"]};
const atmo=$("#atmo"); let curPal="";
function setPal(k){ if(k===curPal) return; curPal=k; const c=PAL[k]||PAL.hero;
  atmo.style.setProperty("--c1",c[0]); atmo.style.setProperty("--c2",c[1]); atmo.style.setProperty("--c3",c[2]); }
$("#menuBtn").onclick=()=>document.body.classList.toggle("menu");

/* ───────────────────────── scroll ───────────────────────── */
const bar=$("#bar"), top=$("#top"), hint=$("#hint");
let ticking=false;
function tick(){
  const y=scrollY, h=document.documentElement.scrollHeight-innerHeight;
  bar.style.width=(h>0?y/h*100:0)+"%";
  top.classList.toggle("stuck",y>40);
  if(hint) hint.classList.toggle("faded",y>90);
  let cur=0;
  for(let i=0;i<secs.length;i++){ if(secs[i].offsetTop-innerHeight*0.35<=y) cur=i; }
  railBtns.forEach((b,i)=>b.classList.toggle("on",i===cur));
  setPal(secs[cur].dataset.k);
  continuous(y);
  ticking=false;
}
addEventListener("scroll",()=>{if(!ticking){ticking=true;requestAnimationFrame(tick);}},{passive:true});
addEventListener("resize",tick,{passive:true});

/* ───────────────────────── motion ─────────────────────────
   Each rule assigns an entrance to a set of elements and a per-group
   stagger, so no two kinds of block arrive the same way. */
const MOTION=[
  /* selector,                                          how,     stagger ms */
  [".eyebrow",                                          "left",   0],
  ["h2.big",                                            "fade",   0],
  ["h3.mid",                                            "up",     0],
  ["section > .wrap > .lead, section > .wrap > p.sm",   "up",     0],
  [".statGrid > div",                                   "clip",  85],
  [".flow > div",                                       "flip",  95],
  [".grid > .card",                                     "card",  95],
  [".cap",                                              "left", 130],
  [".tile",                                             "drop",  55],
  [".mas",                                              "pop",   70],
  [".gal figure",                                       "up",    60],
  [".linkList a",                                       "left",  55],
  [".carHold",                                          "tilt",   0],
  [".cardScene",                                        "up",     0],
  [".cardPick",                                         "up",     0],
  [".btnRow",                                           "up",     0],
  [".demo",                                             "card",   0],
  [".aside",                                            "up",     0],
  /* the marquee brings its own edge-fade mask, so it cannot use the
     mask-based "clip" entrance — the two would fight over mask-image */
  [".marq",                                             "up",     0],
  [".chips",                                            "up",     0],
  [".heroMeta > div",                                   "up",    90],
  [".portrait",                                         "pop",    0],
  [".appTxt",                                           "left",   0],
  [".app.flip .appTxt",                                 "right",  0],
];
function assignMotion(){
  MOTION.forEach(([sel,how,stag])=>{
    $$(sel).forEach(el=>{
      if(el.dataset.a) return;                      /* first rule wins */
      el.dataset.a=how;
      if(stag) el.style.setProperty("--stag",stag+"ms");
    });
  });
  /* number the siblings inside every group so they arrive in a wave */
  $$(".statGrid,.flow,.grid,.gal,.linkList,.mascotGrid,.heroMeta").forEach(g=>{
    [...g.children].forEach((c,i)=>c.style.setProperty("--i",i));
  });
  /* screenshots opposite their text column come in from the other side */
  $$(".app").forEach(app=>{
    const flip=app.classList.contains("flip");
    $$(".carHold",app).forEach(c=>c.dataset.a=flip?"left":"right");
  });
  /* strip the old uniform classes so nothing double-animates */
  $$(".r,.rs").forEach(el=>{ el.classList.remove("r","rs","d1","d2","d3","d4","d5","d6"); if(!el.dataset.a) el.dataset.a="up"; });
}
assignMotion();

/* Two-way. Elements arrive as they scroll into view and leave the same way
   in reverse on the way back up, so scrolling up is as alive as scrolling down.
   Once an element has finished arriving it is marked "settled", which drops the
   entrance stagger — otherwise that delay would also sit in front of every
   later hover, and the last card in a row would react half a second late. */
const settleT=new WeakMap();
const io=new IntersectionObserver(es=>es.forEach(e=>{
  const el=e.target;
  clearTimeout(settleT.get(el));
  if(e.isIntersecting){
    el.classList.add("in");
    const d=parseFloat(getComputedStyle(el).transitionDelay)||0;
    settleT.set(el,setTimeout(()=>el.classList.add("settled"),d*1000+1500));
  }else{
    el.classList.remove("in","settled");
  }
/* The bottom edge is pulled a long way in: that is the edge things leave by
   when you scroll back up, so the exit plays in the lower quarter of the screen
   where you can see it, not off the bottom after it is already gone. */
}),{threshold:0,rootMargin:"0px 0px -24% 0px"});
$$("[data-a]").forEach(n=>io.observe(n));

/* ── pointer-tracked tilt ──
   a screenshot leans towards the cursor, the way a print held in the hand does.
   values land in CSS custom properties so the stylesheet keeps ownership of the
   transform and the entrance animations are never overwritten. */
function tilt(el,maxX,maxY,scale,takeover){
  let raf=0,hx="0",hy="0";
  el.addEventListener("pointermove",e=>{
    if(e.pointerType==="touch")return;
    const r=el.getBoundingClientRect();
    if(!r.width||!r.height)return;
    hx=(-((e.clientY-r.top)/r.height-.5)*maxX).toFixed(2);
    hy=(((e.clientX-r.left)/r.width-.5)*maxY).toFixed(2);
    if(raf)return;
    raf=requestAnimationFrame(()=>{
      raf=0;
      el.style.setProperty("--hx",hx);
      el.style.setProperty("--hy",hy);
      el.style.setProperty("--hs",scale);
      /* the scroll loop writes --tx/--ty inline on the same element, so while
         the pointer is in charge they have to be stood down by hand */
      if(takeover){ el.style.setProperty("--tx","0"); el.style.setProperty("--ty","0"); }
    });
  },{passive:true});
  const rest=()=>{
    if(raf){cancelAnimationFrame(raf);raf=0;}
    el.style.setProperty("--hx","0");
    el.style.setProperty("--hy","0");
    el.style.setProperty("--hs","1");
    if(takeover) continuous(scrollY);      /* hand the lean back to the scroll loop */
  };
  el.addEventListener("pointerleave",rest);
  el.addEventListener("pointercancel",rest);
}
if(matchMedia("(hover:hover)").matches){
  $$(".car").forEach(c=>tilt(c,7,9,"1.012",true));
  $$(".gal figure").forEach(f=>tilt(f,8,10,"1.015"));
  $$(".tile").forEach(t=>tilt(t,6,8,"1.01"));
}

/* continuous, scroll-linked motion (video 1's zoom-through + parallax) */
const heroWrap=$("#hero .wrap"), bigs=$$("h2.big"), cars=$$(".car");
function continuous(y){
  const vh=innerHeight;
  if(heroWrap){
    const p=Math.max(0,Math.min(1,y/(vh*.92)));          /* 0..1 leaving the hero */
    const e=p*p;                                          /* accelerate away */
    heroWrap.style.setProperty("--hz",(1+e*.34).toFixed(4));
    heroWrap.style.setProperty("--hy",(-e*90).toFixed(1));
    heroWrap.style.setProperty("--hb",(e*13).toFixed(2));
    heroWrap.style.setProperty("--ho",(1-e*1.12).toFixed(3));
  }
  for(const h of bigs){
    const r=h.getBoundingClientRect();
    if(r.bottom<-120||r.top>vh+120) continue;
    const p=(r.top+r.height/2-vh/2)/vh;                   /* -1..1 around centre */
    h.style.transform="translateY("+(p*-26).toFixed(1)+"px)";
  }
  for(const c of cars){
    if(c.matches(":hover")) continue;          /* the pointer owns the lean */
    const r=c.getBoundingClientRect();
    if(r.bottom<-200||r.top>vh+200) continue;
    const p=Math.max(-1,Math.min(1,(r.top+r.height/2-vh/2)/vh));
    const t=c.closest(".appGrid")?0:1;                    /* full-width ones tilt back */
    c.style.setProperty("--tx",(p*5.5*t).toFixed(2));
    c.style.setProperty("--ty",(t?0:(c.closest(".app.flip")?-p*6:p*6)).toFixed(2));
  }
}

/* ───────────────────────── counters ─────────────────────────
   A unit can differ by language — "2言語" reads as nonsense on the English
   side, where the label already says "in both" — so data-sfxja / data-sfxen
   win over the plain data-suffix, and finished counters are redrawn whenever
   the language changes. */
function sfxOf(el){
  const s=el.dataset["sfx"+lang];
  return s!==undefined ? s : (el.dataset.suffix||"");
}
function redrawCounts(){
  $$("[data-count].done").forEach(el=>{
    el.textContent=(+el.dataset.count).toLocaleString()+sfxOf(el);
  });
}
const cio=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return; cio.unobserve(e.target);
  const el=e.target, to=+el.dataset.count, t0=performance.now(), dur=1600;
  (function step(t){
    const p=Math.min(1,(t-t0)/dur), k=1-Math.pow(1-p,3.4);
    el.textContent=Math.round(to*k).toLocaleString()+sfxOf(el);
    if(p<1)requestAnimationFrame(step); else el.classList.add("done");
  })(t0);
}),{threshold:.5});
$$("[data-count]").forEach(n=>cio.observe(n));

/* ───────────────────────── carousels ─────────────────────────
   The slides sit stacked in one grid cell and cross-fade. Each carousel
   advances itself on a slow timer, stops while the cursor is over it, and
   stops while it is off screen, the tab is hidden, or a full-size image or
   video is open. The arrows and dots still drive it by hand and wrap round. */
const CAR_DWELL=4800;
$$(".car").forEach(car=>{
  const track=$(".carTrack",car), slides=$$("figure",track);
  const dots=$(".dots",car), cnt=$(".cnt",car);
  const prev=$(".pv",car), next=$(".nx",car);
  const n=slides.length;
  let i=0, timer=null, hovered=false, onScreen=false;
  slides.forEach((_,k)=>{
    const d=document.createElement("button");
    d.onclick=()=>{go(k);restart();}; dots.appendChild(d);
  });
  const dl=[...dots.children];
  function go(k){
    i=((k%n)+n)%n;
    slides.forEach((s,j)=>s.classList.toggle("on",j===i));
    dl.forEach((d,j)=>d.classList.toggle("on",j===i));
    cnt.textContent=pad(i+1)+" / "+pad(n);
  }
  function tickCar(){
    if(hovered||!onScreen||document.hidden||document.body.classList.contains("locked"))return;
    go(i+1);
  }
  function restart(){ clearInterval(timer); if(n>1) timer=setInterval(tickCar,CAR_DWELL); }
  prev.onclick=()=>{go(i-1);restart();};
  next.onclick=()=>{go(i+1);restart();};
  prev.disabled=next.disabled=(n<2);
  car.addEventListener("mouseenter",()=>{hovered=true;});
  car.addEventListener("mouseleave",()=>{hovered=false;restart();});
  let sx=null;
  car.addEventListener("touchstart",e=>{sx=e.touches[0].clientX;},{passive:true});
  car.addEventListener("touchend",e=>{
    if(sx===null)return; const dx=e.changedTouches[0].clientX-sx;
    if(Math.abs(dx)>46){ go(i+(dx<0?1:-1)); restart(); } sx=null;
  },{passive:true});
  new IntersectionObserver(es=>{onScreen=es[0].isIntersecting;},{threshold:.15}).observe(car);
  go(0); restart();
});

/* ───────────────────────── lightbox ───────────────────────── */
const lb=$("#lb"), stage=$("#lbstage"), lbimg=$("#lbimg"), lbpct=$("#lbpct"),
      lbtitle=$("#lbtitle"), lbhelp=$("#lbhelp"), bIn=$("#lbin"), bOut=$("#lbout");
let sc=1, fit=1, tx=0, ty=0, natW=1, natH=1, drag=null, helpT=null, moved=false;
const MIN=.08, MAX=9;

function render(){
  lbimg.style.transform="translate(-50%,-50%) translate("+tx+"px,"+ty+"px) scale("+sc+")";
  lbpct.textContent=Math.round(sc/fit*100)+"%";
  bOut.disabled=sc<=MIN*1.001; bIn.disabled=sc>=MAX*0.999;
}
function clamp(){
  const w=natW*sc,h=natH*sc,vw=stage.clientWidth,vh=stage.clientHeight;
  const mx=Math.max(0,(w-vw)/2+70), my=Math.max(0,(h-vh)/2+70);
  tx=Math.max(-mx,Math.min(mx,tx)); ty=Math.max(-my,Math.min(my,ty));
}
function doFit(){
  const vw=stage.clientWidth-56, vh=stage.clientHeight-56;
  fit=Math.min(vw/natW,vh/natH); if(!isFinite(fit)||fit<=0)fit=1;
  sc=fit; tx=0; ty=0; render();
}
function zoomTo(next,cx,cy){
  next=Math.max(MIN,Math.min(MAX,next));
  if(cx!=null){
    const r=stage.getBoundingClientRect();
    const ox=cx-r.left-r.width/2-tx, oy=cy-r.top-r.height/2-ty, k=next/sc;
    tx-=ox*(k-1); ty-=oy*(k-1);
  }
  sc=next; clamp(); render();
}
function lbOpen(src,title){
  lbtitle.textContent=title||"";
  lb.classList.add("open"); document.body.classList.add("locked");
  lbhelp.style.opacity="1"; clearTimeout(helpT);
  helpT=setTimeout(()=>{lbhelp.style.opacity="0";},4200);
  const setup=()=>{
    natW=lbimg.naturalWidth||1600; natH=lbimg.naturalHeight||1000;
    lbimg.style.width=natW+"px"; lbimg.style.height=natH+"px"; doFit();
  };
  lbimg.onload=setup; lbimg.src=src;
  if(lbimg.complete&&lbimg.naturalWidth) setup();
}
function lbClose(){ lb.classList.remove("open"); document.body.classList.remove("locked"); lbimg.src=""; }

$$(".carTrack img").forEach(im=>{
  im.addEventListener("click",()=>{
    const cap=im.closest("figure").dataset.cap||"";
    lbOpen(im.currentSrc||im.src,cap);
  });
});
$$(".gal figure").forEach(f=>{
  f.addEventListener("click",()=>{
    const cap=$("figcaption",f);
    lbOpen(f.dataset.lb,cap?cap.textContent:"");
  });
});

$("#lbclose").onclick=lbClose;
bIn.onclick=()=>zoomTo(sc*1.45);
bOut.onclick=()=>zoomTo(sc/1.45);
$("#lbfit").onclick=doFit;
$("#lb100").onclick=()=>{sc=1;tx=0;ty=0;clamp();render();};
stage.addEventListener("click",e=>{ if(e.target===stage&&!moved) lbClose(); });
stage.addEventListener("wheel",e=>{e.preventDefault();zoomTo(sc*(e.deltaY<0?1.16:1/1.16),e.clientX,e.clientY);},{passive:false});
stage.addEventListener("pointerdown",e=>{
  drag={x:e.clientX,y:e.clientY,tx:tx,ty:ty}; moved=false;
  stage.classList.add("grabbing"); try{stage.setPointerCapture(e.pointerId);}catch(err){}
});
stage.addEventListener("pointermove",e=>{
  if(!drag)return;
  if(Math.abs(e.clientX-drag.x)>4||Math.abs(e.clientY-drag.y)>4) moved=true;
  tx=drag.tx+(e.clientX-drag.x); ty=drag.ty+(e.clientY-drag.y); clamp(); render();
});
const endDrag=()=>{drag=null;stage.classList.remove("grabbing");};
stage.addEventListener("pointerup",endDrag);
stage.addEventListener("pointercancel",endDrag);
lbimg.addEventListener("dblclick",e=>{e.stopPropagation();zoomTo(sc>fit*1.2?fit:Math.max(1,fit*2.6),e.clientX,e.clientY);});
addEventListener("resize",()=>{if(lb.classList.contains("open"))doFit();});

/* ───────────────────────── video modal ───────────────────────── */
const vm=$("#vm"), vmframe=$("#vmframe"), vmtitle=$("#vmtitle"), vmextra=$("#vmextra");
const blobCache={};
/* In the single-file build every clip is carried inside the page as text and
   has to be decoded before it can play. In the web build VID already holds
   ordinary file paths, so the browser just streams them. */
function blobFor(key){
  const v=VID[key]; if(!v) return null;
  if(VID_ARE_URLS) return v;
  if(blobCache[key]) return blobCache[key];
  const bin=atob(v), len=bin.length, buf=new Uint8Array(len);
  for(let i=0;i<len;i++) buf[i]=bin.charCodeAt(i);
  const url=URL.createObjectURL(new Blob([buf],{type:"video/mp4"}));
  blobCache[key]=url; return url;
}
function vmOpen(html,title,extra){
  vmframe.innerHTML=html; vmtitle.textContent=title||""; vmextra.innerHTML=extra||"";
  vm.classList.add("open"); document.body.classList.add("locked");
}
function vmClose(){
  vm.classList.remove("open"); document.body.classList.remove("locked");
  vmframe.innerHTML=""; vmextra.innerHTML="";
}
$("#vmclose").onclick=vmClose;
vm.addEventListener("click",e=>{if(e.target===vm)vmClose();});

$$(".tile").forEach(tile=>{
  tile.addEventListener("click",()=>{
    /* the caption element is language-aware, so prefer it over the build-time attribute */
    const title=$(".cap b",tile)?.textContent||tile.getAttribute("data-title")||"";
    const yt=tile.dataset.yt;
    if(yt){
      vmOpen('<iframe src="https://www.youtube-nocookie.com/embed/'+yt+'?autoplay=1&rel=0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>',
        title,
        '<a class="btn" href="https://www.youtube.com/watch?v='+yt+'" target="_blank" rel="noopener">'+(T["ui.openyt"][lang])+'</a>');
      return;
    }
    const key=tile.dataset.v;
    if(!key) return;
    vmOpen('<div class="vmLoad">'+T["ui.loading"][lang]+'</div>',title,"");
    setTimeout(()=>{
      const url=blobFor(key);
      if(!url){vmframe.innerHTML='<div class="vmLoad">—</div>';return;}
      vmframe.innerHTML='<video src="'+url+'" controls autoplay playsinline></video>';
    },30);
  });
});

/* ── the looping animations run on their own, no hover and no clicking.
      They only wake up once they are near the screen, so a visitor who never
      scrolls that far never downloads them. ── */
$$("[data-loop]").forEach(v=>{
  let wired=false;
  const start=()=>{ const p=v.play(); if(p&&p.catch) p.catch(()=>{}); };
  const wake=()=>{
    if(wired) return; wired=true;
    const u=blobFor(v.dataset.loop); if(!u) return;
    v.src=u; v.muted=true; v.loop=true;
    v.addEventListener("canplay",start,{once:true});
    start();
  };
  new IntersectionObserver((es,o)=>{
    if(!es[0].isIntersecting) return;
    o.disconnect(); wake();
  },{rootMargin:"300px"}).observe(v);
  /* browsers pause background tabs; pick it back up when the page returns */
  document.addEventListener("visibilitychange",()=>{ if(!document.hidden&&wired) start(); });
});

/* ───────────────────────── mascots ───────────────────────── */
$$(".mas").forEach(m=>{
  const key=m.dataset.v; if(!key) return;
  const v=$("video",m); let loaded=false;
  const start=()=>{
    if(!loaded){ const u=blobFor(key); if(!u)return; v.src=u; loaded=true; }
    m.classList.add("play"); const p=v.play(); if(p&&p.catch) p.catch(()=>{});
  };
  const stop=()=>{ m.classList.remove("play"); try{v.pause();v.currentTime=0;}catch(e){} };
  m.addEventListener("mouseenter",start);
  m.addEventListener("mouseleave",stop);
  m.addEventListener("click",()=>{ m.classList.contains("play")?stop():start(); });
});

/* ───────────────────────── 3D card ─────────────────────────
   One card on the table at a time. The picker above it swaps which year's
   artwork is printed on the four faces. At rest the card stands ajar, so the
   front cover and a wedge of the inside spread are both visible; "open" lays
   it flat. Dragging is tracked on the window rather than the card itself, so
   the rotation can never stall when the pointer leaves the card's own box. */
(function(){
  const card=$("#c3d"); if(!card) return;
  const scene=card.closest(".cardScene"), pick=$("#cardPick");
  const Lf=$(".pL .fc.f",card), Lb=$(".pL .fc.b",card),
        Rf=$(".pR .fc.f",card), Rb=$(".pR .fc.b",card);
  /* a landscape sheet folds down the middle, a portrait one folds across it.
     The closed card opens away from its fold — rightwards on one, downwards on
     the other — so the resting pose leans the card the matching way to show a
     wedge of the inside behind the cover. */
  const POSE={
    wide:{rest:{ry:-17,rx:7}, flat:{ry:0,rx:3}},
    tall:{rest:{ry:-14,rx:-13},flat:{ry:0,rx:4}}
  };
  let horiz=false, ry=POSE.wide.rest.ry, rx=POSE.wide.rest.rx, open=false, cur=null, d=null;

  /* standing ajar the card fills only half of its box — the right half when it
     folds sideways, the bottom half when it folds across — so nudge it back to
     the middle of the scene */
  function paint(){
    /* Closed, the card fills only half its box, so it gets nudged back to the
       middle of the scene. That nudge has to follow the rotation smoothly —
       as the card turns, its folded half swings across to the other side and
       the correction has to swing with it. Hence the cosine: switching the
       sign at ninety degrees instead made the card jump sideways mid-drag. */
    let off="";
    if(!open){
      const rad=Math.PI/180;
      off = horiz ? "translateY("+(-25*Math.cos(rx*rad)).toFixed(2)+"%) "
                  : "translateX("+(-25*Math.cos(ry*rad)).toFixed(2)+"%) ";
    }
    card.style.transform=off+"rotateX("+rx+"deg) rotateY("+ry+"deg)";
  }
  /* a card that folds across the middle is only half as tall while it stands
     ajar, so the scene closes up behind it instead of leaving a hole */
  function fitScene(){
    const cs=getComputedStyle(scene);
    const pad=parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom);
    const h=card.offsetHeight;
    scene.style.height=(((horiz&&!open)?h*.78:h)+pad)+"px";
  }
  addEventListener("resize",fitScene,{passive:true});
  function flipped(){ const a=((ry%360)+360)%360; return a>90&&a<270; }

  const picks=pick?$$("button",pick):[];
  function setCard(b){
    if(!b)return;
    cur=b;
    const ar=parseFloat(b.dataset.ar)||1.403;
    horiz=ar<1;
    card.style.setProperty("--ar",ar);
    card.classList.toggle("horiz",horiz);
    card.classList.toggle("tall",horiz);
    Lf.style.backgroundImage=Rf.style.backgroundImage="url('"+b.dataset.in+"')";
    Lb.style.backgroundImage=Rb.style.backgroundImage="url('"+b.dataset.out+"')";
    picks.forEach(x=>x.classList.toggle("on",x===b));
    setOpen(open);
  }

  const btnOpen=$("#c3dOpen"), btnFlip=$("#c3dFlip"), btnZoom=$("#c3dZoom"), btnReset=$("#c3dReset");
  /* the label is driven through data-i so the language toggle relabels it too */
  function label(){
    btnOpen.dataset.i = open ? "e.close" : "e.open";
    const v=T[btnOpen.dataset.i]; if(v) btnOpen.innerHTML=v[lang];
  }
  function setOpen(v){
    open=v;
    card.classList.toggle("open",open); scene.classList.toggle("open",open);
    btnOpen.classList.toggle("on",open);
    const p=POSE[horiz?"tall":"wide"][open?"flat":"rest"]; ry=p.ry; rx=p.rx;
    label(); paint(); fitScene();
  }
  picks.forEach(b=>b.onclick=()=>setCard(b));
  setCard(picks[0]);

  btnOpen.onclick=()=>setOpen(!open);
  btnFlip.onclick=()=>{ ry+=180; paint(); };
  btnReset.onclick=()=>setOpen(false);
  if(btnZoom) btnZoom.onclick=()=>{
    if(!cur)return;
    const inside = open && !flipped();
    const name=$("span",cur)?.textContent||"";
    const side=T[inside?"e.zside":"e.oside"];
    lbOpen(inside?cur.dataset.in:cur.dataset.out, name+(side?" — "+side[lang]:""));
  };

  card.addEventListener("pointerdown",e=>{
    if(e.button)return;
    d={x:e.clientX,y:e.clientY,ry:ry,rx:rx};
    card.classList.add("grab");
    e.preventDefault();
  });
  addEventListener("pointermove",e=>{
    if(!d)return;
    ry=d.ry+(e.clientX-d.x)*0.45;
    rx=Math.max(-40,Math.min(40,d.rx-(e.clientY-d.y)*0.28));
    paint();
  },{passive:true});
  const up=()=>{ if(d){ d=null; card.classList.remove("grab"); } };
  addEventListener("pointerup",up);
  addEventListener("pointercancel",up);
  addEventListener("blur",up);
})();

/* ───────────────────────── copy buttons ───────────────────────── */
$$(".cp").forEach(b=>b.addEventListener("click",()=>{
  const done=()=>{ b.classList.add("done"); b.textContent=T["ui.copied"][lang];
    setTimeout(()=>{ b.classList.remove("done"); b.textContent=T["ui.copy"][lang]; },1600); };
  if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(b.dataset.cp).then(done,done); }
  else { const t=document.createElement("textarea"); t.value=b.dataset.cp; document.body.appendChild(t); t.select();
    try{document.execCommand("copy");}catch(e){} t.remove(); done(); }
}));

/* ───────────────────────── keys ───────────────────────── */
addEventListener("keydown",e=>{
  if(lb.classList.contains("open")){
    if(e.key==="Escape"){e.preventDefault();lbClose();}
    else if(e.key==="+"||e.key==="="){e.preventDefault();zoomTo(sc*1.45);}
    else if(e.key==="-"||e.key==="_"){e.preventDefault();zoomTo(sc/1.45);}
    else if(e.key==="0"){e.preventDefault();doFit();}
    return;
  }
  if(vm.classList.contains("open")&&e.key==="Escape"){e.preventDefault();vmClose();return;}
  if(document.body.classList.contains("menu")&&e.key==="Escape"){document.body.classList.remove("menu");}
});

applyLang();
tick();
})();
