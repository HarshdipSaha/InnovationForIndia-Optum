/* ============================================================
   SAAKSHI — motion & the simulated live-run.
   Progressive enhancement: all content is in the HTML. This file
   only adds the graph assembly, scroll reveals, and the detector
   run. Every effect degrades to a static end-state when JS is off
   or prefers-reduced-motion is set.
   ============================================================ */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var REDUCED = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
    : false;

  var SVGNS = "http://www.w3.org/2000/svg";
  function el(name, attrs) {
    var n = document.createElementNS(SVGNS, name);
    if (attrs) for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }

  /* ---------------------------------------------------------
     1. BUILD THE EVIDENCE GRAPH
     Center node + two rings of the 11 public portals, with
     hairline edges drawn inward. This is the page's spine.
  --------------------------------------------------------- */
  var CX = 320, CY = 320;
  // ordered outer-in; ring assignment interleaves so both rings fill
  var SOURCES = [
    { id: "LGD",          r: 150, a: -90,  key: true },
    { id: "NREGASoft",    r: 258, a: -60 },
    { id: "eGramSwaraj",  r: 150, a: -18 },
    { id: "CPPP",         r: 258, a: 6 },
    { id: "GeM",          r: 150, a: 54 },
    { id: "AuditOnline",  r: 258, a: 72 },
    { id: "CPGRAMS",      r: 150, a: 126 },
    { id: "DBT Bharat",   r: 258, a: 138 },
    { id: "IMPDS",        r: 150, a: 198 },
    { id: "data.gov.in",  r: 258, a: 210 },
    { id: "API Setu",     r: 150, a: 270 }
  ];

  function polar(r, deg) {
    var rad = (deg * Math.PI) / 180;
    return { x: CX + r * Math.cos(rad), y: CY + r * Math.sin(rad) };
  }

  var graph = document.querySelector("[data-graph]");
  var edgesG = graph && graph.querySelector("[data-edges]");
  var portalsG = graph && graph.querySelector("[data-portals]");
  var sweepsG = graph && graph.querySelector("[data-sweeps]");
  var edgePaths = [];

  if (graph && edgesG && portalsG) {
    SOURCES.forEach(function (s, i) {
      var p = polar(s.r, s.a);
      var charW = 6.2;            // ~monospace advance at 10.5px
      var rw = s.id.length * charW + 18;
      var rh = 21;
      // clamp x so the pill never runs off the 640 canvas
      var px = Math.max(rw / 2 + 2, Math.min(640 - rw / 2 - 2, p.x));
      var py = p.y;

      // edge: gentle quadratic curve from the pill edge toward the node
      var mx = (px + CX) / 2 + (py - CY) * 0.12;
      var my = (py + CY) / 2 + (CX - px) * 0.12;
      var d = "M" + px.toFixed(1) + " " + py.toFixed(1) +
              " Q" + mx.toFixed(1) + " " + my.toFixed(1) +
              " " + CX + " " + CY;
      var path = el("path", { d: d, class: "edge" });
      edgesG.appendChild(path);
      edgePaths.push(path);

      // portal node — every label sits in a pill sized to fit its text
      var g = el("g", { class: "portal" + (s.key ? " portal--key" : "") });
      g.setAttribute("data-portal-id", s.id);
      g.appendChild(el("rect", {
        x: (px - rw / 2).toFixed(1), y: (py - rh / 2).toFixed(1),
        width: rw.toFixed(1), height: rh, rx: rh / 2,
        class: "portal__dot"
      }));
      // a small saffron pip on the leading edge of the pill
      g.appendChild(el("circle", { cx: (px - rw / 2 + 8).toFixed(1), cy: py.toFixed(1), r: 3,
        class: s.key ? "portal__pip portal__pip--key" : "portal__pip" }));
      var t = el("text", { x: (px + 4).toFixed(1), y: (py + 0.5).toFixed(1), class: "portal__label" });
      t.textContent = s.id;
      g.appendChild(t);
      portalsG.appendChild(g);
      // remember resolved center for edge start
      s._px = px; s._py = py;
    });
  }

  // build the four detector sweep arcs (concentric, offset starts)
  var sweepEls = [];
  if (sweepsG) {
    for (var d = 1; d <= 4; d++) {
      var rr = 78 + d * 16;
      var arc = el("circle", { cx: CX, cy: CY, r: rr, class: "sweep sweep--" + d });
      var C = 2 * Math.PI * rr;
      arc.style.strokeDasharray = (C * 0.28).toFixed(1) + " " + C.toFixed(1);
      arc.setAttribute("data-circ", C.toFixed(1));
      sweepsG.appendChild(arc);
      sweepEls.push(arc);
    }
  }

  /* graph assembly: light the edges in sequence when the hero graph
     scrolls into view (or immediately, if reduced motion). */
  function assembleGraph() {
    if (REDUCED) {
      edgePaths.forEach(function (p) { p.classList.add("edge--lit"); });
      if (portalsG) [].forEach.call(portalsG.children, function (pg) { pg.classList.add("is-in"); });
      return;
    }
    edgePaths.forEach(function (path) {
      var len = path.getTotalLength();
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
      path.style.transition = "none";
      // force reflow so the initial offset applies before we animate
      /* eslint-disable no-unused-expressions */
      path.getBoundingClientRect();
    });
    edgePaths.forEach(function (path, i) {
      window.setTimeout(function () {
        var len = path.getTotalLength();
        path.style.transition = "stroke-dashoffset .9s cubic-bezier(.16,1,.3,1), stroke .6s, opacity .6s";
        path.style.strokeDashoffset = "0";
        path.classList.add("edge--lit");
        window.setTimeout(function () {
          path.classList.remove("edge--lit");
        }, 1400);
        var pg = portalsG.children[i];
        if (pg) pg.classList.add("is-in");
      }, 220 + i * 130);
    });
  }

  /* ---------------------------------------------------------
     2. SCROLL REVEALS  (assign targets, observe)
  --------------------------------------------------------- */
  var revealTargets = [
    ".hero__copy", ".hero__field",
    ".band--join .band__head", ".band--failure .band__head", ".band--run .band__head",
    ".band--casefile .band__head", ".band--loop .band__head", ".band--limits .band__head",
    ".band--impact .band__head", ".join__pull", ".failure__pull", ".run__foot",
    ".loop__persona", ".call", ".flywheel", ".team", ".close__copy",
    ".dossier", ".terminal"
  ];
  revealTargets.forEach(function (sel) {
    var n = document.querySelector(sel);
    if (n) n.setAttribute("data-reveal", "");
  });
  var staggerTargets = [".portal-legend", ".ledger", ".signals", ".limits", ".impact-grid", ".align__list"];
  staggerTargets.forEach(function (sel) {
    var n = document.querySelector(sel);
    if (n) {
      n.setAttribute("data-reveal-stagger", "");
      // per-child delay
      [].forEach.call(n.children, function (c, i) {
        c.style.transitionDelay = Math.min(i * 55, 500) + "ms";
      });
    }
  });

  function markIn(node) { node.classList.add("is-in"); }

  if (REDUCED || !("IntersectionObserver" in window)) {
    document.querySelectorAll("[data-reveal], [data-reveal-stagger]").forEach(markIn);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { markIn(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll("[data-reveal], [data-reveal-stagger]").forEach(function (n) { io.observe(n); });

    // graph assembly fires when the field is ~visible
    var field = document.querySelector("[data-field]");
    if (field) {
      var gio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { assembleGraph(); gio.disconnect(); }
        });
      }, { threshold: 0.35 });
      gio.observe(field);
    }
  }
  if (REDUCED) { assembleGraph(); }

  /* ---------------------------------------------------------
     3. COUNT-UP NUMBERS
  --------------------------------------------------------- */
  function countUp(node) {
    var target = parseFloat(node.getAttribute("data-count"));
    if (isNaN(target)) return;
    var decimals = (String(target).split(".")[1] || "").length;
    var text = node.textContent;
    var prefix = text.replace(/[0-9.,].*$/, "");
    var suffix = "";
    if (REDUCED) { return; } // keep the real value already in the HTML
    var dur = 1100, start = null;
    node.textContent = prefix + "0" + (decimals ? "." + "0".repeat(decimals) : "") + suffix;
    function step(ts) {
      if (!start) start = ts;
      var t = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - t, 3);
      var val = target * eased;
      node.textContent = prefix + val.toFixed(decimals) + suffix;
      if (t < 1) requestAnimationFrame(step);
      else node.textContent = prefix + target.toFixed(decimals) + suffix;
    }
    requestAnimationFrame(step);
  }

  /* ---------------------------------------------------------
     4. THE SIMULATED LIVE-RUN
     Sequences the four detectors: queued → running → fired,
     each firing driving a sweep arc across the graph. Ends with
     the 5/5 PASS result. Reduced motion shows all fired at once.
  --------------------------------------------------------- */
  var terminal = document.querySelector("[data-terminal]");
  var detectors = terminal ? [].slice.call(terminal.querySelectorAll(".detector")) : [];
  var resultEl = terminal ? terminal.querySelector("[data-result]") : null;
  var replayBtn = terminal ? terminal.querySelector("[data-replay]") : null;
  var runStarted = false;

  function setStatus(det, text) {
    var s = det.querySelector("[data-status]");
    if (s) s.textContent = text;
  }

  function playSweep(i) {
    if (REDUCED || !sweepEls[i]) return;
    var arc = sweepEls[i];
    var C = parseFloat(arc.getAttribute("data-circ"));
    arc.style.transition = "none";
    arc.style.strokeDashoffset = C;
    arc.style.opacity = "0.9";
    arc.getBoundingClientRect();
    arc.style.transition = "stroke-dashoffset 1.1s cubic-bezier(.22,.61,.36,1), opacity .5s ease .7s";
    arc.style.strokeDashoffset = "0";
    arc.style.opacity = "0";
  }

  function fireDetector(i, done) {
    var det = detectors[i];
    if (!det) { if (done) done(); return; }
    det.classList.add("is-running");
    setStatus(det, "running…");
    playSweep(i);
    window.setTimeout(function () {
      det.classList.remove("is-running");
      det.classList.add("is-fired");
      setStatus(det, "FIRED");
      // count-ups inside this detector
      det.querySelectorAll("[data-count]").forEach(countUp);
      if (done) done();
    }, 620);
  }

  function runSequence() {
    if (runStarted) return;
    runStarted = true;

    if (REDUCED) {
      detectors.forEach(function (det) {
        det.classList.add("is-fired");
        setStatus(det, "FIRED");
      });
      edgePaths.forEach(function (p) { p.classList.add("edge--lit"); });
      if (resultEl) resultEl.hidden = false;
      if (replayBtn) replayBtn.hidden = true;
      return;
    }

    var i = 0;
    (function next() {
      if (i >= detectors.length) {
        window.setTimeout(function () {
          if (resultEl) {
            resultEl.hidden = false;
            resultEl.style.opacity = "0";
            resultEl.style.transform = "translateY(10px)";
            resultEl.style.transition = "opacity .6s var(--ease-out,cubic-bezier(.16,1,.3,1)), transform .6s cubic-bezier(.16,1,.3,1)";
            resultEl.getBoundingClientRect();
            resultEl.style.opacity = "1";
            resultEl.style.transform = "none";
          }
          if (replayBtn) replayBtn.hidden = false;
        }, 350);
        return;
      }
      fireDetector(i, function () { i++; window.setTimeout(next, 480); });
    })();
  }

  function resetSequence() {
    runStarted = false;
    detectors.forEach(function (det) {
      det.classList.remove("is-fired", "is-running");
      setStatus(det, "queued");
    });
    if (resultEl) { resultEl.hidden = true; resultEl.style.opacity = ""; resultEl.style.transform = ""; }
  }

  if (terminal) {
    if (REDUCED || !("IntersectionObserver" in window)) {
      runSequence();
    } else {
      var tio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { runSequence(); tio.disconnect(); }
        });
      }, { threshold: 0.3 });
      tio.observe(terminal);
    }
  }
  if (replayBtn) {
    replayBtn.addEventListener("click", function () {
      resetSequence();
      window.setTimeout(runSequence, 120);
    });
  }

  /* count-ups outside the detector list (clock days-remaining) fire on view */
  var looseCounts = [].slice.call(document.querySelectorAll("[data-count]"))
    .filter(function (n) { return !terminal || !terminal.contains(n); });
  if (!REDUCED && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    looseCounts.forEach(function (n) { cio.observe(n); });
  }

  /* ---------------------------------------------------------
     5. COPY-COMMAND BUTTON
  --------------------------------------------------------- */
  var copyBtn = document.querySelector("[data-copy]");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var text = copyBtn.getAttribute("data-copy");
      var label = copyBtn.querySelector("[data-copy-label]");
      function ok() {
        copyBtn.classList.add("is-copied");
        if (label) label.textContent = "Copied";
        window.setTimeout(function () {
          copyBtn.classList.remove("is-copied");
          if (label) label.textContent = "Copy";
        }, 1800);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(ok, ok);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta); ok();
      }
    });
  }
})();
