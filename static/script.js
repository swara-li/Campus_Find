
const reportForm = document.getElementById("reportForm");
const formMessage = document.getElementById("formMessage");
const reportsContainer = document.getElementById("reportsContainer");
const searchInput = document.getElementById("searchInput");
const filterType = document.getElementById("filterType");

// Submit a new Lost or Found report
reportForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const report = {
        item_name: document.getElementById("item_name").value.trim(),
        report_type: document.getElementById("report_type").value,
        category: document.getElementById("category").value,
        description: document.getElementById("description").value.trim(),
        location: document.getElementById("location").value.trim(),
        contact: document.getElementById("contact").value.trim()
    };

    try {
        const response = await fetch("/api/reports", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(report)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not submit report");
        }

        formMessage.textContent = "Report submitted successfully!";
        formMessage.style.color = "green";

        reportForm.reset();
        loadReports();

    } catch (error) {
        formMessage.textContent = error.message;
        formMessage.style.color = "red";
    }
});


// Load reports from the database
async function loadReports() {
    const search = searchInput.value.trim();
    const type = filterType.value;

    const params = new URLSearchParams();

    if (search) params.append("q", search);
    if (type) params.append("type", type);

    reportsContainer.textContent = "Loading reports...";

    try {
        const response = await fetch(`/api/reports?${params.toString()}`);

        if (!response.ok) {
            throw new Error("Could not load reports");
        }

        const reports = await response.json();

        reportsContainer.replaceChildren();

        if (reports.length === 0) {
            reportsContainer.textContent = "No open reports found.";
            return;
        }

        reports.forEach(function (report) {
            const card = document.createElement("div");
            card.className = "report-card";

            const heading = document.createElement("h3");
            heading.textContent = report.item_name;

            const details = [
                `Type: ${report.report_type}`,
                `Category: ${report.category}`,
                `Description: ${report.description || "Not provided"}`,
                `Location: ${report.location}`,
                `Contact: ${report.contact}`
            ];

            card.appendChild(heading);

            details.forEach(function (detail) {
                const paragraph = document.createElement("p");
                paragraph.textContent = detail;
                card.appendChild(paragraph);
            });

            const resolveButton = document.createElement("button");
            resolveButton.textContent = "Mark as Resolved";

            resolveButton.addEventListener("click", function () {
                resolveReport(report.id);
            });

            card.appendChild(resolveButton);
            reportsContainer.appendChild(card);
        });

    } catch (error) {
        reportsContainer.textContent = error.message;
    }
}


// Mark a report as resolved
async function resolveReport(reportId) {
    const confirmed = confirm("Are you sure you want to mark this report as resolved?");

    if (!confirmed) return;

    try {
        const response = await fetch(`/api/reports/${reportId}/resolve`, {
            method: "PATCH"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not update report");
        }

        loadReports();

    } catch (error) {
        alert(error.message);
    }
}


// Search and filter reports
searchInput.addEventListener("input", loadReports);
filterType.addEventListener("change", loadReports);


// Display reports when the page opens
loadReports();
