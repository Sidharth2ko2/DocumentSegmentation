const BASE = "http://127.0.0.1:8001";

export interface ClassificationResult {
  name: string;
  label: string;
  confidence: number;
}

export const uploadDocs = async (files: FileList): Promise<ClassificationResult[]> => {
  const formData = new FormData();
  
  // Convert FileList to Array and append each to the 'files' key
  Array.from(files).forEach((file) => {
    formData.append('files', file); 
  });

  const response = await fetch(`${BASE}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    console.error("Server Error:", errorData);
    throw new Error('Upload failed');
  }

  return response.json();
};

export const getHistory = async (): Promise<ClassificationResult[]> => {
  const response = await fetch(`${BASE}/history`);
  if (!response.ok) return [];
  return response.json();
};