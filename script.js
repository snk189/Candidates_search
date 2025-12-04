const searchBtn = document.getElementById("searchBtn");
const resultsDiv = document.getElementById("results");

searchBtn.addEventListener("click", async () => {
    const input = document.getElementById("skillsInput").value;
    const keywords = input.split(",").map(s => s.trim()).filter(s => s);

    if (keywords.length === 0) {
        resultsDiv.innerHTML = "<p>Please enter at least one skill.</p>";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/search_candidates", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ keywords })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        const candidates = data.matching_candidates;

        if (candidates.length === 0) {
            resultsDiv.innerHTML = "<p>No matching candidates found.</p>";
            return;
        }

        resultsDiv.innerHTML = candidates.map(c => `
            <div class="candidate">
                <strong>Name:</strong> ${c.name} <br>
                <strong>Email:</strong> ${c.email} <br>
                <strong>Phone:</strong> ${c.phone} <br>
                <strong>Skills:</strong> ${c.skills.join(", ")} <br>
                <strong>Quiz Score:</strong> ${c.quiz_score}
            </div>
        `).join("");

    } catch (err) {
        console.error(err);
        resultsDiv.innerHTML = "<p>Error fetching candidates.</p>";
    }
});
