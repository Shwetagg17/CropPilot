const input = document.getElementById("cropInput");
const dropdown = document.getElementById("dropdownList");

// open dropdown
input.addEventListener("click", () => {
  dropdown.classList.toggle("show");
});

// select item
document.querySelectorAll(".item").forEach(item => {
  item.addEventListener("click", () => {
    input.value = item.innerText;
    dropdown.classList.remove("show");
  });
});

// close outside
document.addEventListener("click", (e) => {
  if (!e.target.closest(".dropdown")) {
    dropdown.classList.remove("show");
  }
});

async function getNutrition() {

  const crop = document.getElementById("cropInput").value;

  if (!crop) {
    alert("Select crop");
    return;
  }

  const res = await fetch(`/crop_nutrition?crop=${crop}`);
  const data = await res.json();

  if (data.error) {
    document.getElementById("result").innerHTML = data.error;
    return;
  }

  let usageList = "";
  data.usage.forEach(u => {
    usageList += `<li>${u}</li>`;
  });

  document.getElementById("result").innerHTML = `
    <h3>${crop} Summary</h3>

    <div class="section">
      <h4>🍽 Nutrition</h4>
      <div class="tags">
        <span>Protein: ${data.protein}</span>
        <span>Carbs: ${data.carbs}</span>
        <span>Fats: ${data.fats}</span>
      </div>
    </div>

    <div class="section">
      <h4>🌱 Soil Requirement</h4>
      <div class="tags">
        <span>N: ${data.N}</span>
        <span>P: ${data.P}</span>
        <span>K: ${data.K}</span>
      </div>
    </div>

    <div class="section">
      <h4>🏭 Industry Usage</h4>
      <ul>${usageList}</ul>
    </div>
  `;
}