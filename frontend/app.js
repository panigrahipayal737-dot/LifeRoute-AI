console.log("PulseRoute Frontend Web Gateway Initialized.");
async function fetchStatus() {
    try {
        const res = await fetch("http://localhost:8000/api/v1/status");
        if(res.ok) {
            const data = await res.json();
            console.log("Telemetry Received:", data);
        }
    } catch (e) {}
}
setInterval(fetchStatus, 3000);
