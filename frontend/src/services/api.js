import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const sendChatMessage = async (message, sessionId = null) => {
  try {
    const response = await api.post("/api/chat", {
      message: message,
      session_id: sessionId,
    });

    return response.data;
  } catch (error) {
    console.error("Chat API Error:", error);

    throw (
      error.response?.data ||
      new Error("Unable to connect to the SchemeConnect AI server.")
    );
  }
};

// Get all government schemes
export const fetchSchemes = async () => {
  try {
    const response = await api.get("/api/schemes");
    return response.data;
  } catch (error) {
    console.error("Schemes API Error:", error);

    throw (
      error.response?.data ||
      new Error("Unable to fetch government schemes.")
    );
  }
};

export default api;