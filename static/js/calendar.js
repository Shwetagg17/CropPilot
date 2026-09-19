// ================= ELEMENTS =================
const stateSelect = document.getElementById("stateSelect");
const cropSelect = document.getElementById("cropSelect");
const analyzeBtn = document.getElementById("analyzeBtn");
const resetBtn = document.getElementById("resetBtn");
const summaryBox = document.getElementById("summaryBox");
const tableBody = document.getElementById("tableBody");


// ================= DATA =================
const dataset = [
  { state: "Punjab", crop: "Wheat", season: "Nov - Mar" },
  { state: "Uttar Pradesh", crop: "Rice", season: "Jun - Oct" },
  { state: "Haryana", crop: "Maize", season: "Aug - Nov" },
  { state: "Maharashtra", crop: "Sugarcane", season: "Feb - Jul" },
  { state: "Karnataka", crop: "Cotton", season: "Aug - Jan" },
  { state: "Tamil Nadu", crop: "Pulses", season: "Nov - Feb" },
  { state: "West Bengal", crop: "Millets", season: "Jun - Sep" }
];


// ================= CURRENT MONTH =================
function getCurrentMonth() {
  return new Date().getMonth(); // 0–11
}


// ================= MONTH MAP =================
const monthMap = {
  Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5,
  Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11
};


// ================= CHECK SEASON =================
function isSeasonActive(seasonRange) {
  const [start, end] = seasonRange.split(" - ");
  const startMonth = monthMap[start];
  const endMonth = monthMap[end];

  const current = getCurrentMonth();

  if (startMonth <= endMonth) {
    return current >= startMonth && current <= endMonth;
  } else {
    return current >= startMonth || current <= endMonth;
  }
}


// ================= TIMELINE =================
function getTimeline() {
  return [
    ["Preparation", "Soil preparation", "Prepare land properly"],
    ["Sowing", "Seed sowing", "Use quality seeds"],
    ["Growth", "Fertilizer / Irrigation", "Maintain nutrients"],
    ["Protection", "Pest control", "Monitor pests regularly"],
    ["Harvest", "Harvest crop", "Harvest at right time"]
  ];
}


// ================= POPULATE CROPS =================
stateSelect.addEventListener("change", () => {
  const state = stateSelect.value;

  const filtered = dataset.filter(d => d.state === state);

  cropSelect.innerHTML = `<option value="">Select Crop</option>`;

  filtered.forEach(item => {
    const option = document.createElement("option");
    option.value = item.crop;
    option.textContent = `${item.crop} (${item.season})`;
    cropSelect.appendChild(option);
  });
});


// ================= ANALYZE =================
analyzeBtn.addEventListener("click", () => {

  const state = stateSelect.value;
  const crop = cropSelect.value;

  if (!state || !crop) {
    alert("Select state and crop");
    return;
  }

  const data = dataset.find(
    d => d.state === state && d.crop === crop
  );

  if (!data) return;

  const active = isSeasonActive(data.season);

  // ================= SUMMARY =================
  summaryBox.innerHTML = `
    <p><strong>Crop:</strong> ${data.crop}</p>
    <p><strong>Season:</strong> ${data.season}</p>
    <p><strong>Status:</strong> ${
      active 
      ? '<span style="color:green;">Active Season</span>' 
      : '<span style="color:red;">Off Season</span>'
    }</p>
  `;

  // ================= TABLE =================
  const timeline = getTimeline();
  tableBody.innerHTML = "";

  timeline.forEach((row, index) => {

    const tr = document.createElement("tr");

    const highlight = active && index >= 1 && index <= 3;

    tr.style.background = highlight ? "#e6f4ea" : "";

    tr.innerHTML = `
      <td>${row[0]}</td>
      <td>${row[1]}</td>
      <td>${data.season}</td>
      <td>
        ${row[2]}
        ${highlight ? "<br><small>⚠️ Act now</small>" : ""}
      </td>
    `;

    tableBody.appendChild(tr);
  });

});


// ================= RESET =================
resetBtn.addEventListener("click", () => {

  stateSelect.value = "";
  cropSelect.innerHTML = `<option value="">Select Crop</option>`;

  summaryBox.innerHTML = "Select a crop to view details";

  tableBody.innerHTML = `
    <tr>
      <td colspan="4">No data selected</td>
    </tr>
  `;
});