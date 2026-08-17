import express from "express";
import path from "path";
import fs from "fs";
import { createServer as createViteServer } from "vite";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json({ limit: "50mb" }));

  // CORS middleware to ensure iframe & browser access
  app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    if (req.method === "OPTIONS") {
      return res.sendStatus(200);
    }
    next();
  });

  // Health endpoint
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", app: "Campus Connect ERP", time: new Date().toISOString() });
  });

  // Base64 JSON download endpoint
  app.get("/api/zip-base64", (req, res) => {
    try {
      const zipPath = path.join(process.cwd(), "CampusConnect_ERP_Production.zip");
      if (!fs.existsSync(zipPath)) {
        return res.status(404).json({ error: "ZIP file not found" });
      }
      const zipBuffer = fs.readFileSync(zipPath);
      const base64 = zipBuffer.toString("base64");
      res.json({
        success: true,
        filename: "CampusConnect_ERP_Production.zip",
        size: zipBuffer.length,
        base64: base64,
      });
    } catch (err: any) {
      res.status(500).json({ error: "Failed to read ZIP", details: err?.message });
    }
  });

  // Production ZIP download endpoint with explicit headers
  app.get(["/download-zip", "/api/download-zip", "/CampusConnect_ERP_Production.zip", "/campus_connect.zip"], (req, res) => {
    const zipPath = path.join(process.cwd(), "CampusConnect_ERP_Production.zip");
    if (!fs.existsSync(zipPath)) {
      return res.status(404).json({ error: "ZIP file not found" });
    }
    const stat = fs.statSync(zipPath);
    res.writeHead(200, {
      "Content-Type": "application/zip",
      "Content-Disposition": 'attachment; filename="CampusConnect_ERP_Production.zip"',
      "Content-Length": stat.size,
      "Cache-Control": "no-cache, no-store, must-revalidate",
    });
    const readStream = fs.createReadStream(zipPath);
    readStream.pipe(res);
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Campus Connect ERP server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();

