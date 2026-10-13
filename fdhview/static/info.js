const POLL_MS = 5 * 60 * 1000;

// "2026-10-13T17:30:00" -> "17:30"
function hhmm(iso) {
  return iso.slice(11, 16);
}

// map kijkwijzer codes to /static/<name>.png
function kijkwijzerIcons(codes) {
  return (codes || []).map(c =>
    `<img class="kijkwijzer" src="/static/${c}.png" alt="${c}">`
  ).join("");
}

function renderFilms(films) {
  document.getElementById("films").innerHTML = films.map(f => {
    const isBoutique = f.screen === "6";
    return `
    <div class="film">
      <div class="times"><div class="start">${hhmm(f.start)}</div><div class="end">${hhmm(f.end)}</div></div>
      <div class="icons">${kijkwijzerIcons(f.kijkwijzer)}</div>
      <div class="info">
        <div class="title">${f.title}</div>
        <div class="meta">
          ${isBoutique
            ? `<span class="pill">Zaal 6 - Boutique Cinema</span>`
            : `<span class="zaal">Zaal ${f.screen}</span>`}
          ${f.en_subs ? "<span>EN subs</span>" : ""}
        </div>
      </div>
      ${f.seats_sold / f.seats_total > 0.85 ? '<div class="badge-last">Laatste kaarten</div>' : "<div></div>"}
    </div>`;
  }).join("");
}
function renderPrices(prices) {
  const row = p => `<div class="price-row"><span>${p.label}</span><span class="price">${p.price}</span></div>`;
  document.getElementById("prijzen").innerHTML = prices.prijzen.map(row).join("");
  document.getElementById("kortingsprijzen").innerHTML = prices.kortingsprijzen.map(row).join("");
}

function renderClock() {
  const d = new Date();
  document.getElementById("date").textContent =
    d.toLocaleTimeString("nl-NL", { hour: "2-digit", minute: "2-digit" });
}

async function refresh() {
  try {
    const [filmsRes, pricesRes] = await Promise.all([
      fetch("/api/screenings"),
      fetch("/api/screenings/prices"),
    ]);
    renderFilms(await filmsRes.json());
    renderPrices(await pricesRes.json());
  } catch (err) {
    console.error("refresh failed, keeping current display:", err);
  }
}

renderClock();
refresh();                        // initial paint
setInterval(refresh, POLL_MS);    // poll every 5 minutes
setInterval(renderClock, 30_000); // keep the clock accurate
