const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const payload = await response.text();
    throw new Error(payload || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export function lookupProperty(address) {
  return request(`/api/property/lookup?address=${encodeURIComponent(address)}`);
}

export function estimateRenovation(payload) {
  return request("/api/renovation/estimate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function analyzeInvestment(payload) {
  return request("/api/investment/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMarketTrend(zipCode) {
  return request(`/api/market/trends?zip_code=${encodeURIComponent(zipCode)}`);
}

export function getHealth() {
  return request("/health");
}
