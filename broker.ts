/**
 * mset-ai-pipeline broker — Bun HTTP server, port 7801
 * In-memory message queues + SSE push, no external dependencies.
 */

interface AgentRecord {
  name: string;
  registered_at: string;
}

interface Message {
  from: string;
  to: string;
  type: string;
  payload: Record<string, unknown>;
  queued_at: string;
}

interface SendBody {
  from: string;
  to: string;
  type: string;
  payload?: Record<string, unknown>;
}

interface RegisterBody {
  agent: string;
}

const agents = new Map<string, AgentRecord>();
const queues = new Map<string, Message[]>();
const sseConnections = new Map<string, ReadableStreamDefaultController<Uint8Array>[]>();

const encoder = new TextEncoder();

function getQueue(agent: string): Message[] {
  if (!queues.has(agent)) queues.set(agent, []);
  return queues.get(agent)!;
}

function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function errorResponse(msg: string, status = 400): Response {
  return jsonResponse({ error: msg }, status);
}

function pushToSSE(agent: string, msg: Message): void {
  const conns = sseConnections.get(agent);
  if (!conns || conns.length === 0) return;
  const data = encoder.encode(`data: ${JSON.stringify(msg)}\n\n`);
  const alive: ReadableStreamDefaultController<Uint8Array>[] = [];
  for (const ctrl of conns) {
    try {
      ctrl.enqueue(data);
      alive.push(ctrl);
    } catch {
      // connection closed — drop it
    }
  }
  sseConnections.set(agent, alive);
  if (alive.length < conns.length) {
    console.log(`[stream] pruned ${conns.length - alive.length} dead connection(s) for ${agent}`);
  }
}

Bun.serve({
  port: 7801,
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);
    const method = req.method;
    const path = url.pathname;

    // POST /register
    if (method === "POST" && path === "/register") {
      let body: RegisterBody;
      try {
        body = (await req.json()) as RegisterBody;
      } catch {
        return errorResponse("Invalid JSON");
      }
      if (!body.agent || typeof body.agent !== "string") {
        return errorResponse("Missing field: agent");
      }
      const record: AgentRecord = {
        name: body.agent,
        registered_at: new Date().toISOString(),
      };
      agents.set(body.agent, record);
      getQueue(body.agent);
      console.log(`[register] ${body.agent}`);
      return jsonResponse({ ok: true, agent: record });
    }

    // POST /send
    if (method === "POST" && path === "/send") {
      let body: SendBody;
      try {
        body = (await req.json()) as SendBody;
      } catch {
        return errorResponse("Invalid JSON");
      }
      if (!body.from || !body.to || !body.type) {
        return errorResponse("Missing fields: from, to, type");
      }
      const msg: Message = {
        from: body.from,
        to: body.to,
        type: body.type,
        payload: body.payload ?? {},
        queued_at: new Date().toISOString(),
      };
      // Queue for poll-based fallback
      getQueue(body.to).push(msg);
      // Push to SSE if connected
      pushToSSE(body.to, msg);
      console.log(`[send] ${body.from} → ${body.to} (${body.type})`);
      return jsonResponse({ ok: true, queued: msg });
    }

    // GET /stream/:agent — SSE push endpoint
    const streamMatch = path.match(/^\/stream\/(.+)$/);
    if (method === "GET" && streamMatch) {
      const agent = streamMatch[1];

      let ctrl!: ReadableStreamDefaultController<Uint8Array>;

      const stream = new ReadableStream<Uint8Array>({
        start(c) {
          ctrl = c;
          if (!sseConnections.has(agent)) sseConnections.set(agent, []);
          sseConnections.get(agent)!.push(ctrl);
          console.log(`[stream] ${agent} connected`);
          c.enqueue(encoder.encode(": connected\n\n"));
        },
        cancel() {
          const conns = sseConnections.get(agent);
          if (conns) {
            const idx = conns.indexOf(ctrl);
            if (idx !== -1) conns.splice(idx, 1);
          }
          clearInterval(heartbeat);
          console.log(`[stream] ${agent} disconnected`);
        },
      });

      // Heartbeat every 30s to keep connection alive through proxies
      const heartbeat = setInterval(() => {
        try {
          ctrl.enqueue(encoder.encode(": heartbeat\n\n"));
        } catch {
          clearInterval(heartbeat);
        }
      }, 30_000);

      return new Response(stream, {
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
        },
      });
    }

    // GET /poll/:agent — poll-based fallback (still supported)
    const pollMatch = path.match(/^\/poll\/(.+)$/);
    if (method === "GET" && pollMatch) {
      const agent = pollMatch[1];
      const msgs = getQueue(agent);
      const pending = [...msgs];
      msgs.length = 0;
      console.log(`[poll] ${agent} → ${pending.length} message(s)`);
      return jsonResponse({ agent, messages: pending });
    }

    // GET /agents
    if (method === "GET" && path === "/agents") {
      return jsonResponse({ agents: [...agents.values()] });
    }

    return errorResponse("Not found", 404);
  },
});

console.log("mset-ai-pipeline broker running on http://localhost:7801");
