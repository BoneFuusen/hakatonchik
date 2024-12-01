import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Адрес FastAPI
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getRecommendation = async (clientData) => {
  const response = await apiClient.post('/recommendation/', clientData);
  return response.data;
};
