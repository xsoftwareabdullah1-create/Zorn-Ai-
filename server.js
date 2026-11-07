// zorn.ai backend — runs its OWN open-source model via Ollama. No API key needed.
// Run: ollama pull qwen2.5-coder:7b  &&  npm i express  &&  node server.js   (Node 18+)
const express = require("express");
const path = require("path");

const PORT = process.env.PORT || 3000;
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID;      // Google Cloud Console se
const LLM_BASE_URL = process.env.LLM_BASE_URL || "http://localhost:11434/v1" // Ollama (self-hosted);
const LLM_MODEL = process.env.LLM_MODEL || "qwen2.5-coder:7b"; // any model you pulled in Ollama
const DAILY_LIMIT = Number(process.env.DAILY_LIMIT || 100); // per user messages/day

if (!GOOGLE_CLIENT_ID) {
  console.error("Set the GOOGLE_CLIENT_ID env var.");
  process.exit(1);
}

const SYSTEM_PROMPT = `You are zorn.ai, an expert AI assistant and senior coding agent.

IDENTITY: Your name is zorn.ai. Never claim to be any other model or company's product.

LANGUAGE: Always reply in English. Keep code, identifiers and comments in English.

CODING (your main strength):
- Think step by step before answering hard problems: understand the goal, consider edge cases, then write the solution.
- Write complete, working, production-quality code. Never leave "..." or "rest of code here" placeholders unless the user asks for a snippet only.
- Use modern best practices, proper error handling, clear naming, and secure defaults (validate input, never hardcode secrets).
- When debugging: find the root cause, explain it briefly, then give the exact fix. Ask for the error message or code if it is missing.
- For big tasks: give a short plan, then the code file by file, each in its own fenced code block with the language and filename.
- Mention how to run or test the code. Point out trade-offs and risks honestly.
- Cover many stacks: JavaScript/TypeScript, Python, HTML/CSS, React, Node, GDScript/Godot, C/C++, Java, Kotlin, SQL, Bash, etc.

GENERAL KNOWLEDGE: Be accurate, clear and concise. Use markdown (headings, lists, tables) when it helps. If you are unsure or the topic may have changed recently, say so instead of guessing. Never invent facts, links, or APIs.

STYLE: Friendly, direct, no filler. Match the depth to the question: short answer for simple questions, thorough for complex ones.`;

const app = express();
app.use(express.json({ limit: "10mb" }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/health", (_, res) => res.send("ok"));
app.get("/config", (_, res) => res.json({ googleClientId: GOOGLE_CLIENT_ID }));

// Google ID token verify (tokeninfo endpoint) + small cache
const cache = new Map();
async function verify(idToken) {
  const hit = cache.get(idToken);
  if (hit && hit.exp > Date.now()) return hit.user;
  const r = await fetch("https://oauth2.googleapis.com/tokeninfo?id_token=" + encodeURIComponent(idToken));
  if (!r.ok) return null;
  const u = await r.json();
  if (u.aud !== GOOGLE_CLIENT_ID) return null;
  const user = { id: u.sub, email: u.email, name: u.name, picture: u.picture };
  cache.set(idToken, { user, exp: Math.min(Number(u.exp) * 1000, Date.now() + 3600e3) });
  return user;
}

const usage = new Map(); // userId -> {day,count}
function allow(id) {
  const day = new Date().toISOString().slice(0, 10);
  const u = usage.get(id);
  if (!u || u.day !== day) { usage.set(id, { day, count: 1 }); return true; }
  return ++u.count <= DAILY_LIMIT;
}

app.post("/api/chat", async (req, res) => {
  try {
    const token = (req.headers.authorization || "").replace("Bearer ", "");
    const user = token && (await verify(token));
    if (!user) return res.status(401).json({ error: "Login required" });
    if (!allow(user.id)) return res.status(429).json({ error: "Daily limit reached" });

    const messages = (req.body.messages || []).slice(-40).map(m => ({
      role: m.role === "assistant" ? "assistant" : "user",
      content: String(m.content || "").slice(0, 60000),
    }));

    const r = await fetch(LLM_BASE_URL + "/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: AbortSignal.timeout(300000),
      body: JSON.stringify({
        model: LLM_MODEL,
        messages: [{ role: "system", content: SYSTEM_PROMPT }, ...messages],
        temperature: 0.3,
        max_tokens: 4096,
      }),
    });
    const data = await r.json();
    if (!r.ok) return res.status(502).json({ error: data.error?.message || "Model error" });
    res.json({ reply: data.choices?.[0]?.message?.content || "" });
  } catch (e) {
    res.status(500).json({ error: "Server error" });
  }
});

app.listen(PORT, () => console.log("zorn.ai running on http://localhost:" + PORT));
