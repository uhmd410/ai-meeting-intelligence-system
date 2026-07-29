/**
 * api.js — Centralized API client for AI Meeting Intelligence System
 * All pages import this file and call these functions instead of using fetch() directly.
 */

const API_BASE = "";

// ─── Helper: parse error body from response ───────────────────────────────────
async function parseErrorBody(response) {
  try {
    const body = await response.json();
    // FastAPI returns { "detail": "..." } for most errors
    if (typeof body.detail === "string") return body.detail;
    if (typeof body.detail === "object") return JSON.stringify(body.detail);
    if (typeof body.message === "string") return body.message;
    return JSON.stringify(body);
  } catch {
    return `Server returned ${response.status} ${response.statusText}`;
  }
}

// ─── Helper: wrap fetch with automatic error extraction ───────────────────────
async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  let response;
  try {
    response = await fetch(url, options);
  } catch (err) {
    throw new Error(
      "Unable to reach the server. Please check that the backend is running."
    );
  }

  if (!response.ok) {
    const msg = await parseErrorBody(response);
    throw new Error(msg);
  }

  // 204 No Content — nothing to parse
  if (response.status === 204) return null;

  return response.json();
}

// ─── Public API functions ─────────────────────────────────────────────────────

/**
 * Create a new meeting.
 * @param {string} title
 * @param {object} opts  – { rawText?: string, file?: File }
 * @returns {Promise<MeetingOut>}
 */
async function createMeeting(title, { rawText, file } = {}) {
  const form = new FormData();
  form.append("title", title);
  if (file) {
    form.append("file", file);
  } else if (rawText) {
    form.append("raw_text", rawText);
  }
  return apiFetch("/api/meetings", { method: "POST", body: form });
}

/**
 * Trigger LLM generation for a meeting.
 * @param {number} id
 * @returns {Promise<MeetingDetailOut>}
 */
async function generateMinutes(id) {
  return apiFetch(`/api/meetings/${id}/generate`, { method: "POST" });
}

/**
 * List meetings with pagination.
 * @param {number} skip
 * @param {number} limit
 * @returns {Promise<MeetingOut[]>}
 */
async function listMeetings(skip = 0, limit = 20) {
  return apiFetch(`/api/meetings?skip=${skip}&limit=${limit}`);
}

/**
 * Get a single meeting's full detail.
 * @param {number} id
 * @returns {Promise<MeetingDetailOut>}
 */
async function getMeeting(id) {
  return apiFetch(`/api/meetings/${id}`);
}

/**
 * Delete a meeting.
 * @param {number} id
 * @returns {Promise<null>}
 */
async function deleteMeeting(id) {
  return apiFetch(`/api/meetings/${id}`, { method: "DELETE" });
}

// ─── UI helpers — shared across pages ─────────────────────────────────────────

/**
 * Set a button into loading state.
 * Returns a restore function to call when done.
 */
function setButtonLoading(btn, loadingText = "Processing…") {
  const original = btn.innerHTML;
  const wasDisabled = btn.disabled;
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>${loadingText}`;
  return () => {
    btn.innerHTML = original;
    btn.disabled = wasDisabled;
  };
}

/**
 * Show a dismissible Bootstrap alert inside a container element.
 */
function showAlert(container, message, type = "danger") {
  const id = "alert-" + Date.now();
  container.insertAdjacentHTML(
    "afterbegin",
    `<div id="${id}" class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${escapeHtml(message)}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`
  );
}

/**
 * Return the appropriate Bootstrap badge class for a meeting status.
 */
function statusBadgeClass(status) {
  switch (status) {
    case "completed":
      return "badge-completed";
    case "failed":
      return "badge-failed";
    case "pending":
    default:
      return "badge-pending";
  }
}

/**
 * Format an ISO datetime string to a human-readable local string.
 */
function formatDate(isoString) {
  if (!isoString) return "—";
  const d = new Date(isoString);
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Escape HTML entities.
 */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
