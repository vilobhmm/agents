/**
 * AI Agents Trend Radar — Dashboard Client
 *
 * Handles data loading, tab switching, filtering, search,
 * and rendering of recommendations, trending feed, topic analysis,
 * and source-grouped views.
 */

// ═══ State ═══════════════════════════════════════════════════════
let DATA = null;
let activeTab = "recommendations";
let activeFilter = null;
let searchQuery = "";

// ═══ Init ════════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
    initParticles();
    initTabs();
    initSearch();
    initRefresh();
    loadData();
});

// ═══ Background particles ════════════════════════════════════════
function initParticles() {
    const container = document.getElementById("particles");
    const colors = ["#6C63FF", "#3B82F6", "#06B6D4", "#8B5CF6", "#EC4899"];
    for (let i = 0; i < 30; i++) {
        const p = document.createElement("div");
        p.className = "particle";
        const size = Math.random() * 6 + 2;
        const color = colors[Math.floor(Math.random() * colors.length)];
        const left = Math.random() * 100;
        const duration = Math.random() * 20 + 15;
        const delay = Math.random() * -30;
        Object.assign(p.style, {
            width: `${size}px`,
            height: `${size}px`,
            left: `${left}%`,
            background: color,
            animationDuration: `${duration}s`,
            animationDelay: `${delay}s`,
        });
        container.appendChild(p);
    }
}

// ═══ Tabs ════════════════════════════════════════════════════════
function initTabs() {
    document.querySelectorAll(".tab").forEach((btn) => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            activeTab = btn.dataset.tab;
            render();
        });
    });
}

// ═══ Search ══════════════════════════════════════════════════════
function initSearch() {
    const input = document.getElementById("searchInput");
    let timer;
    input.addEventListener("input", () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            searchQuery = input.value.trim().toLowerCase();
            render();
        }, 250);
    });
}

// ═══ Refresh ═════════════════════════════════════════════════════
function initRefresh() {
    document.getElementById("btnRefresh").addEventListener("click", () => {
        loadData();
    });
}

// ═══ Data Loading ════════════════════════════════════════════════
async function loadData() {
    const btn = document.getElementById("btnRefresh");
    btn.classList.add("spinning");
    showLoading();

    try {
        const resp = await fetch("/api/data");
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        DATA = await resp.json();
        populateStats();
        populateFilters();
        render();
    } catch (err) {
        console.error("Failed to load data:", err);
        showError("Failed to load data. Make sure the server is running.");
    } finally {
        btn.classList.remove("spinning");
    }
}

// ═══ Stats ═══════════════════════════════════════════════════════
function populateStats() {
    if (!DATA) return;
    const feed = DATA.curated_feed || {};
    const recs = DATA.recommendations || {};
    const meta = DATA.metadata || {};
    const sb = feed.source_breakdown || {};

    setText("statTopics", feed.total_topics || 0);
    setText("statItems", feed.total_items || 0);
    setText("statRecs", recs.total_recommendations || 0);
    setText("statSources", Object.keys(sb).length || 0);
    setText("statDuration", meta.pipeline_duration_seconds ?? "—");
}

// ═══ Filters ═════════════════════════════════════════════════════
function populateFilters() {
    if (!DATA) return;
    const container = document.getElementById("filterChips");
    container.innerHTML = "";

    // Collect unique topics
    const topics = new Set();
    (DATA.analyses || []).forEach((a) => topics.add(a.topic));

    // "All" chip
    const allChip = makeChip("All", !activeFilter);
    allChip.addEventListener("click", () => { activeFilter = null; render(); populateFilters(); });
    container.appendChild(allChip);

    topics.forEach((t) => {
        const chip = makeChip(t, activeFilter === t);
        chip.addEventListener("click", () => {
            activeFilter = activeFilter === t ? null : t;
            render();
            populateFilters();
        });
        container.appendChild(chip);
    });
}

function makeChip(label, isActive) {
    const el = document.createElement("button");
    el.className = `chip${isActive ? " active" : ""}`;
    el.textContent = label;
    return el;
}

// ═══ Render Router ═══════════════════════════════════════════════
function render() {
    if (!DATA) return;
    const container = document.getElementById("tabContent");
    container.innerHTML = "";

    switch (activeTab) {
        case "recommendations":
            renderRecommendations(container);
            break;
        case "trending":
            renderTrending(container);
            break;
        case "topics":
            renderTopics(container);
            break;
        case "sources":
            renderSources(container);
            break;
    }

    // Scroll-reveal animation
    requestAnimationFrame(() => {
        container.querySelectorAll(".reveal").forEach((el, i) => {
            setTimeout(() => el.classList.add("visible"), i * 60);
        });
    });
}

// ═══ Recommendations Tab ═════════════════════════════════════════
function renderRecommendations(container) {
    const recs = (DATA.recommendations?.recommendations || []).filter(filterAndSearch);
    if (!recs.length) return renderEmpty(container, "💡", "No recommendations", "Try adjusting your filters.");

    const grid = document.createElement("div");
    grid.className = "rec-grid";

    recs.forEach((rec) => {
        const card = document.createElement("div");
        card.className = "rec-card glass-card reveal";
        card.dataset.reading = rec.reading_level || "intermediate";

        card.innerHTML = `
            <div class="rec-rank">${rec.rank}</div>
            <div class="rec-title"><a href="${esc(rec.url)}" target="_blank" rel="noopener">${esc(rec.title)}</a></div>
            <div class="rec-meta">
                <span class="rec-badge badge-source">${esc(rec.source)}</span>
                <span class="rec-badge badge-topic">${esc(rec.topic)}</span>
                <span class="rec-badge badge-level-${rec.reading_level || 'intermediate'}">${esc(rec.reading_level || 'intermediate')}</span>
            </div>
            <div class="rec-why">${esc(rec.why_read)}</div>
            <div class="rec-score-bar"><div class="rec-score-fill" style="width:${(rec.score * 100).toFixed(0)}%"></div></div>
        `;
        grid.appendChild(card);
    });

    container.appendChild(grid);
}

// ═══ Trending Feed Tab ═══════════════════════════════════════════
function renderTrending(container) {
    const items = (DATA.curated_feed?.top_items || []).filter(filterAndSearch);
    if (!items.length) return renderEmpty(container, "🔥", "No trending items", "Adjust filters or refresh.");

    const list = document.createElement("div");
    list.className = "trending-list";

    items.forEach((item) => {
        const el = document.createElement("div");
        el.className = "trending-item glass-card reveal";
        el.innerHTML = `
            <div class="trending-score">
                <div class="trending-score-value">${(item.score * 100).toFixed(0)}</div>
                <div class="trending-score-label">Score</div>
            </div>
            <div class="trending-body">
                <div class="trending-title">
                    <a href="${esc(item.url)}" target="_blank" rel="noopener">${esc(item.title)}</a>
                </div>
                <div class="rec-meta" style="margin-bottom:0.3rem">
                    <span class="rec-badge badge-source">${esc(item.source)}</span>
                    ${(item.tags || []).slice(0, 2).map(t => `<span class="rec-badge badge-topic">${esc(t)}</span>`).join("")}
                </div>
                <div class="trending-summary">${esc(item.summary || "")}</div>
            </div>
        `;
        list.appendChild(el);
    });

    container.appendChild(list);
}

// ═══ Topics Tab ══════════════════════════════════════════════════
function renderTopics(container) {
    const analyses = (DATA.analyses || []).filter((a) => {
        if (activeFilter && a.topic !== activeFilter) return false;
        if (searchQuery && !a.topic.toLowerCase().includes(searchQuery) && !a.summary.toLowerCase().includes(searchQuery)) return false;
        return true;
    });
    if (!analyses.length) return renderEmpty(container, "📊", "No topics", "Adjust filters.");

    const grid = document.createElement("div");
    grid.className = "topic-grid";

    analyses.forEach((a) => {
        const card = document.createElement("div");
        card.className = "topic-card glass-card reveal";
        card.innerHTML = `
            <div class="topic-header">
                <div class="topic-name">${esc(a.topic)}</div>
                <div class="topic-heat">
                    <span>${(a.heat_score * 100).toFixed(0)}%</span>
                    <div class="topic-heat-bar">
                        <div class="topic-heat-fill" style="width:${(a.heat_score * 100).toFixed(0)}%"></div>
                    </div>
                </div>
            </div>
            <div class="rec-meta" style="margin-bottom:0.5rem">
                <span class="rec-badge badge-source">${a.item_count} items</span>
                <span class="rec-badge badge-level-${a.reading_level || 'intermediate'}">${esc(a.reading_level || 'intermediate')}</span>
            </div>
            <div class="topic-summary">${esc(a.summary)}</div>
            ${a.key_developments?.length ? `
                <ul class="topic-developments">
                    ${a.key_developments.slice(0, 4).map(d => `<li>${esc(d)}</li>`).join("")}
                </ul>
            ` : ""}
            ${a.related_topics?.length ? `
                <div class="topic-related">
                    ${a.related_topics.map(r => `<span class="related-tag">${esc(r)}</span>`).join("")}
                </div>
            ` : ""}
        `;
        grid.appendChild(card);
    });

    container.appendChild(grid);
}

// ═══ Sources Tab ═════════════════════════════════════════════════
function renderSources(container) {
    const items = DATA.curated_feed?.top_items || [];
    const bySource = {};
    items.forEach((item) => {
        if (!bySource[item.source]) bySource[item.source] = [];
        bySource[item.source].push(item);
    });

    const sourceIcons = {
        arxiv: "📄", hackernews: "🟠", reddit: "🔴",
        github: "🐙", ai_blogs: "📝", huggingface: "🤗",
    };

    if (Object.keys(bySource).length === 0) return renderEmpty(container, "🌐", "No sources", "Run the pipeline first.");

    const grid = document.createElement("div");
    grid.className = "source-grid";

    Object.entries(bySource).forEach(([source, sourceItems]) => {
        if (activeFilter) {
            const topicItems = sourceItems.filter(i => matchesTopic(i, activeFilter));
            if (!topicItems.length) return;
            sourceItems = topicItems;
        }
        if (searchQuery) {
            sourceItems = sourceItems.filter(i => filterAndSearch(i));
        }
        if (!sourceItems.length) return;

        const card = document.createElement("div");
        card.className = "source-card glass-card reveal";
        card.innerHTML = `
            <div class="source-name">
                <span class="source-icon ${source}">${sourceIcons[source] || "🌐"}</span>
                ${esc(source)} <span style="color:var(--text-muted);font-size:0.7rem;font-weight:400">(${sourceItems.length})</span>
            </div>
            <ul class="source-items">
                ${sourceItems.slice(0, 8).map(i => `
                    <li><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></li>
                `).join("")}
            </ul>
        `;
        grid.appendChild(card);
    });

    container.appendChild(grid);
}

// ═══ Helpers ═════════════════════════════════════════════════════
function filterAndSearch(item) {
    if (activeFilter && item.topic !== activeFilter) {
        // For items without .topic, check tags
        const tags = (item.tags || []).join(" ").toLowerCase();
        const title = (item.title || "").toLowerCase();
        if (!title.includes(activeFilter.toLowerCase()) && !tags.includes(activeFilter.toLowerCase())) return false;
    }
    if (searchQuery) {
        const text = `${item.title || ""} ${item.summary || ""} ${item.why_read || ""} ${(item.tags || []).join(" ")} ${item.topic || ""} ${item.source || ""}`.toLowerCase();
        if (!text.includes(searchQuery)) return false;
    }
    return true;
}

function matchesTopic(item, topic) {
    const text = `${item.title || ""} ${(item.tags || []).join(" ")}`.toLowerCase();
    return text.includes(topic.toLowerCase());
}

function showLoading() {
    document.getElementById("tabContent").innerHTML = `
        <div class="loading-state">
            <div class="loader"></div>
            <p>Running multi-agent pipeline...</p>
            <p class="loading-sub">Curator → Analyst → Recommender</p>
        </div>
    `;
}

function showError(msg) {
    document.getElementById("tabContent").innerHTML = `
        <div class="empty-state">
            <div class="emoji">⚠️</div>
            <h3>Error</h3>
            <p>${esc(msg)}</p>
        </div>
    `;
}

function renderEmpty(container, emoji, title, sub) {
    container.innerHTML = `
        <div class="empty-state">
            <div class="emoji">${emoji}</div>
            <h3>${esc(title)}</h3>
            <p>${esc(sub)}</p>
        </div>
    `;
}

function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}

function esc(str) {
    if (typeof str !== "string") return String(str ?? "");
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
}
