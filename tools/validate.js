#!/usr/bin/env node
// SPDX-License-Identifier: GPL-3.0-or-later · Copyright (C) 2026 Пантелеев Г.Д.
/* Проверка банка вопросов и билетов: node tools/validate.js
   Ошибки (код выхода 1): битый формат вопроса, нет картинки, нет шпаргалки, повтор вопроса,
   нет ответа на билет, ссылка на несуществующий билет, остатки шаблонов в тексте.
   Предупреждения: неиспользуемые шпаргалки и картинки. */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const files = [...html.matchAll(/<script src="([^"]+)"><\/script>/g)].map(m => m[1]).filter(f => f !== "js/app.js");
const code = files.map(f => fs.readFileSync(path.join(root, f), "utf8")).join("\n;\n") + "\n;({ Q, C, A, TK, SEC, FC });";
let data;
try { data = vm.runInNewContext(code, {}, { filename: "bank.js" }); }
catch (e) { console.error("Ошибка в файлах данных:", e.message); process.exit(1); }
const { Q, C, A, TK, SEC, FC } = data;

const errors = [], warn = [];
const imgs = new Set([
  ...fs.readdirSync(path.join(root, "img", "slides")).map(f => f.replace(/\.webp$/, "")),
  ...fs.readdirSync(path.join(root, "img", "svg")).map(f => f.replace(/\.svg$/, ""))]);
const used = new Set();
const seen = new Map();
const per = {};

Q.forEach((q, i) => {
  const where = `${q.t}, «${String(q.q).slice(0, 50)}…»`;
  if (!TK[q.t]) errors.push(`#${i}: неизвестная тема ${q.t}`);
  if (typeof q.q !== "string" || !q.q.trim()) errors.push(`${where}: пустой вопрос`);
  if (!Array.isArray(q.o) || q.o.length < 2) errors.push(`${where}: нужно минимум 2 варианта`);
  else if (new Set(q.o).size !== q.o.length) errors.push(`${where}: повторяются варианты`);
  if (q.o && q.o.length > 5) errors.push(`${where}: больше 5 вариантов — клавиши 1–5 не хватит`);
  if (typeof q.e !== "string" || !q.e.trim()) errors.push(`${where}: нет пояснения`);
  if (q.fb && !q.f) errors.push(`${where}: fb без картинки`);
  (q.f ? (Array.isArray(q.f) ? q.f : [q.f]) : []).forEach(k => { used.add(k); if (!imgs.has(k)) errors.push(`${where}: нет картинки ${k}`); });
  if (q.c && !C[q.c]) errors.push(`${where}: нет шпаргалки «${q.c}»`);
  if (seen.has(q.q)) errors.push(`${where}: такой вопрос уже есть`);
  seen.set(q.q, true);
  per[q.t] = (per[q.t] || 0) + 1;
});

Object.keys(TK).forEach(t => {
  const s = t.split("-")[0];
  const sec = SEC.find(x => x.id === s);
  if (!sec) errors.push(`${t}: неизвестный раздел`);
  if (sec && !sec.testless && !per[t]) errors.push(`${t}: нет ни одного вопроса`);
  if (!A[t]) errors.push(`${t}: нет билета с ответом`);
});
Object.keys(A).forEach(t => {
  if (!TK[t]) errors.push(`билет ${t}: нет такой темы`);
  const h = A[t];
  if (/\$\{|undefined|\[object |NaN/.test(h)) errors.push(`билет ${t}: остатки шаблона в тексте`);
  for (const m of h.matchAll(/img\/(?:slides|svg)\/([^"']+?)\.(?:webp|svg)/g)) { used.add(m[1]); if (!imgs.has(m[1])) errors.push(`билет ${t}: нет картинки ${m[1]}`); }
  for (const m of h.matchAll(/data-t="([^"]+)"/g)) if (!TK[m[1]]) errors.push(`билет ${t}: ссылка на несуществующий билет ${m[1]}`);
});
const usedCards = new Set(Q.map(q => q.c).filter(Boolean));
Object.keys(A).forEach(t => { for (const m of A[t].matchAll(/data-card="([^"]+)"/g)) usedCards.add(m[1]); });
Object.keys(C).forEach(k => { if (!usedCards.has(k)) warn.push(`шпаргалка «${k}» не привязана ни к одному вопросу`); });
imgs.forEach(k => { if (!used.has(k)) warn.push(`картинка ${k} нигде не используется`); if (!FC[k]) warn.push(`у картинки ${k} нет подписи в data/figs.js`); });

const bySec = {};
Object.keys(per).forEach(t => { const s = t.split("-")[0]; bySec[s] = (bySec[s] || 0) + per[t]; });
console.log(`Вопросов: ${Q.length} · со схемами: ${Q.filter(q => q.f).length} · шпаргалок: ${Object.keys(C).length} · билетов: ${Object.keys(A).length} · картинок: ${imgs.size}`);
console.log("По разделам: " + Object.keys(bySec).map(s => `${s}: ${bySec[s]}`).join("  "));
const thin = Object.keys(per).filter(t => per[t] < 3);
if (thin.length) console.log("Мало вопросов (<3): " + thin.join(", "));
warn.forEach(w => console.log("Предупреждение: " + w));
if (errors.length) { errors.forEach(e => console.error("Ошибка: " + e)); process.exit(1); }
console.log("Всё в порядке.");
