import { askAI } from "./ai-service.js";

export function attachAdminAI(panelElement) {
  panelElement.innerHTML = `
    <div class="card">
      <h2>Admin AI Console</h2>
      <textarea id="aiPrompt" rows="3" style="width:100%;"></textarea>
      <button id="aiSend" style="margin-top:8px;">Ask AI</button>
      <pre id="aiResponse" style="margin-top:12px; white-space:pre-wrap;"></pre>
    </div>
  `;

  const promptEl = panelElement.querySelector("#aiPrompt");
  const sendBtn = panelElement.querySelector("#aiSend");
  const respEl = panelElement.querySelector("#aiResponse");

  sendBtn.addEventListener("click", () => {
    const prompt = promptEl.value.trim();
    if (!prompt) return;
    const result = askAI(prompt);
    respEl.textContent = `${result.response}\n\n(${result.timestamp})`;
  });
}