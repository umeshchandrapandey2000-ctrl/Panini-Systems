/**
 * Panini Systems | Interactive Game Mathematics & Quantitative Platform
 * Real-time Combinatorics, Monte Carlo Engine, PAR Sheet Generator, and Gacha Modeling
 */

// --- DATA STRUCTURES & DEFAULT PRESETS ---
const DEFAULT_PRESETS = {
  balanced: {
    name: "Balanced Medium Volatility (96.18% RTP)",
    paylines: 25,
    reels: [30, 30, 30, 30, 30],
    wildCount: [1, 2, 2, 2, 1],
    hpCounts: [4, 4, 4, 4, 4],
    mpCounts: [7, 7, 7, 7, 7],
    lpCounts: [17, 16, 16, 16, 17],
    scatterCount: [1, 1, 1, 1, 1],
    featureRtp: 31.52,
    paytable: {
      WILD: { 5: 1000, 4: 250, 3: 50 },
      HP1:  { 5: 500,  4: 120, 3: 30, 2: 2 },
      HP2:  { 5: 350,  4: 80,  3: 20 },
      HP3:  { 5: 250,  4: 60,  3: 15 },
      MP1:  { 5: 150,  4: 40,  3: 10 },
      MP2:  { 5: 100,  4: 30,  3: 8 },
      LP1:  { 5: 50,   4: 15,  3: 5 },
      LP2:  { 5: 35,   4: 10,  3: 4 },
      LP3:  { 5: 25,   4: 8,   3: 3 },
    }
  },
  high_vol: {
    name: "High Volatility / Big Win Potential (94.50% RTP)",
    paylines: 20,
    reels: [32, 32, 32, 32, 32],
    wildCount: [1, 1, 1, 1, 1],
    hpCounts: [2, 2, 2, 2, 2],
    mpCounts: [6, 6, 6, 6, 6],
    lpCounts: [22, 22, 22, 22, 22],
    scatterCount: [1, 1, 1, 1, 1],
    featureRtp: 36.30,
    paytable: {
      WILD: { 5: 2500, 4: 500, 3: 100 },
      HP1:  { 5: 1250, 4: 250, 3: 40 },
      HP2:  { 5: 750,  4: 150, 3: 30 },
      HP3:  { 5: 500,  4: 100, 3: 20 },
      MP1:  { 5: 200,  4: 50,  3: 12 },
      MP2:  { 5: 150,  4: 35,  3: 10 },
      LP1:  { 5: 60,   4: 20,  3: 5 },
      LP2:  { 5: 40,   4: 12,  3: 4 },
      LP3:  { 5: 30,   4: 10,  3: 3 },
    }
  },
  casual_low: {
    name: "Casual High Hit Rate (96.80% RTP)",
    paylines: 25,
    reels: [28, 28, 28, 28, 28],
    wildCount: [2, 2, 2, 2, 2],
    hpCounts: [5, 5, 5, 5, 5],
    mpCounts: [8, 8, 8, 8, 8],
    lpCounts: [12, 12, 12, 12, 12],
    scatterCount: [1, 1, 1, 1, 1],
    featureRtp: 24.70,
    paytable: {
      WILD: { 5: 600, 4: 150, 3: 30 },
      HP1:  { 5: 300, 4: 80,  3: 15 },
      HP2:  { 5: 200, 4: 50,  3: 12 },
      HP3:  { 5: 150, 4: 35,  3: 10 },
      MP1:  { 5: 100, 4: 25,  3: 8 },
      MP2:  { 5: 75,  4: 20,  3: 6 },
      LP1:  { 5: 40,  4: 12,  3: 4 },
      LP2:  { 5: 30,  4: 8,   3: 3 },
      LP3:  { 5: 20,  4: 6,   3: 2 },
    }
  }
};

// --- CONSULTING CONTACT CONFIGURATION ---
// Edit these values anytime with your own email, phone number, and name!
const CONSULTANT_CONFIG = {
  consultantName: "Lead Game Mathematician",
  companyName: "Panini Systems",
  email: "umeshchandrapandey2000@gmail.com",       // <-- Change this to your real email address
  phone: "+91 99560 76057 ",                  // <-- Change this to your phone number
  phoneRaw: "+919956076057",                 // <-- Numbers only with country code for tel: link
  whatsappRaw: "919956076057",               // <-- Numbers only with country code for WhatsApp link
  // Optional: Paste your free Web3Forms Access Key (from https://web3forms.com) to receive form emails directly
  web3FormsAccessKey: "",
};

let currentSlotConfig = JSON.parse(JSON.stringify(DEFAULT_PRESETS.balanced));

// --- INITIALIZATION ---
document.addEventListener("DOMContentLoaded", () => {
  initSlotControls();
  calculateSlotTheoretical();
  initGachaControls();
  calculateGachaModel();
  initClientScoping();
  initContactForm();
});

// --- SLOT COMBINATORICS ENGINE ---
function calculateSlotTheoretical() {
  const cfg = currentSlotConfig;
  const cycle = cfg.reels.reduce((a, b) => a * b, 1);

  let totalWinningCombos = 0;
  let totalLineReturn = 0;
  const tableRows = [];

  const symWeights = {
    WILD: cfg.wildCount,
    HP1: cfg.hpCounts.map(c => Math.max(1, Math.round(c * 0.35))),
    HP2: cfg.hpCounts.map(c => Math.max(1, Math.round(c * 0.35))),
    HP3: cfg.hpCounts.map(c => Math.max(1, Math.round(c * 0.30))),
    MP1: cfg.mpCounts.map(c => Math.max(1, Math.round(c * 0.50))),
    MP2: cfg.mpCounts.map(c => Math.max(1, Math.round(c * 0.50))),
    LP1: cfg.lpCounts.map(c => Math.max(1, Math.round(c * 0.35))),
    LP2: cfg.lpCounts.map(c => Math.max(1, Math.round(c * 0.35))),
    LP3: cfg.lpCounts.map(c => Math.max(1, Math.round(c * 0.30))),
  };

  const wildCount = symWeights.WILD;

  for (const [sym, pays] of Object.entries(cfg.paytable)) {
    const c = symWeights[sym];
    const eff = c.map((cnt, i) => cnt + (sym !== "WILD" ? wildCount[i] : 0));

    // 5-of-a-kind
    if (pays[5]) {
      let n5 = eff[0] * eff[1] * eff[2] * eff[3] * eff[4];
      if (sym !== "WILD") {
        const pureWild5 = wildCount.reduce((a, b) => a * b, 1);
        n5 = Math.max(0, n5 - pureWild5);
      }
      const ret = n5 * pays[5];
      totalWinningCombos += n5;
      totalLineReturn += ret;
      tableRows.push({
        symbol: sym,
        kind: "5x",
        combos: n5,
        payout: pays[5],
        prob: n5 / cycle,
        rtpCont: (ret / cycle) * 100
      });
    }

    // 4-of-a-kind
    if (pays[4]) {
      const nonMatch5 = Math.max(0, cfg.reels[4] - eff[4]);
      const n4 = eff[0] * eff[1] * eff[2] * eff[3] * nonMatch5;
      const ret = n4 * pays[4];
      totalWinningCombos += n4;
      totalLineReturn += ret;
      tableRows.push({
        symbol: sym,
        kind: "4x",
        combos: n4,
        payout: pays[4],
        prob: n4 / cycle,
        rtpCont: (ret / cycle) * 100
      });
    }

    // 3-of-a-kind
    if (pays[3]) {
      const nonMatch4 = Math.max(0, cfg.reels[3] - eff[3]);
      const n3 = eff[0] * eff[1] * eff[2] * nonMatch4 * cfg.reels[4];
      const ret = n3 * pays[3];
      totalWinningCombos += n3;
      totalLineReturn += ret;
      tableRows.push({
        symbol: sym,
        kind: "3x",
        combos: n3,
        payout: pays[3],
        prob: n3 / cycle,
        rtpCont: (ret / cycle) * 100
      });
    }

    // 2-of-a-kind (for high pays and wild)
    if (pays[2]) {
      const nonMatch3 = Math.max(0, cfg.reels[2] - eff[2]);
      const n2 = eff[0] * eff[1] * nonMatch3 * cfg.reels[3] * cfg.reels[4];
      const ret = n2 * pays[2];
      totalWinningCombos += n2;
      totalLineReturn += ret;
      tableRows.push({
        symbol: sym,
        kind: "2x",
        combos: n2,
        payout: pays[2],
        prob: n2 / cycle,
        rtpCont: (ret / cycle) * 100
      });
    }
  }

  const baseGameRTP = (totalLineReturn / cycle) * 100;
  const featureRTP = cfg.featureRtp || 30.60;
  const totalRTP = baseGameRTP + featureRTP;
  const lineHitFreq = (totalWinningCombos / cycle) * 100;

  // Volatility Tier determination
  let volTier = "Medium";
  if (lineHitFreq > 32) volTier = "Low";
  else if (lineHitFreq < 22) volTier = "High";
  if (lineHitFreq < 18 || totalRTP < 94.8) volTier = "Very High";

  // Update UI Elements
  const kpiRtp = document.getElementById("kpi-rtp");
  const kpiHit = document.getElementById("kpi-hit-rate");
  const kpiCyc = document.getElementById("kpi-cycle");
  const kpiVol = document.getElementById("kpi-volatility");

  if (kpiRtp) kpiRtp.textContent = `${totalRTP.toFixed(2)}%`;
  if (kpiHit) kpiHit.textContent = `${lineHitFreq.toFixed(2)}%`;
  if (kpiCyc) kpiCyc.textContent = cycle.toLocaleString();
  if (kpiVol) kpiVol.textContent = volTier;

  renderParSheetTable(tableRows, baseGameRTP, featureRTP, totalRTP, totalWinningCombos);
  window.currentParRows = tableRows;
  window.currentTotalRTP = totalRTP;
  window.currentBaseRTP = baseGameRTP;
  window.currentFeatureRTP = featureRTP;
}

function renderParSheetTable(rows, baseRtp, featureRtp, totalRtp, totalCombos) {
  const tbody = document.getElementById("par-sheet-body");
  if (!tbody) return;

  tbody.innerHTML = rows.slice(0, 16).map(r => `
    <tr>
      <td><span class="px-2 py-0.5 rounded bg-slate-800 text-emerald-400 font-mono text-xs">${r.symbol}</span></td>
      <td class="font-mono text-xs">${r.kind}</td>
      <td class="font-mono text-xs text-right">${r.combos.toLocaleString()}</td>
      <td class="font-mono text-xs text-right text-amber-400">${r.payout.toFixed(1)}x</td>
      <td class="font-mono text-xs text-right text-slate-400">${(r.prob * 100).toFixed(4)}%</td>
      <td class="font-mono text-xs text-right text-emerald-400 font-semibold">${r.rtpCont.toFixed(3)}%</td>
    </tr>
  `).join("");

  const totCombosEl = document.getElementById("par-total-combos");
  const totRtpEl = document.getElementById("par-total-rtp");

  if (totCombosEl) totCombosEl.textContent = totalCombos.toLocaleString();
  if (totRtpEl) totRtpEl.textContent = `${totalRtp.toFixed(2)}% (Base: ${baseRtp.toFixed(2)}% + Feature: ${featureRtp.toFixed(2)}%)`;
}

// --- MONTE CARLO SIMULATION (IN-BROWSER) ---
function runMonteCarlo(spinCount = 50000) {
  const btn = document.getElementById("btn-run-sim");
  const progressContainer = document.getElementById("sim-progress-container");
  const progressBar = document.getElementById("sim-progress-bar");
  const statusTxt = document.getElementById("sim-status-txt");

  if (!btn || !window.currentParRows) return;

  btn.disabled = true;
  btn.classList.add("opacity-50", "cursor-not-allowed");
  if (progressContainer) progressContainer.classList.remove("hidden");

  const cfg = currentSlotConfig;
  const numLines = cfg.paylines;
  const totalBetPerSpin = numLines;
  let totalWon = 0;
  let sumSq = 0;
  let winningSpins = 0;
  let maxWin = 0;

  const featureRate = 1 / 145; // Free spins trigger ~1 in 145 spins
  const featureMeanMultiplier = (cfg.featureRtp / 100) * totalBetPerSpin / featureRate;

  const buckets = {
    "0x (Loss)": 0,
    "0-1x": 0,
    "1-2x": 0,
    "2-5x": 0,
    "5-20x": 0,
    "20-50x": 0,
    "50x+": 0
  };

  const batchSize = 5000;
  let completed = 0;

  function processBatch() {
    const end = Math.min(completed + batchSize, spinCount);
    for (let i = completed; i < end; i++) {
      let spinPayout = 0;

      // Payline sample
      for (let l = 0; l < numLines; l++) {
        const rand = Math.random();
        let accum = 0;
        for (const r of window.currentParRows) {
          accum += r.prob;
          if (rand < accum) {
            spinPayout += r.payout;
            break;
          }
        }
      }

      // Feature trigger sample
      if (Math.random() < featureRate) {
        // Feature payout with lognormal-like dispersion
        const featWin = featureMeanMultiplier * (0.4 + 1.2 * Math.random() + (Math.random() < 0.1 ? 2.5 : 0));
        spinPayout += featWin;
      }

      totalWon += spinPayout;
      sumSq += spinPayout * spinPayout;
      if (spinPayout > 0) {
        winningSpins++;
        if (spinPayout > maxWin) maxWin = spinPayout;
      }

      const mult = spinPayout / totalBetPerSpin;
      if (mult === 0) buckets["0x (Loss)"]++;
      else if (mult <= 1) buckets["0-1x"]++;
      else if (mult <= 2) buckets["1-2x"]++;
      else if (mult <= 5) buckets["2-5x"]++;
      else if (mult <= 20) buckets["5-20x"]++;
      else if (mult <= 50) buckets["20-50x"]++;
      else buckets["50x+"]++;
    }

    completed = end;
    const pct = Math.round((completed / spinCount) * 100);
    if (progressBar) progressBar.style.width = `${pct}%`;
    if (statusTxt) statusTxt.textContent = `Simulated ${completed.toLocaleString()} / ${spinCount.toLocaleString()} spins (${pct}%)...`;

    if (completed < spinCount) {
      requestAnimationFrame(processBatch);
    } else {
      finalizeSimulation(spinCount, totalBetPerSpin * spinCount, totalWon, sumSq, winningSpins, maxWin, buckets);
      btn.disabled = false;
      btn.classList.remove("opacity-50", "cursor-not-allowed");
      if (progressContainer) setTimeout(() => progressContainer.classList.add("hidden"), 1500);
    }
  }

  requestAnimationFrame(processBatch);
}

function finalizeSimulation(spins, totalBet, totalWon, sumSq, winningSpins, maxWin, buckets) {
  const empiricalRtp = (totalWon / totalBet) * 100;
  const hitFreq = (winningSpins / spins) * 100;
  const mean = totalWon / spins;
  const variance = Math.max(0, (sumSq / spins) - (mean * mean));
  const stdDev = Math.sqrt(variance) / (currentSlotConfig.paylines);
  const stdErr = stdDev / Math.sqrt(spins);

  const vi90 = 1.645 * stdDev;
  const vi95 = 1.96 * stdDev;

  const ci95Low = empiricalRtp - (1.96 * stdErr * 100);
  const ci95High = empiricalRtp + (1.96 * stdErr * 100);

  // Update UI
  const resSpins = document.getElementById("sim-res-spins");
  const resRtp = document.getElementById("sim-res-rtp");
  const resCi95 = document.getElementById("sim-res-ci95");
  const resHit = document.getElementById("sim-res-hit-rate");
  const resStd = document.getElementById("sim-res-stddev");
  const resVi95 = document.getElementById("sim-res-vi95");
  const resMax = document.getElementById("sim-res-maxwin");

  if (resSpins) resSpins.textContent = spins.toLocaleString();
  if (resRtp) resRtp.textContent = `${empiricalRtp.toFixed(2)}%`;
  if (resCi95) resCi95.textContent = `[${ci95Low.toFixed(2)}%, ${ci95High.toFixed(2)}%]`;
  if (resHit) resHit.textContent = `${hitFreq.toFixed(2)}%`;
  if (resStd) resStd.textContent = stdDev.toFixed(3);
  if (resVi95) resVi95.textContent = vi95.toFixed(3);
  if (resMax) resMax.textContent = `${(maxWin / currentSlotConfig.paylines).toFixed(1)}x`;

  const resultsCard = document.getElementById("sim-results-card");
  if (resultsCard) resultsCard.classList.remove("hidden");
  renderHistogramChart(buckets, spins);
}

function renderHistogramChart(buckets, totalSpins) {
  const canvas = document.getElementById("simHistogramCanvas");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  const labels = Object.keys(buckets);
  const counts = Object.values(buckets);
  const pcts = counts.map(c => (c / totalSpins) * 100);

  const barWidth = (w - 80) / labels.length;
  const maxPct = Math.max(...pcts, 1);

  // Draw axes
  ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(50, 10);
  ctx.lineTo(50, h - 30);
  ctx.lineTo(w - 10, h - 30);
  ctx.stroke();

  // Draw grid lines
  ctx.fillStyle = "#64748b";
  ctx.font = "10px JetBrains Mono";
  ctx.textAlign = "right";
  for (let step = 0; step <= 100; step += 25) {
    if (step <= maxPct * 1.15) {
      const y = (h - 30) - ((step / (maxPct * 1.15)) * (h - 45));
      ctx.fillText(`${step}%`, 42, y + 3);
      ctx.beginPath();
      ctx.moveTo(50, y);
      ctx.lineTo(w - 10, y);
      ctx.stroke();
    }
  }

  // Draw bars
  labels.forEach((label, i) => {
    const pct = pcts[i];
    const barH = (pct / (maxPct * 1.15)) * (h - 45);
    const x = 60 + (i * barWidth);
    const y = (h - 30) - barH;

    const grad = ctx.createLinearGradient(x, y, x, h - 30);
    if (i === 0) {
      grad.addColorStop(0, "#ef4444");
      grad.addColorStop(1, "rgba(239, 68, 68, 0.2)");
    } else if (i < 4) {
      grad.addColorStop(0, "#10b981");
      grad.addColorStop(1, "rgba(16, 185, 129, 0.2)");
    } else {
      grad.addColorStop(0, "#f59e0b");
      grad.addColorStop(1, "rgba(245, 158, 11, 0.2)");
    }

    ctx.fillStyle = grad;
    ctx.fillRect(x, y, barWidth - 8, barH);

    ctx.fillStyle = "#94a3b8";
    ctx.textAlign = "center";
    ctx.fillText(label, x + (barWidth - 8) / 2, h - 14);

    ctx.fillStyle = "#f8fafc";
    ctx.fillText(`${pct.toFixed(1)}%`, x + (barWidth - 8) / 2, y - 4);
  });
}

// --- GACHA PITY PROBABILITY ENGINE ---
function calculateGachaModel() {
  const baseRateInput = document.getElementById("gacha-base-rate");
  const softStartInput = document.getElementById("gacha-soft-start");
  const hardPityInput = document.getElementById("gacha-hard-pity");

  const baseRate = baseRateInput ? parseFloat(baseRateInput.value) / 100.0 : 0.006;
  const softStart = softStartInput ? parseInt(softStartInput.value, 10) : 74;
  const hardPity = hardPityInput ? parseInt(hardPityInput.value, 10) : 90;
  const softSlope = 0.06;

  const pmf = [0];
  const cdf = [0];
  let survival = 1.0;
  let expectedPulls = 0;

  for (let k = 1; k <= hardPity; k++) {
    let p_k = baseRate;
    if (k >= hardPity) {
      p_k = 1.0;
    } else if (k >= softStart) {
      p_k = Math.min(1.0, baseRate + ((k - softStart + 1) * softSlope));
    }

    const probHit = survival * p_k;
    pmf[k] = probHit;
    cdf[k] = cdf[k - 1] + probHit;
    expectedPulls += k * probHit;
    survival *= (1.0 - p_k);
  }

  if (cdf[hardPity] < 1.0) {
    pmf[hardPity] += (1.0 - cdf[hardPity]);
    cdf[hardPity] = 1.0;
  }

  const consolidatedRate = (1.0 / expectedPulls) * 100;
  const featuredPulls5050 = expectedPulls * 1.5;

  function getQuantile(target) {
    for (let k = 1; k <= hardPity; k++) {
      if (cdf[k] >= target) return k;
    }
    return hardPity;
  }

  const medianPulls = getQuantile(0.50);
  const p90Pulls = getQuantile(0.90);
  const p99Pulls = getQuantile(0.99);

  // Update UI Elements
  const vBase = document.getElementById("val-base-rate");
  const vSoft = document.getElementById("val-soft-start");
  const vHard = document.getElementById("val-hard-pity");

  if (vBase) vBase.textContent = `${(baseRate * 100).toFixed(2)}%`;
  if (vSoft) vSoft.textContent = `Pull ${softStart}`;
  if (vHard) vHard.textContent = `Pull ${hardPity}`;

  const gExp = document.getElementById("gacha-exp-pulls");
  const gCon = document.getElementById("gacha-consolidated");
  const gMed = document.getElementById("gacha-median");
  const gP90 = document.getElementById("gacha-p90");
  const gP99 = document.getElementById("gacha-p99");
  const gFeat = document.getElementById("gacha-featured");

  if (gExp) gExp.textContent = expectedPulls.toFixed(1);
  if (gCon) gCon.textContent = `${consolidatedRate.toFixed(2)}%`;
  if (gMed) gMed.textContent = `${medianPulls} pulls`;
  if (gP90) gP90.textContent = `${p90Pulls} pulls`;
  if (gP99) gP99.textContent = `${p99Pulls} pulls`;
  if (gFeat) gFeat.textContent = `${featuredPulls5050.toFixed(1)} pulls`;

  renderGachaChart(pmf, cdf, hardPity, softStart);
}

function renderGachaChart(pmf, cdf, hardPity, softStart) {
  const canvas = document.getElementById("gachaChartCanvas");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  // Axes
  ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(40, 10);
  ctx.lineTo(40, h - 25);
  ctx.lineTo(w - 10, h - 25);
  ctx.stroke();

  // Plot PMF (bars)
  const maxPmf = Math.max(...pmf.slice(1)) * 1.15;
  const stepX = (w - 55) / hardPity;

  for (let k = 1; k <= hardPity; k++) {
    const val = pmf[k];
    const barH = (val / maxPmf) * (h - 40);
    const x = 45 + ((k - 1) * stepX);
    const y = (h - 25) - barH;

    ctx.fillStyle = k >= softStart ? "rgba(245, 158, 11, 0.7)" : "rgba(16, 185, 129, 0.4)";
    ctx.fillRect(x, y, Math.max(1, stepX - 1), barH);
  }

  // Plot CDF (smooth line)
  ctx.beginPath();
  ctx.strokeStyle = "#06b6d4";
  ctx.lineWidth = 2.5;
  for (let k = 1; k <= hardPity; k++) {
    const x = 45 + ((k - 1) * stepX);
    const y = (h - 25) - (cdf[k] * (h - 40));
    if (k === 1) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // Indicator for soft pity
  const softX = 45 + ((softStart - 1) * stepX);
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = "rgba(245, 158, 11, 0.6)";
  ctx.beginPath();
  ctx.moveTo(softX, 10);
  ctx.lineTo(softX, h - 25);
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = "#f59e0b";
  ctx.font = "10px JetBrains Mono";
  ctx.fillText(`Soft Pity (${softStart})`, softX + 4, 20);
}

// --- CSV PAR SHEET EXPORT ---
function exportParSheetCsv() {
  if (!window.currentParRows) return;
  const cfg = currentSlotConfig;
  const cycle = cfg.reels.reduce((a, b) => a * b, 1);

  let csvContent = "data:text/csv;charset=utf-8,";
  csvContent += "PANINI SYSTEMS - PROBABILITY ACCOUNTING REPORT (PAR SHEET)\r\n";
  csvContent += `Game Title,${cfg.name}\r\n`;
  csvContent += `Paylines,${cfg.paylines}\r\n`;
  csvContent += `Total Combinatorial Cycle,${cycle}\r\n`;
  csvContent += `Theoretical Base RTP,${window.currentBaseRTP.toFixed(4)}%\r\n`;
  csvContent += `Theoretical Feature RTP,${window.currentFeatureRTP.toFixed(4)}%\r\n`;
  csvContent += `Total Theoretical RTP,${window.currentTotalRTP.toFixed(4)}%\r\n\r\n`;
  csvContent += "Symbol,Kind,Combinations,Payout,Probability,RTP_Contribution_Pct\r\n";

  window.currentParRows.forEach(r => {
    csvContent += `${r.symbol},${r.kind},${r.combos},${r.payout},${r.prob.toFixed(8)},${r.rtpCont.toFixed(4)}%\r\n`;
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `panini_par_sheet_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// --- CONTROLS & LISTENERS ---
function initSlotControls() {
  document.getElementById("preset-select")?.addEventListener("change", (e) => {
    const key = e.target.value;
    if (DEFAULT_PRESETS[key]) {
      currentSlotConfig = JSON.parse(JSON.stringify(DEFAULT_PRESETS[key]));
      calculateSlotTheoretical();
    }
  });

  document.getElementById("btn-run-sim")?.addEventListener("click", () => {
    const count = parseInt(document.getElementById("sim-spins-select").value, 10);
    runMonteCarlo(count);
  });

  document.getElementById("btn-export-csv")?.addEventListener("click", exportParSheetCsv);
}

function initGachaControls() {
  const baseRateSlider = document.getElementById("gacha-base-rate");
  const softStartSlider = document.getElementById("gacha-soft-start");
  const hardPitySlider = document.getElementById("gacha-hard-pity");

  [baseRateSlider, softStartSlider, hardPitySlider].forEach(el => {
    el?.addEventListener("input", calculateGachaModel);
  });
}

function initClientScoping() {
  const form = document.getElementById("client-scoping-form");
  const outputCard = document.getElementById("scoping-output-card");
  const briefText = document.getElementById("scoping-brief-text");

  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    const studio = document.getElementById("scope-studio").value || "Studio Client";
    const gameType = document.getElementById("scope-game-type").value;
    const rtpTarget = document.getElementById("scope-rtp").value;
    const volTarget = document.getElementById("scope-vol").value;
    const mechanics = document.getElementById("scope-mechanics").value;

    const brief = `### PANINI SYSTEMS | MATHEMATICAL CONSULTING PROJECT BRIEF
------------------------------------------------------------
Client Studio: ${studio}
Game Type: ${gameType}
Target RTP: ${rtpTarget}%
Volatility Tier: ${volTarget}
Key Mechanics & Features: ${mechanics}

Status: Received & Ready for Combinatorial Architecture
Assigned Practice Lead: Game Mathematics & Economy Engineering
Consulting Lab Readiness: GLI-11 / GLI-19 Standard
------------------------------------------------------------`;

    briefText.textContent = brief;
    outputCard.classList.remove("hidden");
    outputCard.scrollIntoView({ behavior: "smooth" });
  });
}

// --- DIRECT CONTACT & ANALYSIS REQUEST HANDLER ---
function initContactForm() {
  // 1. Sync Direct Phone, WhatsApp, and Email buttons with CONSULTANT_CONFIG
  const phoneBtn = document.getElementById("contact-phone-btn");
  const waBtn = document.getElementById("contact-wa-btn");
  const emailBtn = document.getElementById("contact-email-btn");

  if (phoneBtn) {
    phoneBtn.href = `tel:${CONSULTANT_CONFIG.phoneRaw}`;
    phoneBtn.querySelector("span").textContent = `Call: ${CONSULTANT_CONFIG.phone}`;
  }

  if (waBtn) {
    waBtn.href = `https://wa.me/${CONSULTANT_CONFIG.whatsappRaw}?text=Hello%20${encodeURIComponent(CONSULTANT_CONFIG.companyName)},%20I%20would%20like%20to%20request%20a%20game%20mathematics%20analysis.`;
  }

  if (emailBtn) {
    emailBtn.href = `mailto:${CONSULTANT_CONFIG.email}?subject=Game%20Math%20Analysis%20Inquiry%20-%20${encodeURIComponent(CONSULTANT_CONFIG.companyName)}`;
    emailBtn.textContent = CONSULTANT_CONFIG.email;
  }

  // 2. Helper to construct pre-filled mailto URL from form fields
  function getMailtoUrl() {
    const name = document.getElementById("contact-name")?.value || "Client Lead";
    const company = document.getElementById("contact-company")?.value || "Game Studio";
    const email = document.getElementById("contact-email")?.value || "";
    const phone = document.getElementById("contact-phone")?.value || "Not provided";
    const service = document.getElementById("contact-service")?.value || "General Game Math";
    const timeline = document.getElementById("contact-timeline")?.value || "Standard";
    const message = document.getElementById("contact-message")?.value || "No additional notes provided.";

    const subject = encodeURIComponent(`[Analysis Request] ${service} - ${company}`);
    const body = encodeURIComponent(
`GAME MATHEMATICAL ANALYSIS REQUEST
====================================
Client Name: ${name}
Company / Studio: ${company}
Client Email: ${email}
Client Phone / WhatsApp: ${phone}
Service Requested: ${service}
Target Timeline: ${timeline}

Project Description & Scope:
------------------------------------
${message}

Sent via Panini Systems Consulting Portal`
    );

    return `mailto:${CONSULTANT_CONFIG.email}?subject=${subject}&body=${body}`;
  }

  // 3. Fallback "Send via Email App" button
  document.getElementById("btn-mailto-fallback")?.addEventListener("click", () => {
    const mailtoUrl = getMailtoUrl();
    window.location.href = mailtoUrl;

    const alertBox = document.getElementById("contact-status-alert");
    if (alertBox) {
      alertBox.className = "mt-4 p-4 rounded-xl border border-cyan-500/40 bg-cyan-950/40 text-cyan-200 text-xs";
      alertBox.innerHTML = `
        <div class="font-bold flex items-center space-x-1.5 mb-1">
          <span>📧 Opening your email client...</span>
        </div>
        <p>A pre-filled consultation request has been drafted for <strong>${CONSULTANT_CONFIG.email}</strong>. Simply click 'Send' in your mail app!</p>
      `;
      alertBox.classList.remove("hidden");
    }
  });

  // 4. Primary Form Submission
  const contactForm = document.getElementById("analysis-contact-form");
  const submitBtn = document.getElementById("btn-submit-contact");
  const alertBox = document.getElementById("contact-status-alert");

  contactForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("contact-name").value;
    const company = document.getElementById("contact-company").value;
    const email = document.getElementById("contact-email").value;
    const phone = document.getElementById("contact-phone").value;
    const service = document.getElementById("contact-service").value;
    const timeline = document.getElementById("contact-timeline").value;
    const message = document.getElementById("contact-message").value;

    submitBtn.disabled = true;
    submitBtn.classList.add("opacity-50", "cursor-not-allowed");
    submitBtn.querySelector("span").textContent = "Transmitting Request...";

    // If a Web3Forms access key is configured:
    if (CONSULTANT_CONFIG.web3FormsAccessKey && CONSULTANT_CONFIG.web3FormsAccessKey.trim() !== "") {
      try {
        const res = await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            access_key: CONSULTANT_CONFIG.web3FormsAccessKey,
            subject: `New Math Analysis Request from ${company} (${name})`,
            from_name: `${name} via Panini Systems`,
            name,
            company,
            email,
            phone,
            service,
            timeline,
            message,
          })
        });

        const result = await res.json();
        if (result.success) {
          alertBox.className = "mt-4 p-4 rounded-xl border border-emerald-500/40 bg-emerald-950/40 text-emerald-200 text-xs";
          alertBox.innerHTML = `
            <div class="font-bold flex items-center space-x-1.5 mb-1 text-emerald-400">
              <span>✅ Request Transmitted Directly to Our Lead Mathematician</span>
            </div>
            <p>Thank you, <strong>${name}</strong> (${company}). We have received your project requirements for <em>${service}</em> and will respond to <strong>${email}</strong> within 12–24 hours with preliminary feasibility notes.</p>
          `;
          alertBox.classList.remove("hidden");
          contactForm.reset();
        } else {
          throw new Error(result.message || "Failed to transmit");
        }
      } catch (err) {
        // Fallback to mailto if network or API error occurs
        fallbackToMailto();
      }
    } else {
      // Default out-of-the-box experience before API key is added: opens mailto and displays guidance
      fallbackToMailto();
    }

    submitBtn.disabled = false;
    submitBtn.classList.remove("opacity-50", "cursor-not-allowed");
    submitBtn.querySelector("span").textContent = "Submit Analysis Request";

    function fallbackToMailto() {
      const mailtoUrl = getMailtoUrl();
      window.location.href = mailtoUrl;

      if (alertBox) {
        alertBox.className = "mt-4 p-4 rounded-xl border border-emerald-500/40 bg-emerald-950/40 text-emerald-200 text-xs";
        alertBox.innerHTML = `
          <div class="font-bold flex items-center space-x-1.5 mb-1 text-emerald-400">
            <span>🚀 Consultation Request Ready!</span>
          </div>
          <p class="mb-2">Your request has been drafted directly for <strong>${CONSULTANT_CONFIG.email}</strong>. If your email app didn't automatically pop up, click the button below to send:</p>
          <a href="${mailtoUrl}" class="inline-block py-1.5 px-3 rounded bg-emerald-500 text-slate-950 font-bold text-xs">
            Open Pre-Filled Email Now
          </a>
        `;
        alertBox.classList.remove("hidden");
      }
    }
  });
}
