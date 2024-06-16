import {API_URL} from "./consts";
import axios from "axios";
import data from "bootstrap/js/src/dom/data.js";


const instance = axios.create({
    baseURL: API_URL,
});

instance.defaults.headers.post['Content-Type'] = 'application/json';

export async function apiSearchVideoByQuery(query) {
    const response = await instance.get(`/search?text=${query}`).catch(apiErrorHandler)
    console.log(response.data, response.status)

    return response;
}

export async function apiSearchPopularVideo() {
    const response = await instance.get('/search?text=hot girls',).catch(apiErrorHandler)

    return response;
}

export async function apiUploadVideo(description, link) {
    const response = await instance.post('/upload', {
        description: description,
        link: link
    }).catch(apiErrorHandler)

    return response;
}

function apiErrorHandler(error) {
    if (error.response) {
        console.error(error.response);
        let err = new Error(error.response.data.detail || "Unknown error");
        err.statusCode = error.response.status;
        err.data = error.response.data;
        throw err;
    } else {
        console.error('Unknown error: ', error.message);
        throw new Error("Unknown error, please try again");
    }
}