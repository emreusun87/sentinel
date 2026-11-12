/* ==========================================================================
   SENTINEL — Redoc 3-Pane Interactive Controller
   ========================================================================== */

(function () {
  "use strict";

  const DATA = window.SENTINEL_PORTAL_DATA;
  if (!DATA) {
    console.error("SENTINEL_PORTAL_DATA yüklenemedi.");
    return;
  }

  const nodesById = {};
  const nodesByMermaidId = {};
  DATA.nodes.forEach((n) => {
    nodesById[n.id] = n;
    nodesByMermaidId[n.mermaid_id] = n;
  });

  const notesByNum = {};
  const notesById = {};
  DATA.notes.forEach((p) => {
    notesByNum[p.num] = p;
    notesById[p.id] = p;
  });

  let currentScale = 1.0;
  let activeCodeText = "";

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderMathElement(latexStr, el, displayMode) {
    if (window.katex) {
      try {
        window.katex.render(latexStr, el, {
          displayMode: displayMode,
          throwOnError: false,
        });
        return;
      } catch (e) {
        console.warn("KaTeX render fallback:", e);
      }
    }
    el.textContent = latexStr;
  }

  /* ------------------------------------------------------------------------
     1. BUILD LEFT NAVIGATION TREE
     ------------------------------------------------------------------------ */
  function buildLeftSidebar() {
    const navContainer = document.getElementById("nav-tree");
    let html = "";

    // Group 1: Core Architecture
    html += `
      <div class="nav-group">
        <div class="nav-group-header"><span>Mimari Çekirdek</span></div>
        <a class="nav-item active" href="#sec-overview" data-target="sec-overview" data-search="vizyon problem hipotez genel bakış">
          <span class="pill pill-CORE">SPEC</span><span class="nav-label">Vizyon & Temel Hipotez</span>
        </a>
        <a class="nav-item" href="#sec-diagram" data-target="sec-diagram" data-search="mermaid bilişsel karar döngüsü diyagram akış şeması rsi">
          <span class="pill pill-RSI-L2">FLOW</span><span class="nav-label">Bilişsel Karar & RSI Döngüsü</span>
        </a>
        <a class="nav-item" href="#sec-math" data-target="sec-math" data-search="matematiksel denklemler entropi chollet schmidhuber gödel formül">
          <span class="pill pill-CAUSAL">MATH</span><span class="nav-label">Matematiksel Çerçeve (5 Denklem)</span>
        </a>
        <a class="nav-item" href="#sec-philosophy" data-target="sec-philosophy" data-search="felsefi temel conatus spinoza autopoiesis sibernetik simbiyoz">
          <span class="pill pill-AUTOTELIC">PHIL</span><span class="nav-label">Felsefi & Sibernetik Temel</span>
        </a>
      </div>
    `;

    // Group 2: Cognitive Nodes (Node 0 - Node 7)
    html += `<div class="nav-group"><div class="nav-group-header"><span>Bilişsel Düğümler (src/nodes)</span><span>8</span></div>`;
    DATA.nodes.forEach((n) => {
      const searchBlob = `${n.title} ${n.file} ${n.badge} ${n.summary}`.toLowerCase();
      html += `
        <a class="nav-item" href="#${n.id}" data-target="${n.id}" data-node="${n.id}" data-search="${escapeHtml(searchBlob)}">
          <span class="pill pill-${n.badge}">N${n.num}</span>
          <span class="nav-label">${escapeHtml(n.short_title.replace(/^Node \d+:\s*/, ""))}</span>
        </a>
      `;
    });
    html += `</div>`;

    // Group 3: Categorized Literature & Notes (#01 - #20)
    html += `<div class="nav-group"><div class="nav-group-header"><span>Literatür & Ar-Ge Notları</span><span>20</span></div>`;
    DATA.categories.forEach((cat) => {
      const catNotes = DATA.notes.filter((p) => p.category === cat);
      if (!catNotes.length) return;
      html += `<div class="nav-cat-title">${escapeHtml(cat)}</div>`;
      catNotes.forEach((p) => {
        const shortName = p.title.split(" - arXiv:")[0].split(" (")[0];
        const searchBlob = `#${p.num} ${p.title} ${p.category} ${p.related_nodes.join(" ")}`.toLowerCase();
        html += `
          <a class="nav-item" href="#${p.id}" data-target="${p.id}" data-paper="${p.num}" data-search="${escapeHtml(searchBlob)}">
            <span class="pill pill-PAPER">#${p.num}</span>
            <span class="nav-label">${escapeHtml(shortName)}</span>
          </a>
        `;
      });
    });
    html += `</div>`;

    navContainer.innerHTML = html;

    // Bind navigation clicks to synchronize right panel immediately
    navContainer.querySelectorAll(".nav-item").forEach((item) => {
      item.addEventListener("click", () => {
        navContainer.querySelectorAll(".nav-item").forEach((el) => el.classList.remove("active"));
        item.classList.add("active");

        const nodeId = item.getAttribute("data-node");
        const paperNum = item.getAttribute("data-paper");
        if (nodeId) {
          selectNodeContext(nodeId, true);
        } else if (paperNum) {
          selectPaperContext(paperNum, true);
        }
      });
    });
  }

  /* ------------------------------------------------------------------------
     2. BUILD CENTER SPECIFICATION CONTENT
     ------------------------------------------------------------------------ */
  function buildCenterContent() {
    // Synthesis equation in hero/overview
    const synthEl = document.getElementById("synthesis-math");
    if (synthEl) {
      renderMathElement(DATA.project.synthesis_latex, synthEl, true);
    }

    // Equations list
    const eqContainer = document.getElementById("equations-container");
    DATA.equations.forEach((eq) => {
      const card = document.createElement("div");
      card.className = "formula-card";
      card.innerHTML = `
        <div class="formula-head">
          <span>${escapeHtml(eq.title)}</span>
          <span class="ref-chip" data-jump-node="${eq.node_ref}">İlgili Kod: ${eq.node_ref.toUpperCase()} ➔</span>
        </div>
        <div class="math-display" id="math-${eq.id}"></div>
        <p style="font-size:0.86rem;color:var(--center-muted);margin-top:0.45rem;">${escapeHtml(eq.desc)}</p>
      `;
      card.addEventListener("click", () => {
        selectNodeContext(eq.node_ref, false);
      });
      eqContainer.appendChild(card);
      renderMathElement(eq.latex, card.querySelector(`#math-${eq.id}`), true);
    });

    // Philosophy pillars
    const philContainer = document.getElementById("philosophy-container");
    DATA.philosophy_pillars.forEach((ph) => {
      const div = document.createElement("div");
      div.className = "phil-card";
      div.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">
          <h4>${escapeHtml(ph.title)}</h4>
          <span class="code-chip">${escapeHtml(ph.tag)}</span>
        </div>
        <p>${escapeHtml(ph.desc)}</p>
      `;
      philContainer.appendChild(div);
    });

    // Cognitive Nodes (Node 0 - Node 7)
    const nodesContainer = document.getElementById("nodes-container");
    DATA.nodes.forEach((n) => {
      const card = document.createElement("div");
      card.className = "node-card";
      card.id = n.id;

      const paperChips = n.papers
        .map((num) => {
          const p = notesByNum[num];
          const label = p ? `#${num} ${p.title.split(" (")[0].split(" - ")[0]}` : `#${num}`;
          return `<a class="ref-chip" href="#paper-${num}" data-paper-chip="${num}">${escapeHtml(label)}</a>`;
        })
        .join("");

      const classInfo = n.classes
        .map((c) => `${c.name}(${c.methods.join(", ")})`)
        .join(" | ");

      card.innerHTML = `
        <div class="node-card-top">
          <div>
            <span class="pill pill-${n.badge}" style="margin-bottom:0.35rem;display:inline-block;">${n.badge} • Mermaid: [${n.mermaid_id}]</span>
            <h3 class="node-card-title">${escapeHtml(n.title)}</h3>
          </div>
          <button class="inspect-btn" data-inspect-node="${n.id}">Python & Atıfları Yükle ➔</button>
        </div>
        <p style="font-size:0.9rem;margin-bottom:0.6rem;">${escapeHtml(n.summary)}</p>
        <div class="math-display" id="node-math-${n.num}"></div>
        <p style="font-size:0.83rem;color:var(--center-muted);margin:0.55rem 0;">
          <strong>Felsefi & Teorik Temel:</strong> ${escapeHtml(n.philosophy)}
        </p>
        <div class="meta-row">
          <span class="code-chip">📄 ${escapeHtml(n.repo_path)} (${n.line_count} satır)</span>
          ${classInfo ? `<span class="code-chip">⚙️ ${escapeHtml(classInfo)}</span>` : ""}
        </div>
        <div class="meta-row">
          <span style="font-size:0.76rem;color:var(--center-muted);font-weight:600;">Atıf Yapılan Çalışmalar:</span>
          ${paperChips}
        </div>
      `;

      nodesContainer.appendChild(card);
      renderMathElement(n.formula_latex, card.querySelector(`#node-math-${n.num}`), true);
    });

    // Literature & Study Notes (#01 - #20) grouped by Category
    const notesContainer = document.getElementById("notes-container");
    DATA.categories.forEach((cat) => {
      const catNotes = DATA.notes.filter((p) => p.category === cat);
      if (!catNotes.length) return;

      const catHeader = document.createElement("div");
      catHeader.className = "cat-divider";
      catHeader.textContent = cat;
      notesContainer.appendChild(catHeader);

      catNotes.forEach((p) => {
        const pCard = document.createElement("article");
        pCard.className = "paper-card";
        pCard.id = p.id;

        let actionBtns = "";
        if (p.pdf_rel_from_docs) {
          const szText = p.pdf_size_mb ? ` (${p.pdf_size_mb} MB)` : "";
          actionBtns += `<a class="ext-btn" href="${escapeHtml(p.pdf_rel_from_docs)}" target="_blank" rel="noopener">📄 Yerel PDF${escapeHtml(szText)}</a>`;
        }
        if (p.arxiv_url) {
          actionBtns += `<a class="ext-btn" href="${escapeHtml(p.arxiv_url)}" target="_blank" rel="noopener">🌐 arXiv</a>`;
        }
        if (p.sample_code) {
          actionBtns += `<button class="ext-btn" data-paper-code="${p.num}">🐍 Taslak Kodu Sağda Aç</button>`;
        }

        const nodeLinks = p.related_nodes
          .map((nr) => {
            const num = nr.replace("Node ", "").trim();
            return `<a class="ref-chip" href="#node-${num}" data-jump-node="node-${num}">${escapeHtml(nr)}</a>`;
          })
          .join("");

        const sectionsHtml = p.sections
          .map(
            (s) => `
            <div class="paper-sec">
              <h4>${escapeHtml(s.heading)}</h4>
              <div>${escapeHtml(s.prose)}</div>
            </div>
          `
          )
          .join("");

        pCard.innerHTML = `
          <div class="paper-head">
            <div>
              <span class="pill pill-PAPER" style="margin-bottom:0.3rem;display:inline-block;">ÇALIŞMA NOTU #${p.num}</span>
              <h3 class="paper-title">${escapeHtml(p.title)}</h3>
            </div>
            <div class="paper-links">${actionBtns}</div>
          </div>
          <div class="meta-row">
            <span style="font-size:0.76rem;color:var(--center-muted);font-weight:600;">Entegre Edildiği SENTINEL Düğümleri:</span>
            ${nodeLinks}
          </div>
          ${sectionsHtml}
        `;
        notesContainer.appendChild(pCard);
      });
    });

    // Delegate button clicks inside Center Pane
    document.querySelector(".center-pane").addEventListener("click", (e) => {
      const inspectBtn = e.target.closest("[data-inspect-node]");
      if (inspectBtn) {
        const nid = inspectBtn.getAttribute("data-inspect-node");
        selectNodeContext(nid, true);
        switchRightTab("code");
        return;
      }

      const jumpNode = e.target.closest("[data-jump-node]");
      if (jumpNode) {
        const nid = jumpNode.getAttribute("data-jump-node");
        selectNodeContext(nid, true);
        const el = document.getElementById(nid);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }

      const paperChip = e.target.closest("[data-paper-chip]");
      if (paperChip) {
        const num = paperChip.getAttribute("data-paper-chip");
        selectPaperContext(num, true);
        return;
      }

      const paperCodeBtn = e.target.closest("[data-paper-code]");
      if (paperCodeBtn) {
        const num = paperCodeBtn.getAttribute("data-paper-code");
        selectPaperContext(num, true);
        switchRightTab("code");
      }
    });
  }

  /* ------------------------------------------------------------------------
     3. RIGHT REDOC PANEL SYNCHRONIZATION
     ------------------------------------------------------------------------ */
  function populateNodeSelector() {
    const sel = document.getElementById("right-node-selector");
    DATA.nodes.forEach((n) => {
      const opt = document.createElement("option");
      opt.value = n.id;
      opt.textContent = `Node ${n.num} — ${n.file}`;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", () => {
      selectNodeContext(sel.value, false);
    });

    // Populate raw Mermaid code tab
    const mermaidRawEl = document.getElementById("raw-mermaid-code");
    mermaidRawEl.textContent = DATA.mermaid_diagram;
  }

  function highlightPythonCode(codeStr, pathLabel, metaRightText) {
    activeCodeText = codeStr;
    document.getElementById("code-filepath").textContent = pathLabel;
    document.getElementById("code-status").textContent = metaRightText;

    const codeEl = document.getElementById("right-code-block");
    codeEl.textContent = codeStr;
    codeEl.removeAttribute("data-highlighted");
    if (window.hljs) {
      window.hljs.highlightElement(codeEl);
    }
  }

  function renderCitationsList(paperNums) {
    const container = document.getElementById("right-citations-list");
    if (!paperNums || !paperNums.length) {
      container.innerHTML = `<p style="color:var(--right-muted);font-size:0.82rem;">Bu bölüm için bağlı makale bulunmuyor.</p>`;
      return;
    }

    container.innerHTML = paperNums
      .map((num) => {
        const p = notesByNum[num];
        if (!p) return "";
        const pdfBtn = p.pdf_rel_from_docs
          ? `<a class="cite-link" href="${escapeHtml(p.pdf_rel_from_docs)}" target="_blank" rel="noopener">📄 Yerel PDF (${p.pdf_size_mb || "?"} MB)</a>`
          : "";
        const arxivBtn = p.arxiv_url
          ? `<a class="cite-link" href="${escapeHtml(p.arxiv_url)}" target="_blank" rel="noopener">🌐 arXiv</a>`
          : "";
        return `
          <div class="cite-card">
            <div class="cite-card-head">
              <span class="cite-num">MAKALE / NOT #${p.num}</span>
              <span class="cite-cat">${escapeHtml(p.category)}</span>
            </div>
            <div class="cite-title">${escapeHtml(p.title)}</div>
            <div class="cite-actions">
              ${pdfBtn}
              ${arxivBtn}
              <a class="cite-link" href="#${p.id}" data-right-jump="${p.id}">📝 Çalışma Notuna Git</a>
            </div>
          </div>
        `;
      })
      .join("");

    container.querySelectorAll("[data-right-jump]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-right-jump");
        const num = targetId.replace("paper-", "");
        selectPaperContext(num, true);
      });
    });
  }

  function flashCardFocus(domId) {
    document.querySelectorAll(".focused-card").forEach((el) => el.classList.remove("focused-card"));
    const target = document.getElementById(domId);
    if (target) {
      target.classList.add("focused-card");
    }
  }

  function selectNodeContext(nodeId, highlightCard) {
    const node = nodesById[nodeId];
    if (!node) return;

    document.getElementById("right-ctx-type").textContent = `AKTİF MİMARİ DÜĞÜM // [${node.mermaid_id}]`;
    document.getElementById("right-ctx-title").textContent = node.title;
    document.getElementById("right-node-selector").value = node.id;

    highlightPythonCode(
      node.code,
      node.repo_path,
      `✓ AST Doğrulandı • ${node.line_count} satır`
    );
    renderCitationsList(node.papers);

    // Update citation tab counter
    document.getElementById("tab-cite-count").textContent = `(${node.papers.length})`;

    if (highlightCard) {
      flashCardFocus(node.id);
    }
  }

  function selectPaperContext(num, highlightCard) {
    const p = notesByNum[num];
    if (!p) return;

    document.getElementById("right-ctx-type").textContent = `AKTİF LİTERATÜR NOTU // #${p.num}`;
    document.getElementById("right-ctx-title").textContent = p.title;

    if (p.sample_code) {
      highlightPythonCode(
        p.sample_code,
        `${p.md_file} (Taslak Kod)`,
        `İlgili Düğümler: ${p.related_nodes.join(", ")}`
      );
    } else if (p.related_nodes.length) {
      const firstNodeNum = p.related_nodes[0].replace("Node ", "").trim();
      const linkedNode = nodesById[`node-${firstNodeNum}`];
      if (linkedNode) {
        document.getElementById("right-node-selector").value = linkedNode.id;
        highlightPythonCode(
          linkedNode.code,
          linkedNode.repo_path,
          `Bağlı Düğüm Kodu • #${p.num}`
        );
      }
    }

    renderCitationsList([p.num]);
    document.getElementById("tab-cite-count").textContent = `(1)`;

    if (highlightCard) {
      flashCardFocus(p.id);
    }
  }

  function switchRightTab(tabName) {
    document.querySelectorAll(".r-tab").forEach((t) => {
      t.classList.toggle("active", t.getAttribute("data-tab") === tabName);
    });
    document.querySelectorAll(".r-panel").forEach((p) => {
      p.classList.toggle("active", p.id === `panel-${tabName}`);
    });
  }

  /* ------------------------------------------------------------------------
     4. INTERACTIVE MERMAID RENDERING & CLICK-TO-JUMP
     ------------------------------------------------------------------------ */
  async function initMermaidDiagram() {
    const target = document.getElementById("mermaid-render-target");
    if (!window.mermaid) {
      target.innerHTML = `<pre style="color:#e2e8f0;font-size:0.78rem;">${escapeHtml(DATA.mermaid_diagram)}</pre>`;
      return;
    }

    try {
      window.mermaid.initialize({
        startOnLoad: false,
        theme: "dark",
        securityLevel: "loose",
        flowchart: {
          useMaxWidth: true,
          htmlLabels: true,
          curve: "basis",
        },
      });

      const { svg } = await window.mermaid.render("sentinel-mermaid-svg", DATA.mermaid_diagram);
      target.innerHTML = svg;

      // Bind interactive click events on Mermaid flowchart nodes
      const svgNodes = target.querySelectorAll(".node");
      svgNodes.forEach((gNode) => {
        const rawId = gNode.id || "";
        Object.keys(nodesByMermaidId).forEach((mKey) => {
          if (rawId.includes(`-${mKey}-`) || rawId.endsWith(`-${mKey}`)) {
            const matchedNode = nodesByMermaidId[mKey];
            gNode.classList.add("clickable-node");
            const titleEl = document.createElementNS("http://www.w3.org/2000/svg", "title");
            titleEl.textContent = `Tıkla: ${matchedNode.short_title} detayına ve Python koduna git`;
            gNode.appendChild(titleEl);

            gNode.addEventListener("click", () => {
              selectNodeContext(matchedNode.id, true);
              switchRightTab("code");
              const cardEl = document.getElementById(matchedNode.id);
              if (cardEl) {
                cardEl.scrollIntoView({ behavior: "smooth", block: "center" });
              }
            });
          }
        });
      });
    } catch (err) {
      console.error("Mermaid çizim hatası:", err);
      target.innerHTML = `<pre style="color:#e2e8f0;font-size:0.78rem;">${escapeHtml(DATA.mermaid_diagram)}</pre>`;
    }
  }

  /* ------------------------------------------------------------------------
     5. SEARCH, ZOOM, COPY, THEME & SCROLL-SPY
     ------------------------------------------------------------------------ */
  function bindToolbarAndEvents() {
    // Tabs
    document.querySelectorAll(".r-tab").forEach((btn) => {
      btn.addEventListener("click", () => switchRightTab(btn.getAttribute("data-tab")));
    });

    // Copy active Python code
    document.getElementById("btn-copy-code").addEventListener("click", function () {
      navigator.clipboard.writeText(activeCodeText || "").then(() => {
        const orig = this.textContent;
        this.textContent = "✓ Kopyalandı";
        setTimeout(() => (this.textContent = orig), 1400);
      });
    });

    // Copy raw Mermaid
    const copyMermaidAction = (btnEl) => {
      navigator.clipboard.writeText(DATA.mermaid_diagram).then(() => {
        const orig = btnEl.textContent;
        btnEl.textContent = "✓ Mermaid Kopyalandı";
        setTimeout(() => (btnEl.textContent = orig), 1400);
      });
    };
    document.getElementById("btn-copy-mermaid-top").addEventListener("click", function () {
      copyMermaidAction(this);
    });
    document.getElementById("btn-copy-mermaid-right").addEventListener("click", function () {
      copyMermaidAction(this);
    });

    // Zoom controls
    const mTarget = document.getElementById("mermaid-render-target");
    document.getElementById("btn-zoom-in").addEventListener("click", () => {
      currentScale = Math.min(1.8, currentScale + 0.15);
      mTarget.style.transform = `scale(${currentScale})`;
    });
    document.getElementById("btn-zoom-out").addEventListener("click", () => {
      currentScale = Math.max(0.55, currentScale - 0.15);
      mTarget.style.transform = `scale(${currentScale})`;
    });
    document.getElementById("btn-zoom-reset").addEventListener("click", () => {
      currentScale = 1.0;
      mTarget.style.transform = "scale(1)";
    });

    // Theme toggle
    const themeBtn = document.getElementById("btn-theme-toggle");
    const savedTheme = localStorage.getItem("sentinel_portal_theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
    themeBtn.textContent = savedTheme === "dark" ? "☀️ Açık" : "🌙 Koyu";

    themeBtn.addEventListener("click", () => {
      const cur = document.documentElement.getAttribute("data-theme");
      const next = cur === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("sentinel_portal_theme", next);
      themeBtn.textContent = next === "dark" ? "☀️ Açık" : "🌙 Koyu";
    });

    // Live Search Filter + `/` shortcut
    const searchInput = document.getElementById("sidebar-search");
    searchInput.addEventListener("input", () => {
      const q = searchInput.value.trim().toLowerCase();
      document.querySelectorAll(".nav-item").forEach((item) => {
        if (!q) {
          item.classList.remove("hidden");
          return;
        }
        const hay = (item.getAttribute("data-search") || "") + " " + item.textContent.toLowerCase();
        item.classList.toggle("hidden", !hay.includes(q));
      });
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
    });

    // IntersectionObserver Scroll-Spy for seamless Redoc synchronization
    const observedEls = document.querySelectorAll(".doc-section, .node-card, .paper-card");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const id = entry.target.id;
          if (!id) return;

          const navMatch = document.querySelector(`.nav-item[data-target="${id}"]`);
          if (navMatch) {
            document.querySelectorAll(".nav-item.active").forEach((el) => el.classList.remove("active"));
            navMatch.classList.add("active");
          }

          if (id.startsWith("node-")) {
            selectNodeContext(id, false);
          } else if (id.startsWith("paper-")) {
            selectPaperContext(id.replace("paper-", ""), false);
          }
        });
      },
      { rootMargin: "-15% 0px -70% 0px", threshold: 0.05 }
    );

    observedEls.forEach((el) => observer.observe(el));
  }

  /* ------------------------------------------------------------------------
     INIT
     ------------------------------------------------------------------------ */
  document.addEventListener("DOMContentLoaded", () => {
    buildLeftSidebar();
    populateNodeSelector();
    buildCenterContent();
    selectNodeContext("node-1", false); // Default start on Node 1: Metacognitive Controller
    initMermaidDiagram();
    bindToolbarAndEvents();
  });
})();

