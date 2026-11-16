// SPDX-License-Identifier: GPL-3.0-or-later · Copyright (C) 2026 Пантелеев Г.Д.
/* Общие данные и функции.
   Q — банк вопросов (data/questions/*.js), A — ответы-билеты (data/answers/*.js),
   C — шпаргалки (data/cards.js), FC — подписи к картинкам (data/figs.js). */
const Q = [];
const A = {};
const C = {};
const FC = {};

/* ---------- картинки ---------- */
function IMGSRC(k){ return k.indexOf("sv_")===0 ? "img/svg/"+k+".svg" : "img/slides/"+k+".webp"; }
function figSource(k){
  let m=k.match(/^L(\d\d)_p(\d\d)$/);
  if(m) return "лекция "+(+m[1])+", слайд "+(+m[2]);
  if(k.indexOf("T_")===0) return "из методички";
  if(k.indexOf("sv_")===0) return "";
  m=k.match(/^P(\d)_/);
  if(m) return "из отчёта по практике "+m[1];
  return k;
}
function figCap(k, cap){ const c=cap||FC[k]||"", s=figSource(k); return c&&s?c+" · "+s:(c||s); }
/* F — картинка внутри текста билета */
function F(k, cap){
  return '<figure class="fig"><img src="'+IMGSRC(k)+'" alt="'+(cap||FC[k]||k).replace(/"/g,"&quot;")+'" loading="lazy" data-z="1" onerror="this.closest(\'figure\').hidden=true"><figcaption>'+figCap(k,cap)+'</figcaption></figure>';
}
/* F2 — две картинки рядом */
function F2(a, ca, b, cb){ return '<div class="fig2">'+F(a,ca)+F(b,cb)+'</div>'; }
/* GAL — сетка небольших картинок */
function GAL(keys){ return '<div class="gal">'+keys.map(k=>F(k)).join("")+'</div>'; }
/* CARD — шпаргалка внутри билета */
function CARD(k){ const c=C[k]; return c?'<div class="cardx" data-card="'+k+'"><h3>'+c.title+'</h3>'+c.html+'</div>':''; }
/* L — ссылка на другой билет */
function L(id, text){ return '<a class="tlink" href="#'+id+'" data-t="'+id+'">'+(text||tlabel(id))+'</a>'; }
function tlabel(id){ const p=id.split("-"); return ({k1:"К1",k2:"К2",k3:"К3",k4:"К4",pr:"Практика",ex:"Экзамен"}[p[0]]||p[0])+" · "+p[1]; }
/* H — подзаголовок внутри билета, N — заметка «на защите / на коллоквиуме» */
function H(t){ return '<h4>'+t+'</h4>'; }
function N(t){ return '<p class="tip">'+t+'</p>'; }
function UL(items){ return '<ul>'+items.map(x=>'<li>'+x+'</li>').join("")+'</ul>'; }
function OL(items){ return '<ol>'+items.map(x=>'<li>'+x+'</li>').join("")+'</ol>'; }
function CODE(t){ return '<pre class="code">'+t+'</pre>'; }

/* ---------- хелперы для шпаргалок ---------- */
function card(title){ return {title:title, html:[].slice.call(arguments,1).join("")}; }
function tbl(head, rows){
  let h='<div class="tw"><table class="ct"><thead><tr>'+head.map(x=>'<th>'+x+'</th>').join("")+'</tr></thead><tbody>';
  rows.forEach(r=>{ h+='<tr>'+r.map(x=>'<td>'+x+'</td>').join("")+'</tr>'; });
  return h+'</tbody></table></div>';
}
function chain(items){
  return '<div class="chain">'+items.map((it,i)=>(i?'<span class="arr">→</span>':'')+'<div class="node"><b>'+it[0]+'</b>'+(it[1]?'<span>'+it[1]+'</span>':'')+'</div>').join("")+'</div>';
}
function bits(fields, hl){
  return '<div class="bits">'+fields.map(f=>'<div class="'+(hl&&hl.indexOf(f[0])>=0?'hl':'')+'" style="flex:'+f[1]+' 1 0"><b title="'+f[0]+'">'+f[0]+'</b>'+(f[2]?'<span>'+f[2]+'</span>':'')+'</div>').join("")+'</div>';
}
function note(t){ return '<p class="cn">'+t+'</p>'; }
function seq(L_, R_, msgs){
  const W=560, xl=80, xr=480, top=46, step=46, Hh=top+msgs.length*step+10;
  let s='<div class="tw"><svg class="seq" viewBox="0 0 '+W+' '+Hh+'" role="img" aria-label="Диаграмма обмена '+L_+' и '+R_+'">';
  s+='<rect x="'+(xl-72)+'" y="4" width="144" height="26" rx="6"/><text x="'+xl+'" y="22" text-anchor="middle" font-size="13" font-weight="600">'+L_+'</text>';
  s+='<rect x="'+(xr-72)+'" y="4" width="144" height="26" rx="6"/><text x="'+xr+'" y="22" text-anchor="middle" font-size="13" font-weight="600">'+R_+'</text>';
  s+='<line class="life" x1="'+xl+'" y1="30" x2="'+xl+'" y2="'+Hh+'"/><line class="life" x1="'+xr+'" y1="30" x2="'+xr+'" y2="'+Hh+'"/>';
  msgs.forEach((m,i)=>{
    const y=top+i*step+16, a=m[0]===">"?xl:xr, b=m[0]===">"?xr:xl, d=m[0]===">"?-1:1;
    s+='<line class="m" x1="'+a+'" y1="'+y+'" x2="'+(b+d*8)+'" y2="'+y+'"/>';
    s+='<polygon points="'+b+','+y+' '+(b+d*9)+','+(y-5)+' '+(b+d*9)+','+(y+5)+'"/>';
    s+='<text x="'+(W/2)+'" y="'+(y-6)+'" text-anchor="middle" font-size="13" font-weight="600">'+m[1]+'</text>';
    if(m[2]) s+='<text class="s" x="'+(W/2)+'" y="'+(y+15)+'" text-anchor="middle">'+m[2]+'</text>';
  });
  return s+'</svg></div>';
}
