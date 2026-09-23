import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="OKD / K8s YAML Secret Generator")

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OKD / Kubernetes YAML Secret Generator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #0d1117;
      --bg-panel: #161b22;
      --bg-panel-header: #1f242c;
      --border-color: #30363d;
      --text-main: #c9d1d9;
      --text-bright: #f0f6fc;
      --text-muted: #8b949e;
      --accent-blue: #388bfd;
      --accent-blue-hover: #1f6feb;
      --accent-green: #238636;
      --accent-green-hover: #2ea043;
      --code-bg: #090d13;
      --font-family: 'IBM Plex Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-family);
      background-color: var(--bg-main);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    input, button, textarea {
      font-family: inherit;
    }

    header {
      background-color: var(--bg-panel);
      border-bottom: 1px solid var(--border-color);
      padding: 16px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-badge {
      background: linear-gradient(135deg, #1f6feb, #8957e5);
      color: white;
      font-weight: 700;
      font-size: 13px;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }

    .brand h1 {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-bright);
    }

    .top-controls {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .input-label {
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 600;
    }

    .secret-input {
      background-color: var(--code-bg);
      border: 1px solid var(--border-color);
      color: #7ee787;
      font-family: var(--font-family);
      font-size: 14px;
      font-weight: 600;
      padding: 7px 12px;
      border-radius: 6px;
      outline: none;
      width: 220px;
      transition: border-color 0.2s;
    }

    .secret-input:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 2px rgba(56, 139, 253, 0.2);
    }

    main {
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 0.65fr 1.15fr 1.15fr;
      gap: 16px;
      padding: 20px 24px;
    }

    @media (max-width: 1400px) {
      main {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 760px) {
      main {
        grid-template-columns: 1fr;
      }

      header {
        align-items: flex-start;
        flex-direction: column;
        gap: 12px;
      }

      .top-controls {
        justify-content: flex-start;
      }
    }

    .card {
      background-color: var(--bg-panel);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }

    .card-header {
      background-color: var(--bg-panel-header);
      border-bottom: 1px solid var(--border-color);
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .card-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-bright);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .badge-count {
      background-color: #21262d;
      color: #58a6ff;
      font-size: 11px;
      font-family: var(--font-family);
      padding: 2px 7px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
    }

    .card-body {
      flex: 1;
      padding: 0;
      display: flex;
      flex-direction: column;
    }

    textarea {
      flex: 1;
      width: 100%;
      min-height: 480px;
      background-color: var(--code-bg);
      border: none;
      color: var(--text-bright);
      font-family: var(--font-family);
      font-size: 13px;
      line-height: 1.6;
      padding: 14px;
      resize: none;
      outline: none;
      white-space: pre;
    }

    .output-area {
      color: #a5d6ff;
    }

    .btn {
      font-family: var(--font-family);
      font-size: 12px;
      font-weight: 600;
      border: 1px solid transparent;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }

    .btn-green {
      background-color: var(--accent-green);
      color: white;
    }
    .btn-green:hover {
      background-color: var(--accent-green-hover);
    }

    .btn-blue {
      background-color: var(--accent-blue);
      color: white;
    }
    .btn-blue:hover {
      background-color: var(--accent-blue-hover);
    }

    .btn-ghost {
      background-color: transparent;
      color: var(--text-muted);
      border-color: var(--border-color);
    }
    .btn-ghost:hover {
      color: var(--text-bright);
      background-color: #21262d;
    }

    .btn-group {
      display: flex;
      gap: 8px;
    }

    footer {
      border-top: 1px solid var(--border-color);
      padding: 10px 24px;
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: var(--bg-panel);
    }

    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background-color: #238636;
      color: white;
      font-size: 13px;
      font-weight: 600;
      padding: 10px 18px;
      border-radius: 6px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      display: none;
      align-items: center;
      gap: 8px;
      z-index: 9999;
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <span class="brand-badge">OKD / K8S</span>
      <h1>Secret Env Generator</h1>
    </div>
    <div class="top-controls">
      <span class="input-label">Secret Target Name:</span>
      <input type="text" id="secretName" class="secret-input" value="apps-data" placeholder="Nama secret...">
      <span class="input-label">Namespace:</span>
      <input type="text" id="namespaceInput" class="secret-input" placeholder="Opsional...">
    </div>
  </header>

  <main>
    <!-- Card 1: Input Asli -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>1. Paste Manifest / Env Input</span>
        </div>
        <button class="btn btn-ghost" onclick="clearInput()">Clear</button>
      </div>
      <div class="card-body">
        <textarea id="rawInput" placeholder="- name: APP_KEY&#10;    value: xxxxxx&#10;- name: API_KEY&#10;    value: xxxxxx&#10;&#10;Atau langsung paste daftar nama variabel baris per baris..."></textarea>
      </div>
    </div>

    <!-- Card 2: Extracted Keys (Seperti Foto) -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>2. Extracted Names</span>
          <span class="badge-count" id="keyCount">0 keys</span>
        </div>
        <button class="btn btn-ghost" onclick="copyText('extractedKeys')">Copy</button>
      </div>
      <div class="card-body">
        <textarea id="extractedKeys" readonly placeholder="Daftar nama variabel akan muncul di sini..."></textarea>
      </div>
    </div>

    <!-- Card 3: Generated YAML Output -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>3. Final YAML (Ready to Copy)</span>
        </div>
        <div class="btn-group">
          <button class="btn btn-green" onclick="copyText('yamlOutput')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Copy YAML
          </button>
        </div>
      </div>
      <div class="card-body">
        <textarea id="yamlOutput" class="output-area" readonly placeholder="YAML hasil generate otomatis akan muncul di sini..."></textarea>
      </div>
    </div>

    <!-- Card 4: Secret YAML dengan data Base64 -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>4. Secret YAML (Full Format)</span>
        </div>
        <button class="btn btn-green" onclick="copyText('secretYamlOutput')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          Copy Secret
        </button>
      </div>
      <div class="card-body">
        <textarea id="secretYamlOutput" class="output-area" readonly placeholder="Secret YAML dengan value Base64 akan muncul di sini..."></textarea>
      </div>
    </div>

    <!-- Card 5: Secret YAML siap disimpan sebagai secret.yaml -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>5. secret.yaml (stringData)</span>
        </div>
        <div class="btn-group">
          <button class="btn btn-ghost" onclick="copyText('injectSecretOutput')">Copy</button>
          <button class="btn btn-green" onclick="downloadSecretYaml()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Download secret.yaml
          </button>
        </div>
      </div>
      <div class="card-body">
        <textarea id="injectSecretOutput" class="output-area" readonly placeholder="Manifest stringData siap diunduh sebagai secret.yaml akan muncul di sini..."></textarea>
      </div>
    </div>
  </main>

  <footer>
    <span>Auto-generated in real-time. Data secret diproses lokal di browser.</span>
    <span>Runs on Docker</span>
  </footer>

  <div id="toast" class="toast">✓ Berhasil disalin ke clipboard!</div>

  <script>
    const rawInput = document.getElementById('rawInput');
    const secretName = document.getElementById('secretName');
    const namespaceInput = document.getElementById('namespaceInput');
    const extractedKeys = document.getElementById('extractedKeys');
    const yamlOutput = document.getElementById('yamlOutput');
    const secretYamlOutput = document.getElementById('secretYamlOutput');
    const injectSecretOutput = document.getElementById('injectSecretOutput');
    const keyCount = document.getElementById('keyCount');

    // Default sample data
    const defaultSample = `- name: APP_KEY\n    value: xxxxxx\n- name: API_KEY\n    value: xxxxxx\n- name: API_KEY_SR\n    value: xxxxxx\n- name: GEMINI_API_KEY\n    value: xxxxxx\n- name: DB_PASSWORD\n    value: xxxxxx\n- name: REDIS_PASSWORD\n    value: xxxxxx\n- name: AWS_ACCESS_KEY_ID\n    value: xxxxxx\n- name: AWS_SECRET_ACCESS_KEY\n    value: xxxxxx\n- name: DB_PASSWORD2\n    value: xxxxxx`;

    rawInput.value = defaultSample;

    function normalizeKey(value) {
      return value.trim().replace(/\\_/g, '_');
    }

    function parseYamlScalar(rawValue) {
      const value = rawValue.trim();

      if (value.length >= 2 && value.startsWith('"') && value.endsWith('"')) {
        try {
          return JSON.parse(value);
        } catch (_) {
          return value.slice(1, -1);
        }
      }

      if (value.length >= 2 && value.startsWith("'") && value.endsWith("'")) {
        return value.slice(1, -1).replace(/''/g, "'");
      }

      return value.replace(/\s+#.*$/, '');
    }

    function extractEntries(text) {
      const lines = text.split(/\r?\n/);
      const entries = [];
      let currentEntry = null;

      for (let line of lines) {
        line = line.trim();
        if (!line) continue;

        // Mendukung "- name: KEY", "name: KEY", serta nama yang diberi tanda petik.
        const nameMatch = line.match(/^(?:-\s*)?name\s*:\s*(?:"([^"]+)"|'([^']+)'|([^\s#]+))/i);
        if (nameMatch) {
          currentEntry = {
            name: normalizeKey(nameMatch[1] || nameMatch[2] || nameMatch[3]),
            value: '',
          };
          entries.push(currentEntry);
          continue;
        }

        const valueMatch = line.match(/^value\s*:\s*(.*)$/i);
        if (valueMatch && currentEntry) {
          currentEntry.value = parseYamlScalar(valueMatch[1]);
        } else if (!/^(?:value|valueFrom|secretKeyRef|key)\s*:/i.test(line) && !line.startsWith('#')) {
          // Jika user langsung paste list text biasa seperti di gambar
          const clean = normalizeKey(line.replace(/^[-\s]+/, '').replace(/["']/g, ''));
          if (clean && !clean.includes(':')) {
            currentEntry = { name: clean, value: '' };
            entries.push(currentEntry);
          }
        }
      }

      return entries;
    }

    function encodeBase64(value) {
      const bytes = new TextEncoder().encode(value);
      let binary = '';
      for (const byte of bytes) {
        binary += String.fromCharCode(byte);
      }
      return btoa(binary);
    }

    function formatYamlScalar(value) {
      return /^[A-Za-z0-9._-]+$/.test(value) ? value : JSON.stringify(value);
    }

    function generateSecretYaml(entries, secret, namespace) {
      const data = entries.map(entry => {
        const encoded = encodeBase64(entry.value);
        return `  ${entry.name}: ${encoded}`;
      });

      const managedDataFields = entries.map(entry => {
        return `          'f:${entry.name}': {}`;
      });

      return [
        'kind: Secret',
        'apiVersion: v1',
        'metadata:',
        `  name: ${formatYamlScalar(secret)}`,
        namespace
          ? `  namespace: ${formatYamlScalar(namespace)}`
          : '  namespace:',
        '  uid:',
        "  resourceVersion: '389295843'",
        "  creationTimestamp: '2026-09-05T17:26:12Z'",
        '  managedFields:',
        '    - manager: Mozilla',
        '      operation: Update',
        '      apiVersion: v1',
        "      time: '2026-09-05T17:35:01Z'",
        '      fieldsType: FieldsV1',
        '      fieldsV1:',
        "        'f:data':",
        '          .: {}',
        ...managedDataFields,
        "        'f:type': {}",
        'data:',
        ...data,
        'type: Opaque',
      ].join('\n');
    }

    function generateInjectSecretYaml(entries) {
      const stringData = entries.map(entry => {
        return `  ${entry.name}: ${JSON.stringify(entry.value)}`;
      });

      return [
        'apiVersion: v1',
        'kind: Secret',
        'metadata:',
        '  name: apps-data',
        '  namespace:',
        'type: Opaque',
        'stringData:',
        ...stringData,
      ].join('\n');
    }

    function processText() {
      const text = rawInput.value;
      const secret = secretName.value.trim() || 'apps-data';
      const namespace = namespaceInput.value.trim();
      const entries = extractEntries(text);
      const keys = entries.map(entry => entry.name);

      // 1. Update Box 2 (List Key persis seperti gambar)
      extractedKeys.value = keys.join('\n');
      keyCount.innerText = keys.length + ' keys';

      // 2. Update Box 3 (Format Final YAML)
      if (keys.length === 0) {
        yamlOutput.value = '';
        secretYamlOutput.value = '';
        injectSecretOutput.value = '';
        return;
      }

      const generated = keys.map(k => {
        return `  - name: ${k}\n    valueFrom:\n      secretKeyRef:\n        name: ${secret}\n        key: ${k}`;
      }).join('\n');

      yamlOutput.value = generated;
      secretYamlOutput.value = generateSecretYaml(entries, secret, namespace);
      injectSecretOutput.value = generateInjectSecretYaml(entries);
    }

    rawInput.addEventListener('input', processText);
    secretName.addEventListener('input', processText);
    namespaceInput.addEventListener('input', processText);

    function copyText(elementId) {
      const el = document.getElementById(elementId);
      if (!el.value) return;
      
      navigator.clipboard.writeText(el.value).then(() => {
        showToast();
      });
    }

    function downloadSecretYaml() {
      if (!injectSecretOutput.value) return;

      const blob = new Blob([injectSecretOutput.value + '\n'], {
        type: 'application/yaml;charset=utf-8',
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'secret.yaml';
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    }

    function showToast() {
      const toast = document.getElementById('toast');
      toast.style.display = 'flex';
      setTimeout(() => {
        toast.style.display = 'none';
      }, 2000);
    }

    function clearInput() {
      rawInput.value = '';
      processText();
    }

    // Initial run
    processText();
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE
