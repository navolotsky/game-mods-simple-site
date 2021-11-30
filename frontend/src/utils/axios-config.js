import axios from 'axios';

const { REACT_APP_BASE_API_URL } = process.env;

const defaultUrl = 'http://localhost:8000/';

const instance = axios.create({
    baseURL: REACT_APP_BASE_API_URL || defaultUrl
});

export default instance;
