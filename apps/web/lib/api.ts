export type Template = {
  id: string;
  name: string;
  description: string;
  category: string;
  textureWidth: number;
  textureHeight: number;
};

export type Job = {
  id: string;
  templateId: string;
  status: "queued" | "processing" | "completed" | "failed";
  sourceFilename: string;
  outputPackage: string | null;
  error: string | null;
  createdAt: string;
  updatedAt: string;
};

const API = "";

export async function fetchTemplates(): Promise<Template[]> {
  const res = await fetch(`${API}/api/templates`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load templates");
  const data = await res.json();
  return data.templates;
}

export async function fetchEntitlements(): Promise<{
  credits: number;
  canCreate: boolean;
}> {
  const res = await fetch(`${API}/api/entitlements`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load entitlements");
  return res.json();
}

export async function fetchJobs(): Promise<Job[]> {
  const res = await fetch(`${API}/api/jobs`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load jobs");
  const data = await res.json();
  return data.jobs;
}

export async function fetchJob(id: string): Promise<Job> {
  const res = await fetch(`${API}/api/jobs/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Job not found");
  return res.json();
}

export async function createJob(templateId: string, file: File): Promise<Job> {
  const form = new FormData();
  form.append("templateId", templateId);
  form.append("image", file);
  const res = await fetch(`${API}/api/jobs`, { method: "POST", body: form });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Failed to create job");
  }
  return res.json();
}

export function downloadUrl(jobId: string): string {
  return `${API}/api/jobs/${jobId}/download`;
}

export function installGuideUrl(jobId: string): string {
  return `${API}/api/jobs/${jobId}/install-guide`;
}
