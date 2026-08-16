/**
 * NDMC Smart Grievance AI Workbench - Client Application Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initTriageModule();
  initStormLab();
  initChatbot();
  initBenchmarkModule();
  loadTaxonomy();
});

// ----------------- Tab Navigation -----------------
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  const panes = document.querySelectorAll(".tab-pane");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      panes.forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      const targetPane = document.getElementById(`tab-${tab.dataset.tab}`);
      if (targetPane) targetPane.classList.add("active");
    });
  });
}

// ----------------- Tab 1: AI Triage Sandbox -----------------
function initTriageModule() {
  const btnAnalyze = document.getElementById("btn-analyze");
  const txtInput = document.getElementById("complaint-text");
  const selWard = document.getElementById("select-ward");
  const sampleChips = document.querySelectorAll(".sample-chip[data-sample]");

  sampleChips.forEach(chip => {
    chip.addEventListener("click", () => {
      txtInput.value = chip.dataset.sample;
      triggerAnalysis();
    });
  });

  btnAnalyze.addEventListener("click", () => {
    triggerAnalysis();
  });

  async function triggerAnalysis() {
    const text = txtInput.value.trim();
    if (!text) {
      alert("Please enter a complaint description to analyze.");
      return;
    }

    btnAnalyze.disabled = true;
    btnAnalyze.innerText = "⏳ Processing AI Triage...";

    try {
      const response = await fetch("/api/ai/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          ward: selWard.value || null,
          check_duplicates: true
        })
      });

      const data = await response.json();
      renderAnalysisResults(data);
    } catch (err) {
      console.error("Analysis failed:", err);
      alert("Failed to analyze grievance. Please check backend connection.");
    } finally {
      btnAnalyze.disabled = false;
      btnAnalyze.innerText = "⚡ Run Unified AI Analysis (Classify + Priority + Hazard + Duplicates)";
    }
  }

  function renderAnalysisResults(data) {
    document.getElementById("res-title").innerText = data.title || "Complaint Analysis";
    
    // Priority Badge
    const prioBadge = document.getElementById("res-priority-badge");
    const tier = data.priority.tier.toUpperCase();
    let badgeClass = "badge-low";
    if (tier === "CRITICAL") badgeClass = "badge-critical";
    else if (tier === "HIGH") badgeClass = "badge-high";
    else if (tier === "MEDIUM") badgeClass = "badge-medium";

    prioBadge.innerHTML = `<span class="badge ${badgeClass}">⚡ ${tier} PRIORITY</span>`;

    // Stats Grid
    document.getElementById("res-dept").innerText = data.classification.department_name;
    document.getElementById("res-cat").innerText = data.classification.category;
    document.getElementById("res-conf").innerText = `${Math.round(data.classification.confidence * 100)}%`;
    document.getElementById("res-sla").innerText = `${data.priority.sla_hours} Hours`;

    // Hazard Alert
    const hazardBox = document.getElementById("res-hazard-alert");
    const hazardText = document.getElementById("res-hazard-text");
    if (data.priority.is_safety_hazard) {
      hazardBox.style.display = "block";
      hazardText.innerText = data.priority.rationale;
    } else {
      hazardBox.style.display = "none";
    }

    // Top Candidates
    const candContainer = document.getElementById("res-top-candidates");
    candContainer.innerHTML = "";
    (data.classification.top_candidates || []).forEach(cand => {
      const row = document.createElement("div");
      row.style.display = "flex";
      row.style.justifyContent = "space-between";
      row.style.background = "rgba(15, 23, 42, 0.5)";
      row.style.padding = "0.4rem 0.6rem";
      row.style.borderRadius = "6px";
      row.innerHTML = `
        <span>${cand.department_name}</span>
        <span style="font-weight: 700; color: var(--accent-cyan);">${Math.round(cand.confidence * 100)}%</span>
      `;
      candContainer.appendChild(row);
    });

    // Duplicate Box
    const dupBox = document.getElementById("res-duplicate-box");
    if (data.duplicates && data.duplicates.is_duplicate) {
      dupBox.style.borderColor = "var(--accent-amber)";
      dupBox.style.background = "rgba(245, 158, 11, 0.1)";
      dupBox.innerHTML = `
        <div style="font-weight: 700; color: var(--accent-amber);">⚠️ Possible Duplicate Detected (${Math.round(data.duplicates.highest_similarity * 100)}% Match)</div>
        <div style="margin-top: 0.25rem; font-size: 0.8rem;">Linked to ticket <strong>#${data.duplicates.primary_match.complaint_id}</strong> in ${data.duplicates.primary_match.ward}</div>
      `;
    } else {
      dupBox.style.borderColor = "var(--border-glass)";
      dupBox.style.background = "rgba(15, 23, 42, 0.6)";
      dupBox.innerHTML = `✅ No active duplicates found nearby. Safe to register as a fresh ticket.`;
    }

    // Raw JSON
    const rawBox = document.getElementById("res-raw-json");
    rawBox.style.display = "block";
    document.getElementById("res-json-content").innerText = JSON.stringify(data, null, 2);
  }
}

// ----------------- Tab 2: Duplicate & Storm Lab -----------------
function initStormLab() {
  const btnRunStorm = document.getElementById("btn-run-storm");
  const stormCount = document.getElementById("storm-count");
  const stormWard = document.getElementById("storm-ward");
  const stormResultsBox = document.getElementById("storm-results-box");

  btnRunStorm.addEventListener("click", async () => {
    btnRunStorm.disabled = true;
    btnRunStorm.innerText = "⏳ Simulating Storm Burst...";

    try {
      const res = await fetch("/api/ai/duplicates/simulate-storm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          count: parseInt(stormCount.value, 10) || 50,
          ward: stormWard.value
        })
      });

      const data = await res.json();
      stormResultsBox.innerHTML = `
        <div style="padding: 1rem; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: var(--radius-md); margin-bottom: 1rem;">
          <div style="font-size: 1rem; font-weight: 700; color: var(--accent-emerald);">✅ Surge Clustered Successfully!</div>
          <div style="margin-top: 0.5rem;">Simulated <strong>${data.total_simulated_complaints}</strong> concurrent complaints during monsoon waterlogging.</div>
        </div>
        <div class="stat-grid">
          <div class="stat-box">
            <div class="stat-label">Master Incident Ticket</div>
            <div class="stat-value" style="font-size: 1rem; color: var(--accent-cyan);">#${data.master_ticket_id}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Cluster Size</div>
            <div class="stat-value">${data.cluster_size} Complaints</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Top Similarity</div>
            <div class="stat-value">${Math.round(data.top_match_similarity * 100)}%</div>
          </div>
        </div>
        <p style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-muted);">
          All ${data.total_simulated_complaints} burst complaints from ${data.ward} were consolidated into 1 Master Incident dispatch for the Disaster Management team, preventing ${data.total_simulated_complaints - 1} duplicate field dispatches!
        </p>
      `;
    } catch (err) {
      console.error(err);
      stormResultsBox.innerHTML = `<span style="color: var(--accent-rose);">Error running simulation.</span>`;
    } finally {
      btnRunStorm.disabled = false;
      btnRunStorm.innerText = "⚡ Trigger 50-Complaint Storm Burst Simulation";
    }
  });
}

// ----------------- Tab 3: Citizen AI Chatbot -----------------
function initChatbot() {
  const container = document.getElementById("chat-messages-container");
  const input = document.getElementById("chat-input-field");
  const btnSend = document.getElementById("btn-send-chat");
  const btnReset = document.getElementById("btn-reset-chat");

  let history = [];

  function appendMessage(text, isUser = false, actions = []) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${isUser ? 'user' : 'bot'}`;
    bubble.innerHTML = text.replace(/\n/g, "<br>");

    if (actions && actions.length > 0 && !isUser) {
      const actionsDiv = document.createElement("div");
      actionsDiv.className = "chat-actions";
      actions.forEach(act => {
        const btn = document.createElement("button");
        btn.className = "sample-chip";
        btn.innerText = act.label;
        btn.addEventListener("click", () => {
          sendMessage(act.label);
        });
        actionsDiv.appendChild(btn);
      });
      bubble.appendChild(actionsDiv);
    }

    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
  }

  async function sendMessage(msgText) {
    const text = msgText || input.value.trim();
    if (!text) return;

    input.value = "";
    appendMessage(text, true);
    history.push({ role: "user", content: text });

    try {
      const res = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          conversation_history: history
        })
      });

      const data = await res.json();
      history.push({ role: "assistant", content: data.reply });
      appendMessage(data.reply, false, data.action_buttons);
    } catch (err) {
      console.error(err);
      appendMessage("⚠️ Sorry, I encountered an error communicating with the NDMC AI service.", false);
    }
  }

  btnSend.addEventListener("click", () => sendMessage());
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  btnReset.addEventListener("click", () => {
    history = [];
    container.innerHTML = `
      <div class="chat-bubble bot">
        Namaste! 🙏 Welcome to the <strong>NDMC Smart Grievance Assistant</strong>.<br><br>
        How may I help you today?
      </div>
    `;
  });

  // Delegate quick buttons
  container.addEventListener("click", (e) => {
    if (e.target.classList.contains("chat-quick-btn")) {
      sendMessage(e.target.dataset.msg);
    }
  });
}

// ----------------- Tab 4: Benchmarks -----------------
function initBenchmarkModule() {
  const btn = document.getElementById("btn-run-benchmark");

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.innerText = "⏳ Running Benchmarks on 64 Cases...";

    try {
      const res = await fetch("/api/ai/benchmarks");
      const data = await res.json();

      document.getElementById("bench-dept-acc").innerText = data.department_classification_accuracy;
      document.getElementById("bench-prio-acc").innerText = data.priority_accuracy;
      document.getElementById("bench-haz-acc").innerText = data.safety_hazard_detection_accuracy;
      document.getElementById("bench-latency").innerText = `${(data.execution_time_seconds / data.dataset_size * 1000).toFixed(2)} ms`;

      const langGrid = document.getElementById("bench-lang-grid");
      langGrid.innerHTML = `
        <div class="stat-box">
          <div class="stat-label">English (EN)</div>
          <div class="stat-value" style="font-size: 1.1rem; color: var(--accent-emerald);">${data.language_accuracy.english}</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Hindi Devanagari (HI)</div>
          <div class="stat-value" style="font-size: 1.1rem; color: var(--accent-emerald);">${data.language_accuracy.hindi}</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Hinglish Code-Mixed</div>
          <div class="stat-value" style="font-size: 1.1rem; color: var(--accent-emerald);">${data.language_accuracy.hinglish}</div>
        </div>
      `;
    } catch (err) {
      console.error(err);
      alert("Failed to run live benchmarks.");
    } finally {
      btn.disabled = false;
      btn.innerText = "▶️ Run Live Benchmark Evaluation";
    }
  });
}

// ----------------- Tab 5: Taxonomy -----------------
async function loadTaxonomy() {
  const grid = document.getElementById("taxonomy-grid");
  const search = document.getElementById("taxonomy-search");

  try {
    const res = await fetch("/api/ai/taxonomy");
    const data = await res.json();
    const depts = data.departments || [];

    function renderDepts(items) {
      grid.innerHTML = "";
      items.forEach(dept => {
        const card = document.createElement("div");
        card.className = "stat-box";
        card.style.background = "rgba(15, 23, 42, 0.7)";
        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <div style="font-weight: 700; font-size: 1rem; color: var(--accent-cyan);">${dept.name}</div>
            <span class="badge badge-medium" style="font-size: 0.65rem;">${dept.code}</span>
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.75rem;">${dept.description}</p>
          <div style="font-size: 0.75rem; font-weight: 600; color: var(--text-dim); margin-bottom: 0.35rem;">SUB-CATEGORIES:</div>
          <ul style="font-size: 0.75rem; color: var(--text-main); margin-left: 1.2rem; margin-bottom: 0.75rem;">
            ${(dept.sub_categories || []).slice(0, 4).map(s => `<li>${s}</li>`).join("")}
          </ul>
          <div style="display: flex; justify-content: space-between; font-size: 0.75rem; border-top: 1px solid var(--border-glass); padding-top: 0.5rem; color: var(--accent-amber);">
            <span>Citizen SLA Target:</span>
            <strong>${dept.sla_hours_default} Hours</strong>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    renderDepts(depts);

    search.addEventListener("input", (e) => {
      const q = e.target.value.toLowerCase();
      const filtered = depts.filter(d => 
        d.name.toLowerCase().includes(q) || 
        d.description.toLowerCase().includes(q) ||
        (d.sub_categories || []).some(s => s.toLowerCase().includes(q))
      );
      renderDepts(filtered);
    });

  } catch (err) {
    console.error("Failed to load taxonomy:", err);
  }
}
