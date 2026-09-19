let chart = null;

async function loadData() {

    const crop =
        document.getElementById("cropInput").value;

    if (!crop) {

        alert("Select crop");
        return;
    }

    try {

        const response =
            await fetch(`/market_data?crop=${crop}`);

        const data =
            await response.json();

        console.log(data);

        // =========================
        // ERROR
        // =========================

        if (data.error) {

            alert(data.error);
            return;
        }

        // =========================
        // BEST MARKET
        // =========================

        document.getElementById("bestMarket").innerHTML = `

            <div class="best-box">

                <h3>🏆 Best Market</h3>

                <h2>${data.best_market.market}</h2>

                <p>${data.best_market.state}</p>

                <h1>₹${data.best_market.modal_price}</h1>

            </div>

        `;

        // =========================
        // TABLE DATA
        // =========================

        let rows = "";

        data.top.forEach(item => {

            rows += `

                <tr>

                    <td>${item.market}</td>

                    <td>${item.state}</td>

                    <td>${item.commodity}</td>

                    <td>₹${item.modal_price}</td>

                </tr>

            `;
        });

        document.getElementById("tableBody").innerHTML =
            rows;

        // =========================
        // CHART
        // =========================

        const ctx =
            document.getElementById("chart").getContext("2d");

        if (chart) {

            chart.destroy();
        }

        chart = new Chart(ctx, {

            type: "line",

            data: {

                labels:
                    data.trend.map(
                        item => item.arrival_date
                    ),

                datasets: [{

                    label: "Market Price Trend",

                    data:
                        data.trend.map(
                            item => item.modal_price
                        ),

                    borderWidth: 3,

                    tension: 0.3,

                    fill: false
                }]
            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        display: true
                    }
                },

                scales: {

                    y: {

                        beginAtZero: false
                    }
                }
            }
        });

    }

    catch (error) {

        console.log(error);

        alert("Failed to load market data");
    }
}

function resetData() {

    document.getElementById("cropInput").value = "";

    document.getElementById("bestMarket").innerHTML = `

        Select crop to view best market

    `;

    document.getElementById("tableBody").innerHTML = `

        <tr>

            <td colspan="4">

                No data

            </td>

        </tr>

    `;

    if (chart) {

        chart.destroy();
    }
}