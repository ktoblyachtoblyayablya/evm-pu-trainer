// SPDX-License-Identifier: GPL-3.0-or-later · Copyright (C) 2026 Пантелеев Г.Д.
/* Логика тренажёра: тест по разделам и вопросам, билеты с ответами, схемы и шпаргалки. */
Q.forEach((q,i)=>{ q.i=i; });
(function(){ const cnt={}; Q.forEach(q=>{ cnt[q.t]=(cnt[q.t]||0)+1; q.id=q.t+"#"+cnt[q.t]; }); })();
const $=id=>document.getElementById(id);
const secOf=t=>t.split("-")[0];
const numOf=t=>+t.split("-")[1];
const topicsOf=s=>Object.keys(TK).filter(t=>secOf(t)===s).sort((a,b)=>numOf(a)-numOf(b));
const TEST_SECS=SEC.filter(s=>!s.testless);
const SECN={}; SEC.forEach(s=>SECN[s.id]=s);

/* ---------- хранение ---------- */
const KEY="evmquiz-v1";
let store={st:{},sec:"all",sel:null,rand:false,tsec:"k1"};
try{ const raw=localStorage.getItem(KEY); if(raw) store=Object.assign(store,JSON.parse(raw)); }catch(e){}
function save(){ try{ localStorage.setItem(KEY,JSON.stringify(store)); }catch(e){} }
function allTopics(){ return TEST_SECS.reduce((a,s)=>a.concat(topicsOf(s.id)),[]); }
let sec=store.sec||"all";
if(sec!=="all"&&!SECN[sec]) sec="all";
let sel=new Set((store.sel&&store.sel.length?store.sel:allTopics()).filter(t=>TK[t]));
if(!sel.size) sel=new Set(allTopics());
let rand=!!store.rand;

/* ---------- состояние прохода ---------- */
let deck=[], pos=0, right=0, wrong=0, answered=false, mode="all", order=[];
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function build(m){
  mode=m||"all";
  let list=Q.filter(q=>sel.has(q.t));
  if(mode==="wrong") list=list.filter(q=>store.st[q.id]&&store.st[q.id].last===0);
  deck=list.map(q=>q.i); if(rand) shuffle(deck);
  pos=0; right=0; wrong=0; render();
}
function topicState(t){
  const qs=Q.filter(q=>q.t===t), st=qs.map(q=>store.st[q.id]);
  if(st.some(s=>s&&s.last===0)) return "bad";
  if(qs.length&&st.every(s=>s&&s.last===1)) return "ok";
  return "";
}
function chips(){
  const box=$("secchips"); box.innerHTML="";
  const mk=(label,pressed,title,on,dot)=>{ const b=document.createElement("button"); b.className="chip"; b.setAttribute("aria-pressed",pressed?"true":"false"); if(title) b.title=title; b.innerHTML=(dot!==undefined?'<span class="dot '+dot+'"></span>':'')+label; b.onclick=on; return b; };
  box.appendChild(mk("Все разделы",sec==="all",Q.length+" вопр.",()=>{ sec="all"; sel=new Set(allTopics()); persist(); }));
  TEST_SECS.forEach(s=>{
    const ts=topicsOf(s.id), n=Q.filter(q=>secOf(q.t)===s.id).length;
    const st=ts.map(topicState), dot=st.indexOf("bad")>=0?"bad":(st.every(x=>x==="ok")?"ok":"");
    box.appendChild(mk(s.name,sec===s.id,s.full+": "+s.about+" — "+n+" вопр.",()=>{ sec=s.id; sel=new Set(ts); persist(); },dot));
  });
  const tb=$("topchips"); tb.innerHTML="";
  $("toprow").hidden=(sec==="all");
  if(sec!=="all"){
    const ts=topicsOf(sec);
    $("toplabel").textContent=SECN[sec].full+" — вопросы";
    tb.appendChild(mk("Все",sel.size===ts.length,null,()=>{ sel=new Set(ts); persist(); }));
    ts.forEach(t=>{
      const n=Q.filter(q=>q.t===t).length;
      tb.appendChild(mk(String(numOf(t)),sel.has(t)&&sel.size<ts.length,TK[t]+" — "+n+" вопр.",()=>{
        if(sel.size===ts.length){ sel=new Set([t]); }
        else if(sel.has(t)){ sel.delete(t); if(!sel.size) sel=new Set(ts); }
        else sel.add(t);
        persist();
      },topicState(t)));
    });
  }
  const nw=Q.filter(q=>sel.has(q.t)&&store.st[q.id]&&store.st[q.id].last===0).length;
  $("b-wrong").textContent="Повторить ошибки ("+nw+")"; $("b-wrong").disabled=!nw;
  $("b-order").setAttribute("aria-pressed",rand?"true":"false");
}
function persist(){ store.sec=sec; store.sel=[...sel]; save(); build("all"); }

function fig(k, cap){
  return '<figure class="fig"><img src="'+IMGSRC(k)+'" alt="'+(FC[k]||k)+'" loading="lazy" data-z="1" onerror="this.closest(\'figure\').hidden=true"><figcaption>'+figCap(k,cap)+'</figcaption></figure>';
}
function figs(f, cap){ return (Array.isArray(f)?f:[f]).map(k=>fig(k,FC[k]||cap)).join(""); }
function cardHtml(key, tag){
  const c=C[key]; if(!c) return "";
  return '<div class="cardx">'+(tag?'<div class="tag">'+tag+'</div>':'')+'<h3>'+c.title+'</h3>'+c.html+'</div>';
}
function head(t){ return '<div class="tkt"><span class="n">'+tlabel(t)+'</span><span class="t">'+TK[t]+'</span></div>'; }

function render(){
  chips();
  const n=deck.length, done=right+wrong;
  $("s-pos").innerHTML=n?(pos<n?'Вопрос <b>'+(pos+1)+'</b> из '+n:'Пройдено <b>'+n+'</b> из '+n)+(mode==="wrong"?' · работа над ошибками':''):'';
  $("s-score").innerHTML=done?'Верно <b>'+right+'</b> · ошибок <b>'+wrong+'</b>':'';
  const bar=$("bar").children; bar[0].style.width=(n?right/n*100:0)+"%"; bar[1].style.width=(n?wrong/n*100:0)+"%";
  const stage=$("stage");
  if(!n){ stage.innerHTML='<div class="box">В выбранных вопросах нет заданий для повтора. Выберите другие или начните заново.</div>'; return; }
  if(pos>=n){ finish(); return; }
  const q=Q[deck[pos]]; answered=false;
  order=shuffle(q.o.map((_,i)=>i));
  let h='<article class="qcard">'+head(q.t);
  h+='<p class="q">'+q.q+'</p>';
  if(q.f&&q.fb) h+=figs(q.f,"Схема к вопросу");
  h+='<div class="opts">'+order.map((oi,k)=>'<button class="opt" data-k="'+k+'"><span class="k">'+(k+1)+'</span><span>'+q.o[oi]+'</span></button>').join("")+'</div>';
  h+='<div id="fbk"></div></article>';
  stage.innerHTML=h;
  stage.querySelectorAll(".opt").forEach(b=>b.onclick=()=>answer(+b.dataset.k));
}
function answer(k){
  if(answered) return; answered=true;
  const q=Q[deck[pos]], ok=order[k]===0;
  if(ok) right++; else wrong++;
  const s=store.st[q.id]||{r:0,w:0}; if(ok) s.r++; else s.w++; s.last=ok?1:0; store.st[q.id]=s; save();
  document.querySelectorAll(".opt").forEach((b,i)=>{ b.disabled=true; if(order[i]===0) b.classList.add("right"); else if(i===k) b.classList.add("wrong"); else b.classList.add("dim"); });
  let h='<div class="fb"><div class="verdict '+(ok?'ok':'bad')+'">'+(ok?'Верно.':'Неверно. Правильный ответ: '+q.o[0])+'</div><p class="expl">'+q.e+'</p>';
  if(q.f&&!q.fb) h+=figs(q.f,"Схема для запоминания");
  if(q.c) h+=cardHtml(q.c,"Шпаргалка");
  if(A[q.t]) h+='<p class="more">'+L(q.t,"Открыть билет "+tlabel(q.t)+" с полным ответом →")+'</p>';
  h+='<button class="btn primary next" id="b-next">'+(pos+1<deck.length?'Следующий вопрос →':'Показать итоги')+'</button></div>';
  $("fbk").innerHTML=h;
  const n=deck.length;
  $("s-score").innerHTML='Верно <b>'+right+'</b> · ошибок <b>'+wrong+'</b>';
  const bar=$("bar").children; bar[0].style.width=(right/n*100)+"%"; bar[1].style.width=(wrong/n*100)+"%";
  $("b-next").onclick=next; $("b-next").focus({preventScroll:true});
  chips();
}
function next(){ pos++; render(); const s=$("stage"); if(s.getBoundingClientRect().top<0) s.scrollIntoView({block:"start"}); }
function finish(){
  const n=deck.length, pct=Math.round(right/n*100);
  const per={}; deck.forEach(i=>{ const q=Q[i]; per[q.t]=per[q.t]||{n:0,bad:0}; per[q.t].n++; const s=store.st[q.id]; if(s&&s.last===0) per[q.t].bad++; });
  let h='<div class="box res"><div class="label">Итог прохода</div><div class="big">'+right+' из '+n+' · '+pct+'%</div>';
  h+='<div class="tlist">'+Object.keys(per).map(t=>'<div class="tl '+(per[t].bad?'bad':'ok')+'" title="'+TK[t]+'"><span>'+tlabel(t)+'</span><span>'+(per[t].bad?'ошибок '+per[t].bad:'всё верно')+'</span></div>').join("")+'</div>';
  h+='<div class="row"><button class="btn primary" id="f-wrong">Пройти ошибки ещё раз</button><button class="btn" id="f-again">Пройти заново</button></div></div>';
  $("stage").innerHTML=h;
  const nw=deck.filter(i=>{ const s=store.st[Q[i].id]; return s&&s.last===0; }).length;
  $("f-wrong").disabled=!nw; $("f-wrong").onclick=()=>build("wrong"); $("f-again").onclick=()=>build("all");
}

/* ---------- билеты ---------- */
let tsec=SECN[store.tsec]?store.tsec:"k1";
function ticketHtml(t, open){
  return '<details class="ticket" id="tk-'+t+'"'+(open?' open':'')+'><summary><span class="n">'+tlabel(t)+'</span><span class="tt">'+TK[t]+'</span></summary><div class="ans">'+(A[t]||'<p class="cn">Ответ готовится.</p>')+'</div></details>';
}
function tickets(){
  const v=$("v-tk");
  let h='<div class="box ctl"><div class="label">Раздел</div><div class="chips" id="tsecs"></div>';
  h+='<div class="row"><button class="btn" id="t-open">Развернуть все</button><button class="btn" id="t-close">Свернуть все</button><button class="btn" id="t-rand">Случайный вопрос</button>'+(tsec==="ex"?'<button class="btn" id="t-pair">Билет из двух вопросов</button>':'')+'</div><div id="t-pick"></div></div>';
  h+='<p class="cn">'+SECN[tsec].full+': '+SECN[tsec].about+'. Нажмите на вопрос, чтобы открыть ответ со схемами.</p>';
  h+='<div class="tickets">'+topicsOf(tsec).map(t=>ticketHtml(t,false)).join("")+'</div>';
  v.innerHTML=h;
  const box=$("tsecs");
  SEC.forEach(s=>{ const b=document.createElement("button"); b.className="chip"; b.setAttribute("aria-pressed",s.id===tsec?"true":"false"); b.textContent=s.name; b.title=s.full; b.onclick=()=>{ tsec=s.id; store.tsec=tsec; save(); tickets(); }; box.appendChild(b); });
  $("t-open").onclick=()=>v.querySelectorAll("details.ticket").forEach(d=>d.open=true);
  $("t-close").onclick=()=>v.querySelectorAll("details.ticket").forEach(d=>d.open=false);
  $("t-rand").onclick=()=>{ const ts=topicsOf(tsec); openTicket(ts[Math.floor(Math.random()*ts.length)]); };
  if($("t-pair")) $("t-pair").onclick=()=>{
    const a=1+Math.floor(Math.random()*15), b=16+Math.floor(Math.random()*15);
    $("t-pick").innerHTML='<div class="pick"><b>Билет:</b> 1) '+L("ex-"+a,a+". "+TK["ex-"+a])+'<br>2) '+L("ex-"+b,b+". "+TK["ex-"+b])+'</div>';
  };
}
function openTicket(t){
  if(!TK[t]) return;
  if(secOf(t)!==tsec||!$("tk-"+t)){ tsec=secOf(t); store.tsec=tsec; save(); show("tickets"); tickets(); }
  else show("tickets");
  const d=$("tk-"+t); if(!d) return;
  d.open=true; d.scrollIntoView({block:"start"});
}

/* ---------- схемы ---------- */
function topicFigs(t){
  const set=new Set();
  Q.filter(q=>q.t===t&&q.f).forEach(q=>(Array.isArray(q.f)?q.f:[q.f]).forEach(k=>set.add(k)));
  ((A[t]||"").match(/img\/(?:slides|svg)\/[^"']+?\.(?:webp|svg)/g)||[]).forEach(p=>set.add(p.replace(/^img\/(?:slides|svg)\//,"").replace(/\.(webp|svg)$/,"")));
  return [...set];
}
let ssec="k1";
function schemes(){
  const v=$("v-sch");
  let h='<div class="box ctl"><div class="label">Раздел</div><div class="chips" id="ssecs"></div></div>';
  h+='<p class="cn">Все схемы из лекций, методичек и отчётов, а также шпаргалки — по вопросам раздела. Нажмите на картинку, чтобы увеличить.</p>';
  const seen=new Set();
  topicsOf(ssec).forEach(t=>{
    const fs=topicFigs(t), cs=[...new Set(Q.filter(q=>q.t===t&&q.c).map(q=>q.c))].filter(c=>!seen.has(c));
    cs.forEach(c=>seen.add(c));
    if(!fs.length&&!cs.length) return;
    h+='<section class="sec"><h2><span class="n">'+tlabel(t)+'</span>'+TK[t]+'</h2>';
    if(fs.length) h+='<div class="thumbs">'+fs.map(k=>'<figure><img src="'+IMGSRC(k)+'" alt="'+(FC[k]||k)+'" loading="lazy" data-z="1" onerror="this.closest(\'figure\').hidden=true"><figcaption>'+figCap(k)+'</figcaption></figure>').join("")+'</div>';
    if(cs.length) h+='<div class="cards">'+cs.map(c=>cardHtml(c)).join("")+'</div>';
    if(A[t]) h+='<p class="more">'+L(t,"Билет "+tlabel(t)+" →")+'</p>';
    h+='</section>';
  });
  v.innerHTML=h;
  const box=$("ssecs");
  SEC.forEach(s=>{ const b=document.createElement("button"); b.className="chip"; b.setAttribute("aria-pressed",s.id===ssec?"true":"false"); b.textContent=s.name; b.title=s.full; b.onclick=()=>{ ssec=s.id; schemes(); }; box.appendChild(b); });
}

/* ---------- вкладки и адреса ---------- */
const VIEWS={test:["v-test","tab-test"],tickets:["v-tk","tab-tk"],schemes:["v-sch","tab-sch"],all:["v-all",null]};
function show(which){
  Object.keys(VIEWS).forEach(k=>{ $(VIEWS[k][0]).hidden=(k!==which); if(VIEWS[k][1]) $(VIEWS[k][1]).setAttribute("aria-selected",k===which?"true":"false"); });
  if(which==="all"&&!$("v-all").innerHTML) allView();
  if(which==="tickets"&&!$("v-tk").innerHTML) tickets();
  if(which==="schemes"&&!$("v-sch").innerHTML) schemes();
}
function route(){
  const h=location.hash.replace(/^#/,"");
  if(h==="print"||h==="all"){ document.body.classList.toggle("printing",h==="print"); show("all"); if(h==="print") document.querySelectorAll("#v-all img").forEach(i=>i.loading="eager"); return; }
  document.body.classList.remove("printing");
  if(TK[h]) openTicket(h);
  else if(h==="tickets") show("tickets");
  else if(h==="schemes") show("schemes");
  else show("test");
}
$("tab-test").onclick=()=>{ history.replaceState(null,"","#test"); show("test"); };
$("tab-tk").onclick=()=>{ history.replaceState(null,"","#tickets"); show("tickets"); };
$("tab-sch").onclick=()=>{ history.replaceState(null,"","#schemes"); show("schemes"); };
window.addEventListener("hashchange",route);

/* ---------- кнопки, клавиши, ссылки, лайтбокс ---------- */
$("b-order").onclick=()=>{ rand=!rand; store.rand=rand; save(); build(mode==="wrong"?"wrong":"all"); };
$("b-wrong").onclick=()=>build("wrong");
$("b-restart").onclick=()=>build("all");
$("b-reset").onclick=()=>{ const b=$("b-reset"); if(b.dataset.c){ store.st={}; save(); b.dataset.c=""; b.textContent="Сбросить статистику"; build("all"); } else { b.dataset.c="1"; b.textContent="Точно сбросить? Нажмите ещё раз"; setTimeout(()=>{ b.dataset.c=""; b.textContent="Сбросить статистику"; },4000); } };
document.addEventListener("keydown",e=>{
  if($("lb").classList.contains("on")){ if(e.key==="Escape") $("lb").classList.remove("on"); return; }
  if($("v-test").hidden||e.ctrlKey||e.metaKey||e.altKey) return;
  if(!answered&&/^[1-5]$/.test(e.key)){ const b=document.querySelector('.opt[data-k="'+(+e.key-1)+'"]'); if(b){ e.preventDefault(); b.click(); } }
  else if(answered&&e.key==="Enter"&&document.activeElement&&document.activeElement.id!=="b-next"){ const b=$("b-next"); if(b){ e.preventDefault(); b.click(); } }
});
document.addEventListener("click",e=>{
  const a=e.target.closest("a.tlink");
  if(a){ e.preventDefault(); history.replaceState(null,"","#"+a.dataset.t); openTicket(a.dataset.t); return; }
  const im=e.target.closest("img[data-z]"); if(im){ $("lbimg").src=im.src; $("lb").classList.add("on"); }
});
$("lb").onclick=()=>$("lb").classList.remove("on");

/* ---------- все билеты одной страницей: #all (для PDF — #print) ---------- */
function allView(which){
  const secs=which?[which]:SEC.map(s=>s.id);
  let h='<div class="phead"><h1>ЭВМ и периферийные устройства — билеты с ответами</h1><p>'+secs.map(s=>SECN[s].full).join(" · ")+'. По материалам курса Середкина В.Г. Автор: Пантелеев Г.Д.</p></div>';
  secs.forEach(s=>{
    h+='<section class="psec"><h2>'+SECN[s].full+' <small>'+SECN[s].about+'</small></h2>';
    topicsOf(s).forEach(t=>{ h+='<article class="pt"><h3><span class="n">'+tlabel(t)+'</span> '+TK[t]+'</h3><div class="ans">'+(A[t]||"")+'</div></article>'; });
    h+='</section>';
  });
  $("v-all").innerHTML=h;
}

const nf=Q.filter(q=>q.f).length, na=Object.keys(A).length;
$("sub").textContent=Q.length+" вопросов по 4 коллоквиумам и 9 практикам · "+nf+" со схемами · "+na+" билетов с ответами (коллоквиумы, практики, экзамен) · "+Object.keys(C).length+" шпаргалок.";
build("all"); route();
