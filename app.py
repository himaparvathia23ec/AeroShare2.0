from flask import Flask, request, jsonify, send_from_directory, Response
import os, random, string

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# store {code: filename}
share_codes = {}

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AeroShare 2.0 Dashboard</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
<script>
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: { primary: "#51b7fb", background: "#0f1b23" },
      fontFamily: { display: "Space Grotesk" },
    },
  },
};
</script>
<style>
.glow-border::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 1rem;
  border: 2px solid transparent;
  background: linear-gradient(120deg,#00F6FF,#7A00FF) border-box;
  -webkit-mask: linear-gradient(#fff 0 0) padding-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite: destination-out;
  mask-composite: exclude;
  opacity: .7;
  transition: .3s;
}
.glow-border:hover::before {
  opacity: 1;
  box-shadow: 0 0 15px #00F6FF,0 0 25px #7A00FF;
}
</style>
</head>

<body class="bg-[#110E1F] font-display text-[#E6F1FF]">
<div class="flex flex-col min-h-screen w-full">
<header class="py-10 text-center">
  <h1 class="text-5xl font-bold text-white">AeroShare 2.0</h1>
  <p class="text-lg text-[#E6F1FF]/80">Share Smarter. Anywhere.</p>
</header>

<main class="flex-grow container mx-auto px-4 py-6">
  <div class="max-w-4xl mx-auto flex flex-col gap-8">

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div onclick="sendFile()" class="glow-border relative rounded-lg bg-[#182935]/60 backdrop-blur-md p-6 text-center cursor-pointer">
        <span class="material-symbols-outlined text-5xl text-primary">upload_file</span>
        <h2 class="text-2xl font-bold">Send File</h2>
        <p class="text-[#E6F1FF]/70">Select a file from your device.</p>
      </div>

      <div onclick="receiveFile()" class="glow-border relative rounded-lg bg-[#182935]/60 backdrop-blur-md p-6 text-center cursor-pointer">
        <span class="material-symbols-outlined text-5xl text-primary">download</span>
        <h2 class="text-2xl font-bold">Receive File</h2>
        <p class="text-[#E6F1FF]/70">Enter share code to receive file.</p>
      </div>
    </div>

    <div class="flex flex-col items-center gap-6 rounded-lg border-2 border-dashed border-[#2f526a] px-6 py-14 bg-[#182935]/30">
      <p class="text-lg font-bold">Drag & Drop your file here</p>
      <p class="text-sm text-[#E6F1FF]/70">or click below</p>
      <button onclick="sendFile()" class="rounded-full px-5 h-10 bg-primary text-[#101b23] font-bold hover:opacity-90">Browse Files</button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="rounded-lg p-6 bg-[#182935]/60 backdrop-blur-md">
        <p class="text-lg font-bold">Your Unique Share Code</p>
        <div class="flex justify-between items-center gap-4 mt-2">
          <p id="shareCode" class="text-[#64FFDA] text-2xl font-bold">---</p>
          <button onclick="copyCode()" class="rounded-full px-4 h-9 bg-primary text-[#101b23] text-sm font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-sm">content_copy</span>Copy
          </button>
        </div>
      </div>

      <div class="rounded-lg p-6 bg-[#182935]/60 backdrop-blur-md">
        <p class="text-lg font-bold">Connection Status</p>
        <div class="flex justify-between mt-2">
          <p>Transfer in Progress...</p>
          <p id="progressPercent" class="text-[#64FFDA]">0%</p>
        </div>
        <div class="w-full rounded bg-[#2f526a] mt-2">
          <div id="progressBar" class="h-2 rounded bg-primary" style="width:0%"></div>
        </div>
        <p id="peerStatus" class="text-sm text-[#8eb4cc] mt-2">Waiting for connection...</p>
      </div>
    </div>
  </div>
</main>

<footer class="mt-16 py-8 text-center border-t border-white/10 text-sm text-[#E6F1FF]/60">
  © 2025 AeroShare | AI-Powered File Transfer
</footer>
</div>

<script>
function sendFile() {
  const input = document.createElement('input');
  input.type = 'file';
  input.onchange = e => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    fetch('/upload', { method: 'POST', body: formData })
      .then(res => res.json())
      .then(data => {
        document.getElementById('shareCode').textContent = data.code;
        alert('File uploaded! Share code: ' + data.code);
        simulateProgress();
      })
      .catch(err => alert('Error: ' + err));
  };
  input.click();
}

function receiveFile() {
  const code = prompt("Enter the sender's share code:");
  if (!code) return;
  fetch('/receive', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  })
  .then(res => res.json())
  .then(data => {
    if (data.download_url) {
      alert('Starting download for: ' + data.filename);
      window.location.href = data.download_url;
      simulateProgress();
    } else {
      alert(data.message);
    }
  })
  .catch(err => alert('Error: ' + err));
}

function copyCode() {
  const code = document.getElementById('shareCode').textContent;
  if (code !== '---') {
    navigator.clipboard.writeText(code);
    alert('Copied: ' + code);
  } else {
    alert('No code to copy yet.');
  }
}

function simulateProgress() {
  let p = 0;
  const bar = document.getElementById('progressBar');
  const percent = document.getElementById('progressPercent');
  const peer = document.getElementById('peerStatus');
  peer.textContent = "Connected to Peer_Name";
  const interval = setInterval(() => {
    p += 5;
    bar.style.width = p + "%";
    percent.textContent = p + "%";
    if (p >= 100) {
      clearInterval(interval);
      peer.textContent = "Transfer Complete ✅";
    }
  }, 200);
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return Response(HTML_CONTENT, mimetype='text/html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file found'}), 400
    file = request.files['file']
    if not file.filename:
        return jsonify({'message': 'No filename'}), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    share_codes[code] = file.filename
    return jsonify({'message': 'Uploaded successfully', 'code': code})

@app.route('/receive', methods=['POST'])
def receive_file():
    data = request.get_json()
    code = data.get('code', '')
    if code in share_codes:
        filename = share_codes[code]
        download_url = f"/download/{code}"
        return jsonify({'message': 'Ready to download', 'filename': filename, 'download_url': download_url})
    return jsonify({'message': 'Invalid code. Please check again.'})

@app.route('/download/<code>')
def download(code):
    if code in share_codes:
        filename = share_codes[code]
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return "Invalid code", 404

if __name__ == '__main__':
    app.run(debug=True)
