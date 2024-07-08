import axios from 'axios'

const baseURL = "http://localhost:8000/"; // Development base URL

export const defaultAxiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  }
});

