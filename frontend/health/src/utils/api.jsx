import axios from "axios";

const API_BASE_URL = "http://34.204.43.102:5000";

export const uploadPDFs = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/upload_pdfs`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading PDFs:", error);
    throw (
      error.response?.data?.detail || error.message || "Failed to upload files."
    );
  }
};

export const askQuestion = async (sessionId, query) => {
  const payload = { session_id: sessionId, query: query };
  try {
    const response = await axios.post(`${API_BASE_URL}/ask_question`, payload);
    return response.data;
  } catch (error) {
    console.error("Error asking question:", error);
    throw (
      error.response?.data?.detail || error.message || "Failed to ask question."
    );
  }
};
