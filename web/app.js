/* Pack 1500 — galerie interactive */
(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const PER_PAGE = 24;
  const SLIDE_LABELS = ["Couverture", "Sommaire", "Transition", "Vision", "Chiffres clés",
    "Données", "Processus", "Équipe", "Citation", "Clôture"];
  const MODE_LABEL = { light: "Clair", dark: "Sombre" };

  const state = {
    data: null,
    templates: [],
    filtered: [],
    page: 1,
    favorites: new Set(JSON.parse(localStorage.getItem("pack1500:favs") || "[]")),
    favOnly: false,
    selected: null,
    slide: 0,
    packReady: false,
    packTimer: null,
  };

  const norm = (s) => (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = (n) => new Intl.NumberFormat("fr-FR").format(n);

  async function load() {
    try {
      const data = await fetch("/api/catalog").then((r) => r.json());
      state.data = data;
      state.templates = data.templates;
      initFilters(data.meta);
      bindEvents();
      applyFilters();
      initPackStatus();
    } catch (err) {
      $("grid").innerHTML = `<div class="empty">Impossible de charger le catalogue : ${esc(err.message)}</div>`;
    }
  }

  function fillSelect(id, values, labels) {
    const el = $(id);
    values.forEach((v) => {
      const opt = document.createElement("option");
      opt.value = v;
      opt.textContent = labels ? (labels[v] || v) : v;
      el.appendChild(opt);
    });
  }

  function initFilters(meta) {
    fillSelect("fUnivers", meta.univers);
    fillSelect("fMotif", meta.motifs);
    fillSelect("fTypo", meta.typos);
    fillSelect("fHue", meta.hues);
  }

  function bindEvents() {
    ["search", "fUnivers", "fMode", "fMotif", "fTypo", "fHue", "fSort"].forEach((id) => {
      $(id).addEventListener(id === "search" ? "input" : "change", () => {
        state.page = 1;
        applyFilters();
      });
    });
    $("favToggle").addEventListener("click", () => {
      state.favOnly = !state.favOnly;
      state.page = 1;
      $("favToggle").classList.toggle("active", state.favOnly);
      applyFilters();
    });
    const reset = () => {
      ["fUnivers", "fMode", "fMotif", "fTypo", "fHue"].forEach((id) => ($(id).value = ""));
      $("fSort").value = "popular";
      $("search").value = "";
      state.favOnly = false;
      $("favToggle").classList.remove("active");
      state.page = 1;
      applyFilters();
    };
    $("resetFilters").addEventListener("click", reset);
    $("emptyReset").addEventListener("click", reset);

    $("grid").addEventListener("click", (e) => {
      const fav = e.target.closest(".fav-btn");
      if (fav) {
        toggleFav(fav.dataset.id);
        e.stopPropagation();
        return;
      }
      const action = e.target.closest("[data-action]");
      if (!action) return;
      const id = action.dataset.id;
      if (action.dataset.action === "download") {
        window.location.href = `/api/download/${id}.pptx`;
        toast(`Téléchargement de ${id}…`);
      } else {
        openModal(id);
      }
    });

    ["headerPackBtn", "heroPackBtn", "footerPackBtn"].forEach((id) =>
      $(id).addEventListener("click", handlePackClick));

    document.querySelectorAll("[data-close]").forEach((el) =>
      el.addEventListener("click", closeModal));
    $("mDownload").addEventListener("click", () => {
      if (!state.selected) return;
      window.location.href = `/api/download/${state.selected.id}.pptx`;
      toast(`Téléchargement de ${state.selected.id}…`);
    });
    $("mFav").addEventListener("click", () => {
      if (!state.selected) return;
      toggleFav(state.selected.id);
      updateFavButton();
    });
    $("slideStrip").addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-slide]");
      if (btn) setSlide(Number(btn.dataset.slide));
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
      if (!$("modal").hidden && (e.key === "ArrowRight" || e.key === "ArrowLeft")) {
        setSlide(state.slide + (e.key === "ArrowRight" ? 1 : -1));
      }
      if (e.key === "/" && document.activeElement.tagName !== "INPUT" &&
          document.activeElement.tagName !== "SELECT") {
        e.preventDefault();
        $("search").focus();
      }
    });
  }

  function filterValues() {
    return {
      q: norm($("search").value.trim()),
      univers: $("fUnivers").value,
      mode: $("fMode").value,
      motif: $("fMotif").value,
      typo: $("fTypo").value,
      hue: $("fHue").value,
      sort: $("fSort").value,
    };
  }

  function applyFilters() {
    const f = filterValues();
    let list = state.templates.filter((t) => {
      if (f.q && !norm(t.search).includes(f.q)) return false;
      if (f.univers && t.univers !== f.univers) return false;
      if (f.mode && t.mode !== f.mode) return false;
      if (f.motif && t.motif !== f.motif) return false;
      if (f.typo && t.typo_label !== f.typo) return false;
      if (f.hue && t.hue !== f.hue) return false;
      if (state.favOnly && !state.favorites.has(t.id)) return false;
      return true;
    });
    const cmp = {
      popular: (a, b) => b.popularity - a.popularity || a.number - b.number,
      number: (a, b) => a.number - b.number,
      name: (a, b) => a.name.localeCompare(b.name, "fr"),
      family: (a, b) => a.family.localeCompare(b.family, "fr") || a.number - b.number,
    }[f.sort];
    list = list.slice().sort(cmp);
    state.filtered = list;
    const pages = Math.max(1, Math.ceil(list.length / PER_PAGE));
    state.page = Math.min(state.page, pages);
    renderGrid();
    renderPagination(pages);
    $("resultCount").textContent = fmt(list.length);
    $("favCount").textContent = state.favorites.size;
  }

  function renderGrid() {
    const start = (state.page - 1) * PER_PAGE;
    const items = state.filtered.slice(start, start + PER_PAGE);
    $("empty").hidden = items.length > 0;
    $("grid").innerHTML = items.map((t) => `
      <article class="card">
        <div class="card-preview">
          <img src="/api/thumb/${t.id}.svg?slide=0" alt="Aperçu de ${esc(t.name)}" loading="lazy">
          <div class="card-badges">
            <span class="badge">${esc(t.univers)}</span>
            <span class="badge">${MODE_LABEL[t.mode]}</span>
            <span class="badge badge-pro">✦ Animé · 4 images</span>
          </div>
          <button class="fav-btn ${state.favorites.has(t.id) ? "on" : ""}" data-id="${t.id}"
                  title="Ajouter aux favoris" aria-label="Favori">${state.favorites.has(t.id) ? "♥" : "♡"}</button>
          <div class="card-overlay">
            <button data-action="preview" data-id="${t.id}">Aperçu des 10 slides</button>
            <button class="secondary" data-action="download" data-id="${t.id}">↓ .pptx</button>
          </div>
        </div>
        <div class="card-body">
          <h3 class="card-name" title="${esc(t.name)}">${esc(t.name)}</h3>
          <div class="card-meta">
            <span>${esc(t.typo_label)} · ${esc(t.motif)}</span>
            <span class="id">${t.id}</span>
          </div>
        </div>
      </article>`).join("");
  }

  function renderPagination(pages) {
    const p = state.page;
    const nums = [];
    const from = Math.max(1, Math.min(p - 2, pages - 4));
    const to = Math.min(pages, from + 4);
    for (let i = from; i <= to; i++) nums.push(i);
    let html = `<button data-page="${p - 1}" ${p === 1 ? "disabled" : ""}>←</button>`;
    if (from > 1) html += `<button data-page="1">1</button>${from > 2 ? "<span>…</span>" : ""}`;
    nums.forEach((n) => (html += `<button data-page="${n}" class="${n === p ? "active" : ""}">${n}</button>`));
    if (to < pages) html += `${to < pages - 1 ? "<span>…</span>" : ""}<button data-page="${pages}">${pages}</button>`;
    html += `<button data-page="${p + 1}" ${p === pages ? "disabled" : ""}>→</button>`;
    const box = $("pagination");
    box.innerHTML = html;
    box.onclick = (e) => {
      const b = e.target.closest("button[data-page]");
      if (!b || b.disabled) return;
      state.page = Number(b.dataset.page);
      renderGrid();
      renderPagination(Math.max(1, Math.ceil(state.filtered.length / PER_PAGE)));
      document.getElementById("galerie").scrollIntoView({ behavior: "smooth", block: "start" });
    };
  }

  function toggleFav(id) {
    if (state.favorites.has(id)) state.favorites.delete(id);
    else state.favorites.add(id);
    localStorage.setItem("pack1500:favs", JSON.stringify([...state.favorites]));
    $("favCount").textContent = state.favorites.size;
    const btn = document.querySelector(`.fav-btn[data-id="${id}"]`);
    if (btn) {
      const on = state.favorites.has(id);
      btn.classList.toggle("on", on);
      btn.textContent = on ? "♥" : "♡";
    }
    if (state.favOnly) applyFilters();
    if (state.selected && state.selected.id === id) updateFavButton();
  }

  function updateFavButton() {
    const on = state.favorites.has(state.selected.id);
    $("mFav").textContent = on ? "♥ Dans les favoris" : "♡ Ajouter aux favoris";
    $("mFav").classList.toggle("active", on);
  }

  function findTemplate(id) {
    return state.templates.find((t) => t.id === id);
  }

  function openModal(id) {
    const t = findTemplate(id);
    if (!t) return;
    state.selected = t;
    $("mId").textContent = `${t.id}  ·  MODÈLE ${fmt(t.number)} / 1 500`;
    $("mName").textContent = t.name;
    $("mDesc").textContent = t.description;
    $("mTags").innerHTML = [t.univers, MODE_LABEL[t.mode], t.typo_label, t.motif, t.hue]
      .map((x) => `<span>${esc(x)}</span>`).join("");
    const swatchKeys = ["bg", "surface", "soft", "accent", "accent2", "ink"];
    $("mSwatches").innerHTML = swatchKeys.map((k) =>
      `<div style="background:${t.colors[k]}" title="${k}: ${t.colors[k]}"><span>${k}</span></div>`).join("");
    $("mMeta").innerHTML = [
      ["Famille", t.family], ["Palette", t.palette], ["Mise en page", t.archetype],
      ["Densité", t.density], ["Format", "16:9 · 13,33 × 7,5 po"], ["Slides", "10 + notes"],
      ["Animations", "Transitions + fondus"], ["Images", "4 remplaçables"],
      ["Design", "10 empreintes uniques"], ["Signature", `${t.id} · 8 paramètres`],
    ].map(([k, v]) => `<div><small>${k}</small><strong>${esc(v)}</strong></div>`).join("");
    $("mSlides").innerHTML = SLIDE_LABELS.map((l, i) =>
      `<span><b>${String(i + 1).padStart(2, "0")}</b>${l}</span>`).join("");
    $("slideStrip").innerHTML = SLIDE_LABELS.map((l, i) =>
      `<button data-slide="${i}" title="${l}"><img src="/api/thumb/${t.id}.svg?slide=${i}" loading="lazy" alt="${l}"></button>`).join("");
    updateFavButton();
    setSlide(0);
    $("modal").hidden = false;
    document.body.style.overflow = "hidden";
  }

  function setSlide(n) {
    if (!state.selected) return;
    state.slide = (n + 10) % 10;
    $("modalSlide").src = `/api/thumb/${state.selected.id}.svg?slide=${state.slide}`;
    $("modalSlide").alt = `${state.selected.name} — ${SLIDE_LABELS[state.slide]}`;
    document.querySelectorAll("#slideStrip button").forEach((b) =>
      b.classList.toggle("active", Number(b.dataset.slide) === state.slide));
  }

  function closeModal() {
    $("modal").hidden = true;
    document.body.style.overflow = "";
    state.selected = null;
  }

  let toastTimer;
  function toast(msg) {
    const el = $("toast");
    el.textContent = msg;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (el.hidden = true), 2600);
  }

  /* ---------------- archive complète ---------------- */
  function updatePackUI(st) {
    const box = $("packProgress");
    const pct = st.percent != null ? st.percent : Math.round(100 * st.done / st.total);
    if (st.ready) {
      state.packReady = true;
      box.hidden = true;
      const mb = st.zip_bytes ? ` · ${(st.zip_bytes / 1048576).toFixed(0)} Mio` : "";
      $("heroPackBtn").innerHTML = `Télécharger les 1 500 modèles${mb} <span>↓</span>`;
      return true;
    }
    box.hidden = false;
    $("packProgressLabel").textContent = st.stage === "compression"
      ? "Finalisation de l'archive…" : `Génération : ${fmt(st.done)} / ${fmt(st.total)} modèles`;
    $("packProgressPct").textContent = `${pct} %`;
    $("packProgressBar").style.width = `${pct}%`;
    return false;
  }

  async function initPackStatus() {
    try {
      const st = await fetch("/api/pack/status").then((r) => r.json());
      if (!updatePackUI(st)) startPolling();
    } catch (_) { /* le serveur redémarre peut-être */ }
  }

  function startPolling() {
    if (state.packTimer) return;
    state.packTimer = setInterval(async () => {
      try {
        const st = await fetch("/api/pack/status").then((r) => r.json());
        if (updatePackUI(st)) {
          clearInterval(state.packTimer);
          state.packTimer = null;
          toast("Le pack complet est prêt !");
        }
      } catch (_) { /* on réessaiera */ }
    }, 1800);
  }

  async function handlePackClick() {
    if (state.packReady) {
      window.location.href = "/api/pack";
      toast("Téléchargement de l'archive…");
      return;
    }
    try {
      await fetch("/api/pack/start");
      startPolling();
      toast("Génération des 1 500 modèles en cours…");
      $("packProgress").scrollIntoView({ behavior: "smooth", block: "center" });
    } catch (_) {
      toast("Impossible de lancer la génération.");
    }
  }

  load();
})();
