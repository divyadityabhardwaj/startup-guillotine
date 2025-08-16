import { ValidationResult } from "@/types";

const API_BASE_URL = "/api/v1";

export class APIError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "APIError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      detail: "An unknown error occurred",
    }));
    throw new APIError(errorData.detail || "An unknown error occurred");
  }
  return response.json();
}

export const api = {
  validateStartupIdea: async (idea: string): Promise<ValidationResult> => {
    const response = await fetch(`${API_BASE_URL}/validate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idea: idea }),
    });
    return handleResponse<ValidationResult>(response);
  },

  validateFile: async (file: File): Promise<ValidationResult> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/validate-file`, {
      method: "POST",
      body: formData,
    });
    return handleResponse<ValidationResult>(response);
  },
};
