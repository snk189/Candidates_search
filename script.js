const searchBtn = document.getElementById("searchBtn");
const skillsInput = document.getElementById("skillsInput");
const resultsDiv = document.getElementById("results");

searchBtn.addEventListener("click", async () => {
    const skills = skillsInput.value.split(",").map(s => s.trim()).filter(s => s);
    if (skills.length === 0) {
        resultsDiv.innerHTML = "<p>Enter at least one skill.</p>";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/search_candidates", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ keywords: skills })
        });

        const data = await response.json();

        // Smart ranking: candidates with more matching skills appear first
        const ranked = data.matching_candidates.map(c => {
            const matchCount = c.skills.filter(s => skills.map(k => k.toLowerCase()).includes(s.toLowerCase())).length;
            return { ...c, matchCount };
        }).sort((a, b) => b.matchCount - a.matchCount || a.name.localeCompare(b.name));

        if (ranked.length === 0) {
            resultsDiv.innerHTML = "<p>No matching candidates found.</p>";
        } else {
            resultsDiv.innerHTML = ranked.map(c => `
                <div class="candidate">
                    <strong>${c.name}</strong><br>
                    Email: ${c.email}<br>
                    Phone: ${c.phone}<br>
                    Skills: ${c.skills.join(", ")}<br>
                    Quiz Score: ${c.quiz_score}
                </div>
            `).join("");
        }

    } catch (err) {
        resultsDiv.innerHTML = "<p>Error fetching data from backend.</p>";
        console.error(err);
    }
});
