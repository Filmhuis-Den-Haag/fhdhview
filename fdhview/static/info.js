const POLL_MS = 5 * 60 * 1000;

// "2026-10-13T17:30:00" -> "17:30"
function hhmm(iso) {
  return iso.slice(11, 16);
}

// map kijkwijzer codes to /static/<name>.png
function kijkwijzerIcons(codes) {
  return (codes || []).map(c =>
    `<img class="kijkwijzer" src="/static/kw/${c}.png" alt="${c}">`
  ).join("");
}

function renderFilms(films) {
  const rows = (films || []).map(f => {
    const isBoutique = f.screen === "6";
    const ratio = f.seats_sold / f.seats_total;
    const start = new Date(f.start);          // "2026-10-13T18:00:00" parses as local time
    const minsUntil = (start - new Date()) / 60000;
    const badge = ratio >= 1
    ? '<div class="badge-last uitverkocht">Uitverkocht</div>'
    : "<div></div>";

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
          ${f.en_subs ? "<span class='subs'>EN subs</span>" : ""}
        </div>
      </div>
      ${badge}
    </div>`;
  }).join("");
  document.getElementById("films").innerHTML =
  rows + `<div class="film" "film-spacer" aria-hidden="true"></div>`;
}
function renderPrices(prices) {
  const row = p => `<div class="price-row"><span>${p.label}</span><span class="price">${p.price}</span></div>`;
  document.getElementById("prijzen").innerHTML = prices.prijzen.map(row).join("");
  document.getElementById("kortingsprijzen").innerHTML = prices.kortingsprijzen.map(row).join("");
}

function renderClock() {
  const d = new Date();
  const hh = String(d.getHours()).padStart(2, "0");
  const mm = String(d.getMinutes()).padStart(2, "0");
  document.getElementById("date").innerHTML = `${hh}<span class="colon">:</span>${mm}`;
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
setInterval(renderClock, 1_000);  // every second: updates minutes + blinks the colon
refresh();                        // initial paint
setInterval(refresh, POLL_MS);    // poll every 5 minutes
setInterval(renderClock, 30_000); // keep the clock accurate
