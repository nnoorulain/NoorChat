const messages = document.querySelector("#messages");
const form = document.querySelector("#chat-form");
const input = document.querySelector("#message");
const reset = document.querySelector("#reset");
const send = document.querySelector("#send");
const suggestions = document.querySelectorAll("[data-message]");
const historyList = document.querySelector("#chat-history");
const companionToggle = document.querySelector("#companion-toggle");
const companionStage = document.querySelector("#companion-stage");
const companionNext = document.querySelector("#companion-next");
const companionImage = document.querySelector("#companion-image");
const companionFrameLabel = document.querySelector("#companion-frame-label");
const companionFrames = [
  { image: "/companion.webp", label: "Portrait", alt: "Noor in a black shirt and glasses" },
  { image: "/companion-laptop.webp", label: "Laptop", alt: "Noor with an open laptop" },
  { image: "/companion-phone.webp", label: "Phone", alt: "Noor holding a smartphone" },
];
let companionIndex = 0;
let busy = false;
let activeChatId = null;
let savedChats = [];

function addMessage(who, text, method) {
  const entry = document.createElement("div");
  entry.className = "entry " + (who === "You" ? "user" : "bot");

  const label = document.createElement("div");
  label.className = "message-label";
  label.textContent = who;

  const bubble = document.createElement("p");
  bubble.className = "bubble";
  bubble.textContent = text;

  entry.append(label, bubble);
  if (method) {
    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = method;
    entry.append(badge);
  }
  messages.append(entry);
  messages.scrollTop = messages.scrollHeight;
}

function startChat() {
  messages.replaceChildren();
  addMessage("NoorChat", "Hi! I'm NoorChat. Ask me about NLP, Python, or how I find my replies.");
}

function setBusy(value) {
  busy = value;
  send.disabled = value;
  reset.disabled = value;
}

function showChat(chat) {
  activeChatId = chat ? chat.id : null;
  startChat();
  if (chat) {
    for (const exchange of chat.exchanges) {
      addMessage("You", exchange.message);
      addMessage("NoorChat", exchange.reply, exchange.method);
    }
  }
  renderHistory();
}

function renderHistory(emptyMessage = "Send a message to save your first chat.") {
  historyList.replaceChildren();
  if (!savedChats.length) {
    const note = document.createElement("p");
    note.className = "history-note";
    note.textContent = emptyMessage;
    historyList.append(note);
    return;
  }
  for (const chat of savedChats) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "history-chat";
    button.textContent = chat.exchanges[0].message;
    if (chat.id === activeChatId) button.setAttribute("aria-current", "true");
    button.addEventListener("click", () => {
      if (busy) return;
      loadSavedChats(chat.id);
      input.value = "";
      input.focus();
    });
    historyList.append(button);
  }
}

async function loadSavedChats(chatId = null) {
  setBusy(true);
  try {
    const response = await fetch("/history");
    if (!response.ok) throw new Error("History request failed");
    const result = await response.json();
    savedChats = result.chats;
    if (chatId) {
      showChat(savedChats.find((chat) => chat.id === chatId));
    } else {
      renderHistory();
    }
  } catch {
    savedChats = [];
    renderHistory("Saved chats could not be loaded.");
  } finally {
    setBusy(false);
  }
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message || busy) return;

  setBusy(true);
  input.value = "";
  addMessage("You", message);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, chat_id: activeChatId }),
    });
    const result = await response.json();
    if (!response.ok) {
      addMessage("NoorChat", result.error);
      return;
    }
    savedChats = result.chats;
    if (activeChatId && activeChatId !== result.chat_id) {
      showChat(savedChats.find((chat) => chat.id === result.chat_id));
    } else {
      activeChatId = result.chat_id;
      addMessage("NoorChat", result.reply, result.method);
      renderHistory();
    }
  } catch {
    addMessage("NoorChat", "I couldn't reach the chatbot. Check that app.py is running, then try again.");
  } finally {
    setBusy(false);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
  input.focus();
});

suggestions.forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.message));
});

reset.addEventListener("click", () => {
  showChat(null);
  input.value = "";
  input.focus();
});

function updateCompanion() {
  companionStage.hidden = !companionToggle.checked;
}

function nextCompanionFrame() {
  companionIndex = (companionIndex + 1) % companionFrames.length;
  const frame = companionFrames[companionIndex];
  companionImage.src = frame.image;
  companionImage.alt = frame.alt;
  companionFrameLabel.textContent = `${frame.label} · ${companionIndex + 1} of ${companionFrames.length}`;
}

companionToggle.addEventListener("change", updateCompanion);
companionNext.addEventListener("pointerenter", (event) => {
  if (event.pointerType === "mouse") nextCompanionFrame();
});
companionNext.addEventListener("pointerup", (event) => {
  if (event.pointerType === "touch" || event.pointerType === "pen") nextCompanionFrame();
});
companionNext.addEventListener("click", (event) => {
  // A keyboard activation has no pointer clicks.
  if (event.detail === 0) nextCompanionFrame();
});
updateCompanion();
startChat();
loadSavedChats();
