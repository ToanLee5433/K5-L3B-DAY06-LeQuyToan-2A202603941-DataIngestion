"""Lightweight Web UI Dashboard to test and compare Day 06 Data Ingestion strategies."""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv

# Path setup
current_dir = Path(__file__).resolve().parent
candidate = current_dir
while candidate != candidate.parent:
    if (candidate / "STUDENT.md").exists() or (candidate / "BENCHMARK.md").exists():
        root_dir = candidate
        break
    candidate = candidate.parent
else:
    root_dir = current_dir.parent

sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "starter"))
sys.path.insert(0, str(root_dir / "src"))

env_paths = [root_dir / "starter" / ".env", root_dir / ".env"]
for ep in env_paths:
    if ep.exists():
        load_dotenv(ep)
        break

from starter.src.embeddings import GeminiEmbedder
from starter.src.store import PgVectorStore

# Global services
db_url = os.getenv("DATABASE_URL", "postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab")
api_key = os.getenv("GEMINI_API_KEY")

embedder = None
store = None
if api_key:
    embedder = GeminiEmbedder(api_key=api_key, model_name="models/gemini-embedding-2", dimensions=768)
    store = PgVectorStore(database_url=db_url, dimensions=768)

# Load benchmark questions and summary metrics
questions_path = root_dir / "benchmark" / "questions.json"
summary_path = root_dir / "results" / "summary_metrics.json"

benchmark_questions = []
if questions_path.exists():
    with open(questions_path, "r", encoding="utf-8") as f:
        benchmark_questions = json.load(f)

summary_metrics = {}
if summary_path.exists():
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_metrics = json.load(f)

HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Day 06: Data Ingestion & Retrieval Playground</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    .score-badge { background: linear-gradient(135deg, #4f46e5, #06b6d4); }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-lg shadow-lg shadow-indigo-500/30">
          <i class="fa-solid fa-database"></i>
        </div>
        <div>
          <h1 class="text-lg font-bold text-white flex items-center gap-2">
            Data Ingestion Engineering Playground
            <span class="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Day 06</span>
          </h1>
          <p class="text-xs text-slate-400">Model: <span class="text-cyan-400 font-semibold">Gemini Embedding 2</span> (768d) | DB: PostgreSQL 16 + pgvector</p>
        </div>
      </div>
      <div class="text-right text-xs text-slate-400">
        <p class="font-medium text-slate-300">Lê Quý Toàn · 2A202603941</p>
        <p>Lớp L3B · Handbook VinUni 2025-2026</p>
      </div>
    </div>
  </header>

  <!-- Navigation Tabs -->
  <div class="max-w-7xl mx-auto px-4 pt-4">
    <div class="flex border-b border-slate-800 space-x-4">
      <button onclick="switchTab('search')" id="tab-btn-search" class="px-4 py-2 text-sm font-semibold border-b-2 border-indigo-500 text-indigo-400 flex items-center gap-2">
        <i class="fa-solid fa-magnifying-glass"></i> Tra cứu tương tác
      </button>
      <button onclick="switchTab('benchmark')" id="tab-btn-benchmark" class="px-4 py-2 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2">
        <i class="fa-solid fa-list-check"></i> 20 Câu Benchmark & Gold
      </button>
      <button onclick="switchTab('metrics')" id="tab-btn-metrics" class="px-4 py-2 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2">
        <i class="fa-solid fa-chart-column"></i> So sánh 3 Chiến lược (A/B/C)
      </button>
    </div>
  </div>

  <main class="max-w-7xl mx-auto px-4 py-6">
    <!-- TAB 1: SEARCH PLAYGROUND -->
    <section id="tab-search" class="space-y-6">
      <!-- Search Controls Card -->
      <div class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <!-- Strategy Selector -->
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Chiến lược dữ liệu</label>
            <select id="strategy" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500">
              <option value="c" selected>Strategy C: Paragraph + Metadata Filter (Tốt nhất)</option>
              <option value="b">Strategy B: Paragraph (Max 1000 chars, no filter)</option>
              <option value="a">Strategy A: Fixed-size (500 chars, overlap 50)</option>
            </select>
          </div>

          <!-- Section Filter -->
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Metadata Filter (section)</label>
            <select id="section-filter" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500">
              <option value="">(Tất cả / Không lọc)</option>
              <option value="admissions">admissions (Tuyển sinh)</option>
              <option value="course_registration">course_registration (Đăng ký môn học)</option>
              <option value="attendance_leave">attendance_leave (Chuyên cần & Nghỉ học)</option>
              <option value="grading_gpa">grading_gpa (Thang điểm & GPA)</option>
              <option value="academic_standing">academic_standing (Cảnh báo học thuật)</option>
              <option value="academic_integrity">academic_integrity (Liêm chính học thuật)</option>
              <option value="graduation_honors">graduation_honors (Tốt nghiệp & Danh hiệu)</option>
              <option value="tuition_scholarships">tuition_scholarships (Học phí & Học bổng)</option>
            </select>
          </div>

          <!-- Top-K Selector -->
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Top-K kết quả</label>
            <select id="top-k" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500">
              <option value="1">Top 1</option>
              <option value="3" selected>Top 3 (Chuẩn benchmark)</option>
              <option value="5">Top 5</option>
            </select>
          </div>
        </div>

        <!-- Query Input -->
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Câu hỏi hoặc truy vấn</label>
          <div class="flex gap-2">
            <input type="text" id="query-input" placeholder="Ví dụ: Điểm IELTS tối thiểu để được tuyển thẳng không điều kiện là bao nhiêu?..." 
                   class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 shadow-inner"
                   onkeydown="if(event.key === 'Enter') doSearch()">
            <button onclick="doSearch()" id="search-btn" class="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3 rounded-xl transition flex items-center gap-2 shadow-lg shadow-indigo-600/30">
              <i class="fa-solid fa-magnifying-glass"></i> Tìm kiếm
            </button>
          </div>
        </div>

        <!-- Quick Sample Queries -->
        <div class="mt-4 pt-4 border-t border-slate-700/60 flex flex-wrap items-center gap-2 text-xs">
          <span class="text-slate-400 font-semibold"><i class="fa-solid fa-lightbulb text-amber-400 mr-1"></i>Câu hỏi mẫu:</span>
          <button onclick="setSample('Điểm IELTS tối thiểu để được xét tuyển thẳng không điều kiện là bao nhiêu?', 'admissions', 'c')" class="bg-slate-700/60 hover:bg-slate-700 px-3 py-1 rounded-lg text-slate-300">
            q01: IELTS Tuyển thẳng
          </button>
          <button onclick="setSample('Vắng bao nhiêu phần trăm số tiết học sẽ bị cảnh báo chuyên cần chính thức?', 'attendance_leave', 'c')" class="bg-slate-700/60 hover:bg-slate-700 px-3 py-1 rounded-lg text-slate-300">
            q05: Cảnh báo chuyên cần
          </button>
          <button onclick="setSample('Hành vi sử dụng công cụ AI tạo sinh nộp bài mà không khai báo bị xếp vào mức vi phạm nào?', 'academic_integrity', 'c')" class="bg-slate-700/60 hover:bg-slate-700 px-3 py-1 rounded-lg text-slate-300">
            q16: Vi phạm AI (Test)
          </button>
          <button onclick="setSample('Sinh viên nhận học bổng tài năng 70% và 50% phải duy trì điểm GPA tích lũy tối thiểu là bao nhiêu?', 'tuition_scholarships', 'c')" class="bg-slate-700/60 hover:bg-slate-700 px-3 py-1 rounded-lg text-slate-300">
            q19: Duy trì học bổng (Test)
          </button>
          <button onclick="setSample('Chính sách hoàn học phí khi sinh viên chính thức rút học trong tuần thứ 3 đến tuần thứ 4 là bao nhiêu?', 'tuition_scholarships', 'c')" class="bg-slate-700/60 hover:bg-slate-700 px-3 py-1 rounded-lg text-slate-300">
            q20: Hoàn học phí (Test)
          </button>
        </div>
      </div>

      <!-- Search Results Container -->
      <div id="results-area" class="space-y-4">
        <div class="text-center py-12 text-slate-500">
          <i class="fa-solid fa-compass text-4xl mb-3 text-slate-600"></i>
          <p>Nhập câu hỏi hoặc bấm vào câu hỏi mẫu phía trên để tra cứu bằng pgvector.</p>
        </div>
      </div>
    </section>

    <!-- TAB 2: BENCHMARK QUESTIONS EXPLORER -->
    <section id="tab-benchmark" class="hidden space-y-4">
      <div class="flex items-center justify-between mb-2">
        <div>
          <h2 class="text-base font-bold text-white">Danh sách 20 câu hỏi Benchmark (15 Dev / 5 Test)</h2>
          <p class="text-xs text-slate-400">Mỗi câu hỏi đều có Gold Source, Gold Page và trích dẫn bằng chứng (Evidence Quote) đã kiểm chứng.</p>
        </div>
        <div class="text-xs text-slate-400">
          <span class="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">15 Dev</span>
          <span class="px-2.5 py-1 rounded-lg bg-blue-500/20 text-blue-300 border border-blue-500/30 ml-2">5 Test</span>
        </div>
      </div>
      <div id="benchmark-list" class="space-y-3">
        <!-- Rendered via JS -->
      </div>
    </section>

    <!-- TAB 3: METRICS COMPARISON -->
    <section id="tab-metrics" class="hidden space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Strategy A Card -->
        <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-xl">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="font-bold text-lg text-rose-400">Strategy A</h3>
              <p class="text-xs text-slate-400">Fixed-size (500 chars, overlap 50)</p>
            </div>
            <span class="px-2.5 py-1 text-xs rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-semibold">98 Chunks</span>
          </div>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Overall Hit@1:</span>
              <span class="font-bold text-white">9/20 (45.0%)</span>
            </div>
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Evidence Hit@3:</span>
              <span class="font-bold text-white">16/20 (80.0%)</span>
            </div>
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Chunk Coherence:</span>
              <span class="font-bold text-amber-400">0.70 / 2.0</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Grounding Test:</span>
              <span class="font-bold text-amber-400">1.40 / 2.0</span>
            </div>
          </div>
        </div>

        <!-- Strategy B Card -->
        <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-xl">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="font-bold text-lg text-cyan-400">Strategy B</h3>
              <p class="text-xs text-slate-400">Paragraph-aware (Max 1000 chars)</p>
            </div>
            <span class="px-2.5 py-1 text-xs rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-semibold">33 Chunks</span>
          </div>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Overall Hit@1:</span>
              <span class="font-bold text-emerald-400">19/20 (95.0%)</span>
            </div>
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Evidence Hit@3:</span>
              <span class="font-bold text-emerald-400">20/20 (100.0%)</span>
            </div>
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Chunk Coherence:</span>
              <span class="font-bold text-emerald-400">2.00 / 2.0</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Grounding Test:</span>
              <span class="font-bold text-emerald-400">2.00 / 2.0</span>
            </div>
          </div>
        </div>

        <!-- Strategy C Card -->
        <div class="bg-slate-800/80 border border-indigo-500/50 rounded-2xl p-6 shadow-xl ring-2 ring-indigo-500/20">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="font-bold text-lg text-indigo-400 flex items-center gap-1.5">
                Strategy C <i class="fa-solid fa-crown text-amber-400 text-xs"></i>
              </h3>
              <p class="text-xs text-slate-400">Paragraph + Metadata Filter</p>
            </div>
            <span class="px-2.5 py-1 text-xs rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold">33 Chunks</span>
          </div>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Overall Hit@1:</span>
              <span class="font-bold text-emerald-400">19/20 (95.0%)</span>
            </div>
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Evidence Hit@3:</span>
              <span class="font-bold text-emerald-400">20/20 (100.0%)</span>
            </div>
            <div class="flex justify-between border-b border-slate-700/60 pb-2">
              <span class="text-slate-400">Filter Tuân thủ:</span>
              <span class="font-bold text-emerald-400">3/3 (100.0%)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Grounding Test:</span>
              <span class="font-bold text-emerald-400">2.00 / 2.0</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <script>
    const questions = %QUESTIONS_JSON%;

    function switchTab(tab) {
      document.getElementById('tab-search').classList.add('hidden');
      document.getElementById('tab-benchmark').classList.add('hidden');
      document.getElementById('tab-metrics').classList.add('hidden');

      document.getElementById('tab-btn-search').className = "px-4 py-2 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2";
      document.getElementById('tab-btn-benchmark').className = "px-4 py-2 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2";
      document.getElementById('tab-btn-metrics').className = "px-4 py-2 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2";

      document.getElementById('tab-' + tab).classList.remove('hidden');
      document.getElementById('tab-btn-' + tab).className = "px-4 py-2 text-sm font-semibold border-b-2 border-indigo-500 text-indigo-400 flex items-center gap-2";
    }

    function setSample(q, sec, strat) {
      document.getElementById('query-input').value = q;
      document.getElementById('section-filter').value = sec || '';
      document.getElementById('strategy').value = strat || 'c';
      doSearch();
    }

    async function doSearch() {
      const q = document.getElementById('query-input').value.trim();
      if (!q) return;

      const strat = document.getElementById('strategy').value;
      const sec = document.getElementById('section-filter').value;
      const topK = document.getElementById('top-k').value;
      const btn = document.getElementById('search-btn');
      const resultsArea = document.getElementById('results-area');

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang tìm...';
      resultsArea.innerHTML = '<div class="text-center py-8 text-slate-400"><i class="fa-solid fa-spinner fa-spin text-2xl mb-2"></i><p>Đang embedding câu hỏi và truy vấn pgvector...</p></div>';

      try {
        const resp = await fetch(`/api/search?q=${encodeURIComponent(q)}&strategy=${strat}&section=${encodeURIComponent(sec)}&top_k=${topK}`);
        const data = await resp.json();

        if (data.error) {
          resultsArea.innerHTML = `<div class="p-4 bg-rose-500/20 border border-rose-500/30 text-rose-300 rounded-xl">Lỗi: ${data.error}</div>`;
          return;
        }

        if (!data.hits || data.hits.length === 0) {
          resultsArea.innerHTML = '<div class="text-center py-8 text-slate-400">Không tìm thấy kết quả phù hợp.</div>';
          return;
        }

        let html = `<div class="flex items-center justify-between text-xs text-slate-400 mb-2">
          <span>Tìm thấy <b>${data.hits.length}</b> kết quả (Chiến lược: <b>${strat.toUpperCase()}</b>${sec ? ` | Filter: <b>${sec}</b>` : ''})</span>
          <span>Thời gian phản hồi: <b>${data.elapsed_ms}ms</b></span>
        </div>`;

        data.hits.forEach((hit, idx) => {
          const score = (hit.score * 100).toFixed(1);
          const meta = hit.metadata || {};
          html += `
            <div class="bg-slate-800/90 border border-slate-700/80 rounded-2xl p-5 shadow-lg space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="px-2.5 py-1 text-xs font-bold rounded-lg bg-indigo-600/30 text-indigo-300 border border-indigo-500/30">Top ${idx + 1}</span>
                  <span class="px-2 py-0.5 text-xs rounded-md bg-slate-700 text-slate-300">Trang ${hit.page}</span>
                  <span class="px-2 py-0.5 text-xs rounded-md bg-cyan-950 text-cyan-300 border border-cyan-800">${meta.section || 'N/A'}</span>
                  <span class="text-xs text-slate-500 font-mono">${hit.chunk_id}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-400">Cosine Score:</span>
                  <span class="px-2.5 py-1 rounded-full text-xs font-bold score-badge text-white shadow">${(hit.score).toFixed(4)} (${score}%)</span>
                </div>
              </div>
              <div class="text-sm text-slate-200 leading-relaxed bg-slate-900/60 p-4 rounded-xl border border-slate-800 whitespace-pre-wrap font-sans">
                ${hit.text}
              </div>
            </div>
          `;
        });

        resultsArea.innerHTML = html;
      } catch (err) {
        resultsArea.innerHTML = `<div class="p-4 bg-rose-500/20 border border-rose-500/30 text-rose-300 rounded-xl">Lỗi kết nối: ${err.message}</div>`;
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> Tìm kiếm';
      }
    }

    // Render Benchmark List
    function renderBenchmark() {
      const container = document.getElementById('benchmark-list');
      if (!questions || questions.length === 0) return;

      container.innerHTML = questions.map(q => {
        const isTest = q.split === 'test';
        const badgeClass = isTest ? 'bg-blue-500/20 text-blue-300 border-blue-500/30' : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
        const filterStr = q.filter ? JSON.stringify(q.filter) : 'None';
        const secVal = q.filter ? q.filter.section : '';

        return `
          <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3 hover:border-slate-600 transition">
            <div class="space-y-1 flex-1">
              <div class="flex items-center gap-2 text-xs">
                <span class="font-mono font-bold text-slate-300">${q.id.toUpperCase()}</span>
                <span class="px-2 py-0.5 rounded-full text-xs font-semibold border ${badgeClass}">${q.split.toUpperCase()}</span>
                <span class="text-slate-400">Trang nguồn: <b>${q.gold_page}</b></span>
                <span class="text-slate-400">Filter: <code class="text-amber-300">${filterStr}</code></span>
              </div>
              <p class="text-sm font-semibold text-white">${q.question}</p>
              <p class="text-xs text-slate-400 italic">Đáp án mong đợi: ${q.expected_answer}</p>
              <div class="text-xs text-slate-300 bg-slate-900/50 p-2 rounded border border-slate-800/80 mt-1">
                <span class="text-emerald-400 font-semibold">Evidence:</span> "${q.evidence_quote}"
              </div>
            </div>
            <div>
              <button onclick="setSample('${q.question.replace(/'/g, "\\'")}', '${secVal}', 'c'); switchTab('search');" class="bg-indigo-600/80 hover:bg-indigo-600 text-white text-xs font-semibold px-4 py-2 rounded-xl transition flex items-center gap-1.5 whitespace-nowrap">
                <i class="fa-solid fa-play text-xs"></i> Test câu này
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    renderBenchmark();
  </script>
</body>
</html>"""


class UIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            rendered = HTML_PAGE.replace("%QUESTIONS_JSON%", json.dumps(benchmark_questions, ensure_ascii=False))
            self.wfile.write(rendered.encode("utf-8"))
            return

        if parsed.path == "/api/search":
            qs = parse_qs(parsed.query)
            q = qs.get("q", [""])[0]
            strategy = qs.get("strategy", ["c"])[0].lower()
            section = qs.get("section", [""])[0]
            top_k = int(qs.get("top_k", [3])[0])

            if not q or not embedder or not store:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing query or services not initialized"}).encode("utf-8"))
                return

            try:
                import time
                t0 = time.time()
                q_vec = embedder.embed_query(q)
                filters = {"section": section} if section else None
                strat_key = f"strategy_{strategy}"
                hits = store.search(strat_key, q_vec, top_k=top_k, filters=filters)
                elapsed_ms = round((time.time() - t0) * 1000, 1)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"hits": hits, "elapsed_ms": elapsed_ms}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        super().do_GET()


def run_server(port: int = 5500):
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, UIHandler)
    print(f"\n=======================================================")
    print(f"🚀 Day 06 Playground UI is running!")
    print(f"👉 Mở trình duyệt tại: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã tắt UI server.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
    run_server(port)
