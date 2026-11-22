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

const MONTHS_NL = ["jan", "feb", "mrt", "apr", "mei", "jun",
                   "jul", "aug", "sep", "okt", "nov", "dec"];

// "2026-12-01" -> local midnight Date, or null when empty/unparsable
function parseDay(iso) {
  if (!iso) return null;
  const d = new Date(`${iso}T00:00:00`);
  return isNaN(d) ? null : d;
}

// local midnight today
function today() {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d;
}

function priceHeader(iso) {
  const d = parseDay(iso);
  const m = MONTHS_NL[d.getMonth()];
  return `per ${d.getDate()} ${m[0].toUpperCase()}${m.slice(1)}`;
}

// How the upcoming prices should be shown:
//   null                       -> single column, current prices
//   { header, active: false }  -> extra column with the new prices
//   { active: true }           -> the start date has passed: new prices are
//                                 now the current ones
function newPriceState(prices) {
  const rows = (prices && prices.prijzen) || [];
  if (!rows.some(r => r.price_new)) return null;

  const starts = parseDay(prices.price_start);
  if (!starts) return null;
  if (starts <= today()) return { active: true };
  return { header: priceHeader(prices.price_start) };
}

// Rows as they should read today. Once the start date has passed the new price
// is simply the price; rows without a price_new keep their current one.
function effectiveRows(rows, state) {
  if (!state || !state.active) return rows || [];
  return (rows || []).map(p => ({ label: p.label, price: p.price_new || p.price }));
}

function priceRows(rows) {
  return (rows || []).map(p =>
    `<div class="price-row"><span>${p.label}</span><span class="price">${p.price}</span></div>`
  ).join("");
}

function renderPrices(prices) {
  const state = newPriceState(prices);
  const el = document.getElementById("prijzen");
  const twoColumn = Boolean(state) && !state.active;
  el.classList.toggle("has-new", twoColumn);

  if (!twoColumn) {
    el.innerHTML = priceRows(effectiveRows(prices.prijzen, state));
  } else {
    el.innerHTML =
      `<span class="price-head"></span><span class="price-head"></span>`
      + `<span class="price-head right">${state.header}</span>`
      + prices.prijzen.map(p =>
          `<span>${p.label}</span>`
          + `<span class="price">${p.price}</span>`
          + `<span class="price new">${p.price_new || ""}</span>`
        ).join("");
  }

  document.getElementById("kortingsprijzen").innerHTML =
    priceRows(prices.kortingsprijzen);
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
