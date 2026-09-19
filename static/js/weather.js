// ==============================
// 🌍 AUTO LOCATION WEATHER
// ==============================
function getLocationWeather() {

  const status = document.getElementById("status");
  const box = document.getElementById("weatherBox");

  if (!navigator.geolocation) {
    status.innerText = "Geolocation not supported ❌";
    return;
  }

  status.innerText = "📡 Detecting your location...";

  navigator.geolocation.getCurrentPosition(
    async (position) => {

      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      status.innerText = "🌐 Fetching live weather...";

      try {
        const res = await fetch(`/weather_by_coords?lat=${lat}&lon=${lon}`);

        // DEBUG
        console.log("GPS RESPONSE STATUS:", res.status);

        const data = await res.json();
        console.log("GPS DATA:", data);

        if (!res.ok || data.error) {
          status.innerText = data.error || "Failed to load weather ❌";
          return;
        }

        showWeather(data);
        status.innerText = "📍 Your Location";

      } catch (err) {
        console.error("GPS ERROR:", err);
        status.innerText = "Error fetching weather ❌";
      }
    },

    (error) => {
      console.error("GEO ERROR:", error);

      status.innerText =
        "❌ Location blocked — allow permission or use search below";
    }
  );
}


// ==============================
// 🔍 MANUAL CITY SEARCH
// ==============================
async function getWeatherByCity() {

  const status = document.getElementById("status");
  const city = document.getElementById("cityInput").value.trim();

  if (!city) {
    alert("Enter city name");
    return;
  }

  status.innerText = "🔍 Searching weather...";

  try {
    const res = await fetch(`/weather?city=${city}`);

    console.log("CITY RESPONSE STATUS:", res.status);

    const data = await res.json();
    console.log("CITY DATA:", data);

    if (!res.ok || data.error) {
      status.innerText = data.error || "City not found ❌";
      return;
    }

    showWeather(data);
    status.innerText = "📍 " + data.city;

  } catch (err) {
    console.error("CITY ERROR:", err);
    status.innerText = "Error fetching weather ❌";
  }
}


// ==============================
// 🎯 DISPLAY WEATHER UI
// ==============================
function showWeather(data) {

  const box = document.getElementById("weatherBox");

  box.innerHTML = `
    <div style="
      margin-top:20px;
      padding:20px;
      background:#f4f7f6;
      border-radius:12px;
      box-shadow:0 5px 15px rgba(0,0,0,0.08);
    ">
      <h2 style="margin-bottom:10px;">📍 ${data.city}</h2>

      <p>🌡 <b>Temperature:</b> ${data.temp} °C</p>
      <p>💧 <b>Humidity:</b> ${data.humidity}%</p>
      <p>🌥 <b>Condition:</b> ${data.condition}</p>
    </div>
  `;
}


// ==============================
// 🚀 AUTO RUN ON PAGE LOAD
// ==============================
window.onload = () => {
  getLocationWeather();
};