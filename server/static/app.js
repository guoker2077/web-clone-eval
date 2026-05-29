// 云端 UI 逻辑：提交任务 → 轮询列表与日志 → 完成后给预览/报告链接。
// 纯轮询（非 SSE）：本地骨架够用，且与未来 SSE/WebSocket 升级解耦。

const $ = (id) => document.getElementById(id);
const logCursors = {};   // job_id -> 已拉到的最大 log id（增量轮询）

const STATUS_LABEL = { queued: "排队中", running: "运行中", done: "完成", failed: "失败" };

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) {
    const t = await r.text();
    throw new Error(`${r.status}: ${t}`);
  }
  return r.json();
}

async function submit() {
  const btn = $("submit");
  const err = $("formErr");
  err.textContent = "";
  const url = $("url").value.trim();
  const scope_text = $("scope").value.trim();
  if (!url || !scope_text) {
    err.textContent = "网址和复刻范围都要填。";
    return;
  }
  btn.disabled = true;
  btn.textContent = "提交中...";
  try {
    await api("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url,
        scope_text,
        max_rounds: parseInt($("rounds").value, 10) || 2,
        threshold: parseFloat($("threshold").value) || 85,
      }),
    });
    $("scope").value = "";
    await refresh();
  } catch (e) {
    err.textContent = "提交失败：" + e.message;
  } finally {
    btn.disabled = false;
    btn.textContent = "提交复刻任务";
  }
}

function badge(status) {
  const cls = { queued: "b-queued", running: "b-running", done: "b-done", failed: "b-failed" }[status] || "b-queued";
  return `<span class="badge ${cls}">${STATUS_LABEL[status] || status}</span>`;
}

function jobCard(job) {
  const scoreTxt = job.score != null ? ` · 得分 ${job.score}` : "";
  let acts = "";
  if (job.status === "done") {
    acts = `<div class="acts">
      <a href="/preview/${job.site_id}/" target="_blank">↗ 预览复刻页</a>
      <a href="/report/${job.site_id}" target="_blank">查看评估报告</a>
    </div>`;
  }
  const errHtml = job.error ? `<div class="err">${escapeHtml(job.error)}</div>` : "";
  return `<div class="job" data-id="${job.id}">
    <div class="job-head">
      <div class="job-title">${escapeHtml(job.url)}</div>
      ${badge(job.status)}
    </div>
    <div class="stage">阶段：${escapeHtml(job.stage)}${scoreTxt} · ${escapeHtml(job.scope_text || "")}</div>
    <div class="logbox" id="log-${job.id}"></div>
    ${acts}
    ${errHtml}
  </div>`;
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

async function pullLogs(jobId) {
  const after = logCursors[jobId] || 0;
  try {
    const { logs } = await api(`/api/jobs/${jobId}/logs?after_id=${after}`);
    if (!logs.length) return;
    const box = $(`log-${jobId}`);
    if (!box) return;
    for (const l of logs) {
      const div = document.createElement("div");
      div.textContent = (l.stage ? `[${l.stage}] ` : "") + l.line;
      box.appendChild(div);
      logCursors[jobId] = l.id;
    }
    box.scrollTop = box.scrollHeight;
  } catch (e) { /* 静默：列表刷新时会再试 */ }
}

let lastIds = "";
async function refresh() {
  let data;
  try { data = await api("/api/jobs"); } catch (e) { return; }
  const jobs = data.jobs || [];
  const container = $("jobs");
  if (!jobs.length) {
    container.innerHTML = `<div class="empty">还没有任务，提交一个试试。</div>`;
    return;
  }
  // 仅当任务集合/状态变化时重渲染，避免清空日志框
  const sig = jobs.map((j) => `${j.id}:${j.status}:${j.stage}:${j.score}`).join("|");
  if (sig !== lastIds) {
    container.innerHTML = jobs.map(jobCard).join("");
    lastIds = sig;
  }
  // 给每个未完成任务拉增量日志
  for (const j of jobs) await pullLogs(j.id);
}

$("submit").addEventListener("click", submit);
refresh();
setInterval(refresh, 2000);
