document.getElementById("searchBtn").addEventListener("click", async () => {
    const skillInput = document.getElementById("skillsInput").value.trim();
    const resultDiv = document.getElementById("results");
    resultDiv.innerHTML = "";

    if (!skillInput) {
        resultDiv.innerHTML = "Enter skills!";
        return;
    }

    const keywords = skillInput.split(",").map(k => k.trim());

    try {
        const res = await fetch("http://127.0.0.1:8000/search_candidates", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ keywords })
        });

        if (!res.ok) {
            resultDiv.innerHTML = "Server error!";
            return;
        }

        const data = await res.json();
        if (data.length === 0) {
            resultDiv.innerHTML = "No match found!";
            return;
        }

        data.forEach(c => {
            const p = document.createElement("p");
            p.innerHTML = `${c.name} → Skills: ${c.skills.join(", ")}`;
            resultDiv.appendChild(p);
        });

    } catch (error) {
        resultDiv.innerHTML = "Backend not running!";
    }
});
