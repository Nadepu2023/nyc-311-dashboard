const NYC_BLUE = "#003087";
const NYC_ORANGE = "#FF6319";
const NYC_PURPLE = "#9e11ef"

async function loadSummary() {
    const response = await fetch("http://127.0.0.1:8000/api/summary");
    const data = await response.json();
    document.getElementById("total-complaints").innerText =
        data.total_complaints.toLocaleString();
}

async function loadAverageResponseTime() {
    const response = await fetch("http://127.0.0.1:8000/api/average-response-time");
    const data = await response.json();
    const element = document.getElementById("avg-response-time");
    element.innerText = data.average_response_time_hours !== null
        ? data.average_response_time_hours + " hrs"
        : "N/A";
}

async function loadTopAgenciesData() {
    const response = await fetch("http://127.0.0.1:8000/api/top-agencies");
    return await response.json();
}

async function loadTopComplaintsData() {
    const response = await fetch("http://127.0.0.1:8000/api/top-complaints");
    return await response.json();
}

async function loadTopBoroughsData() {
    const response = await fetch("http://127.0.0.1:8000/api/complaints-by-borough");
    return await response.json();
}

async function loadAgencies() {
    const data = await loadTopAgenciesData();

    document.getElementById("top-agency").innerText = data[0].agency;

    new Chart(document.getElementById("agency-chart"), {
        type: "bar",
        data: {
            labels: data.map(a => a.agency),
            datasets: [{
                label: "Number of Complaints",
                data: data.map(a => a.count),
                backgroundColor: NYC_BLUE,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

async function loadComplaintChart() {
    const data = await loadTopComplaintsData();

    new Chart(document.getElementById("complaint-chart"), {
        type: "bar",
        data: {
            labels: data.map(c => c.complaint_type),
            datasets: [{
                label: "Number of Complaints",
                data: data.map(c => c.count),
                backgroundColor: NYC_ORANGE,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            indexAxis: "y",
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { beginAtZero: true }
            }
        }
    });
}

const PIE_COLORS = [
    "#003087", "#FF6319", "#9e11ef", "#28a745", "#e0c800",
    "#d32f2f", "#0288d1", "#f57c00"
];

async function loadBoroughChart() {
    const data = await loadTopBoroughsData();

    new Chart(document.getElementById("borough-chart"), {
        type: "pie",
        data: {
            labels: data.map(c => c.borough),
            datasets: [{
                label: "Number of Complaints",
                data: data.map(c => c.count),
                backgroundColor: PIE_COLORS,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
}

async function populateBoroughDropdown() {
    const data = await loadTopBoroughsData();  // get the list

    for (const item of data) {                 // loop over each borough
        const option = document.createElement("option");
        option.value = item.borough;
        option.innerText = item.borough;
        document.getElementById("borough-filter").appendChild(option);
    }
}

async function populateComplaintTypeDropdown() {
    const data = await loadTopComplaintsData();  // get the list

    for (const item of data) {                 // loop over each complaint
        const option = document.createElement("option");
        option.value = item.complaint_type;
        option.innerText = item.complaint_type;
        document.getElementById("complaint-filter").appendChild(option);
    }
}

document.getElementById("apply-filters").addEventListener("click", async function() {
    const borough = document.getElementById("borough-filter").value;
    const complaintType = document.getElementById("complaint-filter").value;

    let url = "http://127.0.0.1:8000/api/search?";
    if (borough) url += "borough=" + borough + "&";
    if (complaintType) url += "complaint_type=" + complaintType;

    const response = await fetch(url);
    const data = await response.json();

    console.log(data);  // check what comes back first

    const resultsDiv = document.getElementById("search-results");
    resultsDiv.innerHTML = "";

    let table = "<p class='results-count'>Showing " + data.length + " results</p>";
    table += "<table><thead><tr><th>Complaint Type</th><th>Borough</th><th>Status</th></tr></thead><tbody>";

    for (const complaint of data) {
        table += "<tr>";
        table += "<td>" + complaint.complaint_type + "</td>";
        table += "<td>" + complaint.borough + "</td>";
        table += "<td>" + complaint.status + "</td>";
        table += "</tr>";
    }

    table += "</tbody></table>";
    resultsDiv.innerHTML = table;

});


loadSummary();
loadAverageResponseTime();
loadAgencies();
loadComplaintChart();
loadBoroughChart();
populateBoroughDropdown();
populateComplaintTypeDropdown()
