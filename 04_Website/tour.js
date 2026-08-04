/* SAAKSHI — captioned 15-second guided tour (no audio).
   Adds a "Play 15-sec tour" button; on start it auto-scrolls the page while
   showing timed captions in the site's own type/colour. Total ≈ 14.4s.
   Triggers: click the button · press "t" · or open the page with ?tour=1
   (auto-starts after a short delay so you can hit Record first). */
(function () {
  "use strict";
  if (window.__skTour) return;
  window.__skTour = true;

  var STEPS = [
    { f: 0.00, t: "SAAKSHI — the witness for every rupee.", d: 2000 },
    { f: 0.12, t: "Eleven public portals — joined for the first time, on the LGD code.", d: 1900 },
    { f: 0.30, t: "62,745 audit findings. Zero acted on. ₹878 crore untraced.", d: 1900 },
    { f: 0.48, t: "Four forensic detectors run the whole audit as a batch job.", d: 1800 },
    { f: 0.60, t: "462 payments after completion · ₹1.19 crore · MATCH.", d: 1700 },
    { f: 0.74, t: "A case file: four signals, never one score — a question, not a verdict.", d: 1900 },
    { f: 0.87, t: "Then a citizen verifies it — in her language, on a borrowed phone.", d: 1800 },
    { f: 1.00, t: "Read-only. A false positive costs an official an explanation — never a citizen her rice.", d: 1400 }
  ];

  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  var CSS =
    '#sk-tourbtn{position:fixed;right:20px;bottom:20px;z-index:99998;' +
    'font:600 13.5px/1 "Segoe UI",system-ui,sans-serif;letter-spacing:.02em;' +
    'background:#D98A2B;color:#141B2E;border:1px solid #b9741f;border-radius:999px;' +
    'padding:11px 17px;cursor:pointer;box-shadow:0 6px 22px rgba(20,27,46,.28);}' +
    '#sk-tourbtn:hover{background:#e79a3f;}' +
    '#sk-tourbtn:focus-visible{outline:3px solid #2E8B6B;outline-offset:2px;}' +
    '#sk-cap{position:fixed;left:50%;bottom:34px;transform:translateX(-50%) translateY(8px);' +
    'z-index:99999;max-width:min(880px,92vw);' +
    'background:rgba(20,27,46,.95);color:#F4F0E6;' +
    'font:400 22px/1.42 Georgia,"Times New Roman",serif;' +
    'padding:20px 28px;border-radius:12px;text-align:center;' +
    'box-shadow:0 14px 44px rgba(20,27,46,.4);' +
    'opacity:0;transition:opacity .4s ease,transform .4s ease;pointer-events:none;}' +
    '#sk-cap.on{opacity:1;transform:translateX(-50%) translateY(0);}' +
    '#sk-cap .sk-bar{position:absolute;left:0;top:0;height:3px;width:0;background:#D98A2B;border-radius:12px 0 0 0;}' +
    '@media (max-width:600px){#sk-cap{font-size:17px;padding:15px 18px;bottom:18px;}#sk-tourbtn{bottom:14px;right:14px;}}';

  function build() {
    var st = document.createElement("style");
    st.textContent = CSS;
    document.head.appendChild(st);

    var btn = document.createElement("button");
    btn.id = "sk-tourbtn";
    btn.type = "button";
    btn.textContent = "▶ Play 15-sec tour";
    btn.setAttribute("aria-label", "Play a 15 second guided tour of the page");
    document.body.appendChild(btn);

    var cap = document.createElement("div");
    cap.id = "sk-cap";
    cap.setAttribute("role", "status");
    cap.setAttribute("aria-live", "polite");
    cap.innerHTML = '<span class="sk-bar"></span><span class="sk-text"></span>';
    document.body.appendChild(cap);

    return { btn: btn, cap: cap };
  }

  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  function scrollToF(f) {
    var max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    window.scrollTo({ top: Math.round(max * f), behavior: reduce ? "auto" : "smooth" });
  }

  var running = false;
  function run(els) {
    if (running) return;
    running = true;
    var btn = els.btn, cap = els.cap;
    var text = cap.querySelector(".sk-text"), bar = cap.querySelector(".sk-bar");
    btn.style.display = "none";

    (async function () {
      for (var i = 0; i < STEPS.length; i++) {
        var s = STEPS[i];
        scrollToF(s.f);
        text.textContent = s.t;
        bar.style.transition = "none";
        bar.style.width = "0%";
        cap.classList.add("on");
        void bar.offsetWidth; // reflow so the timer bar animates cleanly
        bar.style.transition = "width " + s.d + "ms linear";
        bar.style.width = "100%";
        await wait(s.d);
      }
      cap.classList.remove("on");
      await wait(450);
      btn.style.display = "";
      running = false;
    })();
  }

  function boot() {
    var els = build();
    els.btn.addEventListener("click", function () { run(els); });
    document.addEventListener("keydown", function (e) {
      var tag = (e.target && e.target.tagName || "").toLowerCase();
      if ((e.key === "t" || e.key === "T") && tag !== "input" && tag !== "textarea") run(els);
    });
    if (/[?&]tour=(1|auto|play)\b/.test(location.search)) {
      setTimeout(function () { run(els); }, 900);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
