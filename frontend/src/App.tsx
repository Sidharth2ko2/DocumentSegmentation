import { useState, useRef, useEffect } from 'react';
import { uploadDocs, getHistory, type ClassificationResult } from './api';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [batchResults, setBatchResults] = useState<ClassificationResult[]>([]);
  const [history, setHistory] = useState<ClassificationResult[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history", err);
    }
  };

  const handleUpload = async (files: FileList) => {
    if (files.length === 0) return;
    setLoading(true);
    setBatchResults([]); 
    
    try {
      const data = await uploadDocs(files);
      setBatchResults(data);
      await loadHistory(); 
    } catch (err) {
      alert("Error uploading files. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <header className="text-center mb-10">
          <h1 className="text-4xl font-black text-gray-900 tracking-tight">DocSegment AI</h1>
          <p className="text-gray-500 mt-2">Batch classify up to 10 documents at once</p>
        </header>

        {/* Upload Section */}
        <div 
          onClick={() => fileInputRef.current?.click()}
          className={`border-4 border-dashed rounded-3xl p-12 text-center transition-all cursor-pointer bg-white
            ${loading ? 'border-blue-300 bg-blue-50' : 'border-gray-200 hover:border-black'}`}
        >
          <input 
            type="file" 
            className="hidden" 
            ref={fileInputRef} 
            multiple 
            accept=".pdf,.txt"
            onChange={(e) => e.target.files && handleUpload(e.target.files)}
          />
          <div className="flex flex-col items-center">
            <span className="text-5xl mb-4">{loading ? "⚙️" : "📂"}</span>
            <h3 className="text-xl font-bold text-gray-800">
              {loading ? "Analyzing Documents..." : "Click to select PDFs"}
            </h3>
            <p className="text-gray-400 mt-2 text-sm">Shift-click to select multiple files</p>
          </div>
        </div>

        {/* Current Batch Results */}
        {batchResults.length > 0 && (
          <section className="mt-12">
            <h2 className="text-xs font-bold text-blue-600 uppercase tracking-widest mb-4">Latest Batch Results</h2>
            <div className="grid gap-4 sm:grid-cols-2">
              {batchResults.map((res, i) => (
                <div key={i} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition-shadow">
                  <div className="mb-4">
                    <p className="text-[10px] font-bold text-gray-400 truncate mb-1">{res.name}</p>
                    <p className="text-lg font-black text-gray-900">{res.label.replace('_', ' ')}</p>
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs font-bold text-gray-500">Confidence</span>
                      <span className={`text-xs font-mono font-bold ${res.confidence > 0.8 ? 'text-green-600' : 'text-blue-600'}`}>
                        {(res.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    {/* The New Dynamic Glow Bar */}
                    <div className="w-full bg-gray-100 h-2.5 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-1000 ease-out ${
                          res.confidence > 0.8 
                            ? 'bg-green-500 shadow-[0_0_10px_#22c55e]' 
                            : 'bg-blue-600'
                        }`} 
                        style={{ width: `${res.confidence * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* History Table */}
        <section className="mt-16">
          <h2 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Upload History</h2>
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 text-gray-400 text-[10px] uppercase font-bold">
                  <th className="px-6 py-4">Document Name</th>
                  <th className="px-6 py-4">Classification</th>
                  <th className="px-6 py-4 text-right">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {history.length > 0 ? history.map((doc, i) => (
                  <tr key={i} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm font-medium text-gray-700 truncate max-w-[200px]">{doc.name}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-block px-2 py-1 rounded-md text-xs font-bold ${
                        doc.confidence > 0.8 ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {doc.label}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono text-gray-400">
                      {(doc.confidence * 100).toFixed(1)}%
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan={3} className="px-6 py-8 text-center text-gray-400 text-sm">No documents found in history</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </div>
  );
}