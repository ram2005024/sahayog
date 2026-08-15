import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL,
  withCredentials: true,
});

// Request interceptor
api.interceptors.request.use((config) => {
  // Find there is incident idempotancy key or not
  let incidentIdempotancyKey = localStorage.getItem("incident_idempotancy_key");
  if (!incidentIdempotancyKey) {
    incidentIdempotancyKey = crypto.randomUUID();
    localStorage.setItem("incident_idempotancy_key", incidentIdempotancyKey);
  }
  //   if (token) {
  //     config.headers.Authorization = `Bearer token`;
  //   }
  //   -----------For Incident Idempotancy Key------------
  config.headers.incident_idempotancy_key = incidentIdempotancyKey;
  return config;
});

export default api;
