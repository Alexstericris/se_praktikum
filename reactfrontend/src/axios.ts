import axios from "axios";

const token = localStorage.getItem('accessKey');
export default axios.create({
    baseURL: "http://49.12.242.25/api/",
    timeout: 1000,
    headers:{
        'Authorization':`Bearer ${token}`
    }
});