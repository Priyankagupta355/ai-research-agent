"use client";

import { useState } from "react";

interface Source {
  title?: string;
  url?: string;
}

interface ResearchReport {
  title?: string;
  summary?: string;
  key_findings?: string[];
  sources?: Source[];
  conclusion?: string;
}

const exampleQueries = [
  "What is Generative AI?",
  "How does RAG work?",
  "Future of Artificial Intelligence",
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [report, setReport] = useState<ResearchReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const runResearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setReport(null);

    try {
      const response = await fetch(
        "https://ai-research-agent-nyrc.onrender.com/research",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query.trim(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Research request failed");
      }

      const data: ResearchReport = await response.json();
      setReport(data);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to get research report. Please check the backend or try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const createReportText = () => {
    if (!report) return "";

    let text = "";

    text += `${report.title || "AI Research Report"}\n`;
    text += `${"=".repeat(60)}\n\n`;

    text += `SUMMARY\n`;
    text += `${report.summary || "No summary available."}\n\n`;

    text += `KEY FINDINGS\n`;
    if (report.key_findings && report.key_findings.length > 0) {
      report.key_findings.forEach((finding, index) => {
        text += `${index + 1}. ${finding}\n`;
      });
    } else {
      text += "No key findings available.\n";
    }

    text += `\nSOURCES\n`;
    if (report.sources && report.sources.length > 0) {
      report.sources.forEach((source, index) => {
        text += `${index + 1}. ${source.title || "Source"}\n`;
        if (source.url) {
          text += `   ${source.url}\n`;
        }
      });
    } else {
      text += "No sources available.\n";
    }

    text += `\nCONCLUSION\n`;
    text += `${report.conclusion || "No conclusion available."}\n`;

    return text;
  };

  const copyReport = async () => {
    const text = createReportText();

    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch (err) {
      console.error(err);
    }
  };

  const downloadReport = () => {
    const text = createReportText();

    if (!text) return;

    const blob = new Blob([text], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "ai-research-report.txt";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* NAVBAR */}
      <nav className="border-b border-slate-800 bg-slate-950/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              AI Research Agent
            </h1>

            <p className="text-xs text-slate-400">
              Intelligent Web Research Assistant
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400"></span>

            <span className="text-sm text-emerald-300">
              API Online
            </span>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="mx-auto max-w-6xl px-6 pb-10 pt-16 text-center">
        <div className="mx-auto max-w-3xl">
          <div className="mb-5 inline-flex rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm text-slate-300">
            AI-Powered Research
          </div>

          <h2 className="text-4xl font-bold leading-tight md:text-6xl">
            Research Smarter.
            <span className="block text-slate-400">
              Get Answers Faster.
            </span>
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Ask a research question and let the AI agent search the web,
            analyze information, and generate a structured research report.
          </p>
        </div>
      </section>

      {/* SEARCH */}
      <section className="mx-auto max-w-4xl px-6">
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-3 shadow-2xl">
          <div className="flex flex-col gap-3 md:flex-row">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  runResearch();
                }
              }}
              placeholder="Ask a research question..."
              className="flex-1 rounded-xl border border-slate-700 bg-slate-950 px-5 py-4 text-white outline-none placeholder:text-slate-500 focus:border-slate-500"
            />

            <button
              onClick={runResearch}
              disabled={loading || !query.trim()}
              className="rounded-xl bg-white px-7 py-4 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Researching..." : "Research"}
            </button>
          </div>
        </div>

        {/* EXAMPLES */}
        <div className="mt-4 flex flex-wrap justify-center gap-2">
          {exampleQueries.map((example) => (
            <button
              key={example}
              onClick={() => setQuery(example)}
              className="rounded-full border border-slate-800 bg-slate-900 px-4 py-2 text-sm text-slate-400 transition hover:border-slate-600 hover:text-white"
            >
              {example}
            </button>
          ))}
        </div>
      </section>

      {/* ERROR */}
      {error && (
        <section className="mx-auto mt-8 max-w-4xl px-6">
          <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-red-300">
            {error}
          </div>
        </section>
      )}

      {/* LOADING */}
      {loading && (
        <section className="mx-auto mt-12 max-w-4xl px-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center">
            <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-slate-600 border-t-white"></div>

            <h3 className="font-semibold">
              AI is researching...
            </h3>

            <p className="mt-2 text-sm text-slate-400">
              Searching sources and analyzing information.
            </p>
          </div>
        </section>
      )}

      {/* REPORT */}
      {report && !loading && (
        <section className="mx-auto max-w-5xl px-6 pb-16 pt-12">
          {/* REPORT HEADER */}
          <div className="mb-6 flex flex-col gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-6 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="mb-2 text-sm text-slate-500">
                Research Report
              </p>

              <h2 className="text-2xl font-bold">
                {report.title || "Research Report"}
              </h2>
            </div>

            {/* ACTION BUTTONS */}
            <div className="flex gap-2">
              <button
                onClick={copyReport}
                className="rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-slate-500 hover:text-white"
              >
                {copied ? "✓ Copied" : "Copy Report"}
              </button>

              <button
                onClick={downloadReport}
                className="rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-slate-500 hover:text-white"
              >
                ↓ Download
              </button>
            </div>
          </div>

          {/* SUMMARY */}
          <ReportCard title="Summary">
            <p className="leading-8 text-slate-300">
              {report.summary || "No summary available."}
            </p>
          </ReportCard>

          {/* KEY FINDINGS */}
          <ReportCard title="Key Findings">
            {report.key_findings &&
            report.key_findings.length > 0 ? (
              <div className="space-y-4">
                {report.key_findings.map((finding, index) => (
                  <div
                    key={index}
                    className="flex gap-4 rounded-xl border border-slate-800 bg-slate-950 p-4"
                  >
                    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-800 text-sm font-semibold">
                      {index + 1}
                    </div>

                    <p className="leading-7 text-slate-300">
                      {finding}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-400">
                No key findings available.
              </p>
            )}
          </ReportCard>

          {/* SOURCES */}
          <ReportCard title="Sources">
            {report.sources &&
            report.sources.length > 0 ? (
              <div className="grid gap-3">
                {report.sources.map((source, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-slate-800 bg-slate-950 p-4 transition hover:border-slate-600"
                  >
                    <div className="flex gap-3">
                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-800 text-sm">
                        {index + 1}
                      </div>

                      <div className="min-w-0">
                        <p className="font-medium text-white">
                          {source.title || "Research Source"}
                        </p>

                        {source.url && (
                          <a
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-1 block truncate text-sm text-slate-400 hover:text-white"
                          >
                            {source.url}
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-400">
                No sources available.
              </p>
            )}
          </ReportCard>

          {/* CONCLUSION */}
          <ReportCard title="Conclusion">
            <p className="leading-8 text-slate-300">
              {report.conclusion || "No conclusion available."}
            </p>
          </ReportCard>

          {/* NEW RESEARCH */}
          <div className="mt-8 text-center">
            <button
              onClick={() => {
                setReport(null);
                setQuery("");
                setError("");
                window.scrollTo({
                  top: 0,
                  behavior: "smooth",
                });
              }}
              className="rounded-xl bg-white px-6 py-3 font-semibold text-slate-950 transition hover:bg-slate-200"
            >
              + New Research
            </button>
          </div>
        </section>
      )}

      {/* FEATURES */}
      {!report && !loading && (
        <section className="mx-auto grid max-w-6xl gap-4 px-6 pb-16 pt-16 md:grid-cols-3">
          <FeatureCard
            title="Web Search"
            description="Searches the web to collect relevant information for your research question."
          />

          <FeatureCard
            title="AI Analysis"
            description="Uses an AI agent to analyze gathered information and build meaningful findings."
          />

          <FeatureCard
            title="Structured Report"
            description="Transforms research results into summary, findings, sources, and conclusion."
          />
        </section>
      )}

      {/* FOOTER */}
      <footer className="border-t border-slate-800 py-8 text-center text-sm text-slate-500">
        AI Research Agent • Built with Next.js, FastAPI & Groq
      </footer>
    </main>
  );
}

function FeatureCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 transition hover:border-slate-700">
      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-3 leading-7 text-slate-400">
        {description}
      </p>
    </div>
  );
}

function ReportCard({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="mb-5 rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="mb-5 text-lg font-semibold">
        {title}
      </h3>

      {children}
    </div>
  );
}