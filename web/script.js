const API_URL = "http://localhost:5000";

async function sendCommand() {
    const input = document.getElementById("command");
    const output = document.getElementById("generated-code");
    const prompt = input.value.trim();

    if (!prompt) {
        alert("Please enter a valid prompt!");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

        const result = await response.json();

        if (result.error) {
            alert(`Error: ${result.error}`);
        } else {
            output.textContent = result.code;
            setTimeout(refreshRender, 2000);
        }
    } catch (error) {
        alert(`Execution failed: ${error.message}`);
    }
}

function refreshRender() {
    document.getElementById("blender-render").src = `/render?t=${Date.now()}`;
}

function copyCode() {
    navigator.clipboard.writeText(document.getElementById("generated-code").textContent)
        .then(() => alert("Code copied successfully ✅"))
        .catch(() => alert("Failed to copy ❌"));
}
