(function () {
  "use strict";

  var STORAGE_LANG = "portfolio-language";
  var HANGUL_RE = /[\uac00-\ud7a3]/;
  var SKIP_TAGS = {
    SCRIPT: true,
    STYLE: true,
    NOSCRIPT: true,
    CODE: true,
    PRE: true,
    TEXTAREA: true,
    INPUT: true,
    SELECT: true
  };
  var ATTRS = ["title", "alt", "aria-label", "placeholder", "content"];
  var resources = { ko: null, en: null };
  var sourceMap = {};
  var currentLang = readLang();
  var observer = null;
  var statusTimer = null;

  function readLang() {
    try {
      return localStorage.getItem(STORAGE_LANG) === "en" ? "en" : "ko";
    } catch (_) {
      return "ko";
    } 
  }

  function saveLang(lang) {
    currentLang = lang === "en" ? "en" : "ko";
    try {
      localStorage.setItem(STORAGE_LANG, currentLang);
    } catch (_) {}
  }

  function normalize(text) {
    return String(text || "").replace(/\s+/g, " ").trim();
  }

  function preserveSpacing(original, translated) {
    var leading = (String(original).match(/^\s*/) || [""])[0];
    var trailing = (String(original).match(/\s*$/) || [""])[0];
    return leading + translated + trailing;
  }

  function shouldSkip(node) {
    for (var el = node.parentElement; el; el = el.parentElement) {
      if (SKIP_TAGS[el.tagName] || el.hasAttribute("data-no-translate")) return true;
    }
    return false;
  }

  function collectTextNodes(root) {
    var nodes = [];
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || shouldSkip(node)) return NodeFilter.FILTER_REJECT;
        var original = node.__portfolioOriginalText === undefined ? node.nodeValue : node.__portfolioOriginalText;
        if (!HANGUL_RE.test(original)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (walker.nextNode()) nodes.push(walker.currentNode);
    return nodes;
  }

  function collectAttrNodes(root) {
    var items = [];
    var elements = [];
    if (root.nodeType === 1) elements.push(root);
    if (root.querySelectorAll) {
      root.querySelectorAll("*").forEach(function (el) { elements.push(el); });
    }
    elements.forEach(function (el) {
      if (SKIP_TAGS[el.tagName] || el.hasAttribute("data-no-translate")) return;
      ATTRS.forEach(function (attr) {
        if (!el.hasAttribute(attr)) return;
        var value = el.getAttribute(attr);
        var key = "__portfolioOriginalAttr_" + attr;
        var original = el[key] === undefined ? value : el[key];
        if (original && HANGUL_RE.test(original)) items.push({ el: el, attr: attr, value: value });
      });
    });
    return items;
  }

  function originalText(node) {
    if (node.__portfolioOriginalText === undefined) node.__portfolioOriginalText = node.nodeValue;
    return node.__portfolioOriginalText;
  }

  function originalAttr(item) {
    var key = "__portfolioOriginalAttr_" + item.attr;
    if (item.el[key] === undefined) item.el[key] = item.value;
    return item.el[key];
  }

  function buildSourceMap() {
    sourceMap = {};
    var koEntries = resources.ko && Array.isArray(resources.ko.entries) ? resources.ko.entries : [];
    var enEntries = resources.en && Array.isArray(resources.en.entries) ? resources.en.entries : [];
    var enByKey = {};
    enEntries.forEach(function (entry) {
      if (!entry || !entry.key) return;
      enByKey[entry.key] = entry;
    });
    koEntries.forEach(function (entry) {
      if (!entry || !entry.source) return;
      var enEntry = enByKey[entry.key] || {};
      sourceMap[normalize(entry.source)] = {
        ko: entry.text || entry.source,
        en: enEntry.text || "",
        source: entry.source
      };
    });
  }

  function pageId() {
    var path = window.location.pathname.replace(/\\/g, "/");
    try {
      var assetsPath = new URL(assetBase(), window.location.href).pathname.replace(/\\/g, "/");
      var siteRoot = assetsPath.replace(/assets\/?$/i, "");
      if (path.indexOf(siteRoot) === 0) path = path.slice(siteRoot.length);
    } catch (_) {}

    var parts = path.split("/").filter(Boolean);
    if (!parts.length) return "home";

    var last = parts[parts.length - 1].toLowerCase();
    if (last === "index.html") {
      return parts.length === 1 ? "home" : parts[parts.length - 2];
    }

    if (parts.length === 1 && !/\.html?$/i.test(parts[0])) {
      return parts[0] === "Portfolio" ? "home" : parts[0];
    }

    return parts[0].replace(/\.html?$/i, "") || "home";
  }

  function assetBase() {
    var script = document.currentScript || document.querySelector('script[src$="language-toggle.js"]');
    if (!script) return "assets/";
    return script.src.replace(/language-toggle\.js(?:\?.*)?$/, "");
  }

  function loadResources() {
    var base = assetBase() + "i18n/" + pageId();
    return Promise.all(["ko", "en"].map(function (lang) {
      return fetch(base + "." + lang + ".json", { cache: "no-cache" })
        .then(function (response) {
          if (!response.ok) throw new Error("Missing language file: " + lang);
          return response.json();
        })
        .then(function (data) {
          resources[lang] = data;
        });
    })).then(function () {
      buildSourceMap();
    }).catch(function () {
      resources = { ko: { entries: [] }, en: { entries: [] } };
      sourceMap = {};
      showStatus("Language text files were not found.");
    });
  }

  function isEnglishMissing() {
    if (currentLang !== "en" || !resources.en || !Array.isArray(resources.en.entries)) return false;
    return resources.en.entries.some(function (entry) {
      return entry && entry.source && (!entry.text || !entry.text.trim());
    });
  }

  function showMissingEnglishNotice() {
    if (isEnglishMissing()) {
      showStatus("Some English text is empty. Edit assets/i18n/*.en.json.");
    }
  }

  function translateValue(source, lang) {
    var entry = sourceMap[normalize(source)];
    if (!entry) return source;
    var value = entry[lang];
    if (typeof value !== "string" || !value.trim()) {
      return entry.ko || entry.source || source;
    }
    return value;
  }

  function applyLanguage(root) {
    root = root || document.documentElement;
    if (root.nodeType === 3) {
      if (!root.nodeValue || shouldSkip(root)) return;
      var original = originalText(root);
      if (HANGUL_RE.test(original)) {
        root.nodeValue = preserveSpacing(original, translateValue(original, currentLang));
      }
      return;
    }
    collectTextNodes(root).forEach(function (node) {
      var source = originalText(node);
      node.nodeValue = preserveSpacing(source, translateValue(source, currentLang));
    });
    collectAttrNodes(root).forEach(function (item) {
      var source = originalAttr(item);
      item.el.setAttribute(item.attr, translateValue(source, currentLang));
    });
  }

  function refreshToggle() {
    document.documentElement.lang = currentLang;
    document.body.setAttribute("data-lang", currentLang);
    document.querySelectorAll(".language-toggle button").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-lang-value") === currentLang);
    });
  }

  function setLanguage(lang, root) {
    saveLang(lang);
    refreshToggle();
    applyLanguage(root);
    showMissingEnglishNotice();
  }

  function showStatus(message) {
    var el = document.querySelector(".language-toggle-status");
    if (!el) {
      el = document.createElement("div");
      el.className = "language-toggle-status";
      el.setAttribute("data-no-translate", "");
      document.body.appendChild(el);
    }
    el.textContent = message;
    el.classList.add("is-visible");
    clearTimeout(statusTimer);
    statusTimer = setTimeout(function () {
      el.classList.remove("is-visible");
    }, 2400);
  }

  function makeToggle() {
    if (document.querySelector(".language-toggle")) return;
    var toggle = document.createElement("div");
    toggle.className = "language-toggle";
    toggle.setAttribute("aria-label", "Language switcher");
    toggle.setAttribute("data-no-translate", "");
    toggle.innerHTML = '<button type="button" data-lang-value="ko">KO</button><button type="button" data-lang-value="en">EN</button>';

    var host = document.querySelector(".nav-tools") ||
      document.querySelector(".nav-inner") ||
      document.querySelector("header.nav") ||
      document.querySelector("header");

    if (host) {
      host.appendChild(toggle);
    } else {
      toggle.classList.add("is-floating");
      document.body.appendChild(toggle);
    }

    toggle.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-lang-value]");
      if (!button) return;
      setLanguage(button.getAttribute("data-lang-value"));
    });
  }

  function observeMutations() {
    if (observer) observer.disconnect();
    observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          if (node.nodeType === 1 || node.nodeType === 3) applyLanguage(node);
        });
      });
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  function init() {
    makeToggle();
    refreshToggle();
    loadResources().then(function () {
      applyLanguage(document.documentElement);
      showMissingEnglishNotice();
      observeMutations();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
