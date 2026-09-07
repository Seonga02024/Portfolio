import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const i18nDir = path.join(root, "assets", "i18n");
const overrides = readJson(path.join(root, "scripts", "i18n-overrides.en.json"));
const pages = {
  home: "index.html",
  "attack-on-titan": "attack-on-titan/index.html",
  carebrainfit: "carebrainfit/index.html",
  gostop: "gostop/index.html",
  "gucci-tennis": "gucci-tennis/index.html",
  match3: "match3/index.html",
  "melody-pangpang": "melody-pangpang/index.html",
  robocare: "robocare/index.html",
  "run-to-room": "run-to-room/index.html",
  silbot: "silbot/index.html",
};

const hangul = /[\uac00-\ud7a3]/;
const skipTags = new Set(["script", "style", "noscript", "code", "pre", "textarea", "input", "select"]);
const translatedAttributes = ["title", "alt", "aria-label", "placeholder", "content"];

function normalize(value) {
  return String(value || "")
    .replace(/\bKEMI FRIENDS\b/gi, "Cami Friends")
    .replace(/\bKEMI\b/gi, "Cami")
    .replace(/\s+/g, " ")
    .trim();
}

function decodeHtml(value) {
  return value
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)))
    .replace(/&nbsp;/gi, "\u00a0")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&apos;|&#39;/gi, "'");
}

function collectSources(html) {
  let clean = html.replace(/<!--[^]*?-->/g, "");
  for (const tag of skipTags) {
    if (tag === "input") continue;
    clean = clean.replace(new RegExp(`<${tag}\\b[^>]*>[^]*?<\\/${tag}\\s*>`, "gi"), "");
  }

  const sources = new Set();
  const add = (value) => {
    const source = normalize(decodeHtml(value));
    if (source && hangul.test(source)) sources.add(source);
  };

  for (const match of clean.matchAll(/>([^<>]+)</gs)) {
    const value = decodeHtml(match[1]);
    if (!hangul.test(value)) continue;
    if (value.includes("\n")) {
      for (const line of value.split(/\r?\n/)) add(line);
    } else {
      add(value);
    }
  }

  for (const match of clean.matchAll(/<([a-z][\w:-]*)\b[^>]*>/gi)) {
    const tag = match[1].toLowerCase();
    if (skipTags.has(tag)) continue;
    const markup = match[0];
    for (const attribute of translatedAttributes) {
      const attrMatch = markup.match(new RegExp(`\\b${attribute}\\s*=\\s*["']([^"']+)["']`, "i"));
      if (attrMatch) add(attrMatch[1]);
    }
  }

  return [...sources];
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function readBaseline(relativeFile, fallbackFile) {
  try {
    return JSON.parse(execFileSync("git", ["show", `HEAD:${relativeFile}`], {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }));
  } catch {
    return readJson(fallbackFile);
  }
}

function keyNumber(key) {
  const match = String(key).match(/(\d+)$/);
  return match ? Number(match[1]) : 0;
}

function polishEnglish(source, value) {
  let polished = String(value || "")
    .replace(/Get hit by a robo|Robo Hitgo|Robo Hit/g, "Robo Go-Stop")
    .replace(/\bRobo Gostop\b/g, "Robo Go-Stop")
    .replace(/\bMajgo\b/g, "Go-Stop")
    .replace(/\bGoStop\b/g, "Go-Stop")
    .replace(/\bKEMI Friends\b|\bChemistry Friends\b|\bChemi Friends\b/gi, "Cami Friends")
    .replace(/\bKEMI\b|\bChemistry\b|\bChemi\b/gi, "Cami")
    .replace(/\bSeongah Park\b/g, "Park Seong-A")
    .replace(/\battack on titan\b/g, "Attack on Titan");
  if (source.includes("재화")) polished = polished.replace(/\bgoods\b/gi, "currency");
  if (source.includes("체조")) polished = polished.replace(/\bgymnastics\b/gi, "exercise");
  if (source.includes("실제 서비스")) {
    polished = polished
      .replace(/actual services?/gi, "production services")
      .replace(/actual operational functions/gi, "production features");
  }
  return polished;
}

for (const [page, relativeHtml] of Object.entries(pages)) {
  const koFile = path.join(i18nDir, `${page}.ko.json`);
  const enFile = path.join(i18nDir, `${page}.en.json`);
  const oldKo = readBaseline(`assets/i18n/${page}.ko.json`, koFile);
  const oldEn = readBaseline(`assets/i18n/${page}.en.json`, enFile);
  const oldKeys = new Map(oldKo.entries.map((entry) => [normalize(entry.source), entry.key]));
  const oldEnglish = new Map(oldEn.entries.map((entry) => [normalize(entry.source), entry.text]));
  let nextKey = Math.max(0, ...oldKo.entries.map((entry) => keyNumber(entry.key))) + 1;

  const allSources = new Set(oldKo.entries.map((entry) => normalize(entry.source)));
  for (const source of collectSources(fs.readFileSync(path.join(root, relativeHtml), "utf8"))) allSources.add(source);

  const entries = [...allSources].map((source) => ({
    key: oldKeys.get(source) || `t${String(nextKey++).padStart(4, "0")}`,
    source,
  })).sort((a, b) => keyNumber(a.key) - keyNumber(b.key));

  const editNote = "Edit the text values. Keep key/source unchanged so the page can find each original string.";
  const ko = { page, language: "ko", edit_note: editNote, entries: entries.map((entry) => ({ ...entry, text: entry.source })) };
  const pageOverrides = { ...(overrides.global || {}), ...(overrides[page] || {}) };
  const en = {
    page,
    language: "en",
    edit_note: editNote,
    entries: entries.map((entry) => ({
      ...entry,
      text: polishEnglish(entry.source, pageOverrides[entry.source] ?? oldEnglish.get(entry.source) ?? ""),
    })),
  };

  fs.writeFileSync(koFile, `${JSON.stringify(ko, null, 2)}\n`, "utf8");
  fs.writeFileSync(enFile, `${JSON.stringify(en, null, 2)}\n`, "utf8");
  const missing = en.entries.filter((entry) => !entry.text.trim()).length;
  console.log(`${page}: ${entries.length} entries, ${missing} English translations missing`);
}
