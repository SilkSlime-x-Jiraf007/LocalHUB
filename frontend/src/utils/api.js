import axios from "axios";

const apiBaseUrl = "/api";
export const instance = axios.create({
    baseURL: apiBaseUrl
});

instance.interceptors.request.use(function (config) {
    if (!config.headers.Authorization && localStorage.getItem("access_token") != "") {
        config.headers.Authorization = `Bearer ${localStorage.getItem("access_token")}`
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

instance.interceptors.response.use(function (response) {
    if ('content' in response.data && 'message' in response.data) {
        return {
            content: response.data.content,
            message: response.data.message,
        }
    }
    return {
        content: response.data,
        message: null,
    }
}, async function (error) {
    if (error.response.status == 401 && error.response?.data?.detail == 'The access token has expired' && !error.config._retry) {
        error.config._retry = true;
        const { content, message } = await instance.post("/auth/refresh", null, { headers: { Authorization: `Bearer ${localStorage.getItem("refresh_token")}` } })
        localStorage.setItem("access_token", content.access_token)
        localStorage.setItem("refresh_token", content.refresh_token)
        return instance(error.config);
    }
    return Promise.reject({
        content: null,
        message: error.response.data.detail
    });
}
);


export const userSignIn = (username, password) => {
    let bodyFormData = new FormData();
    bodyFormData.append('username', username);
    bodyFormData.append('password', password);
    return instance.post("/auth/signin", bodyFormData)
}

export const getUserSessions = () => {
    return instance.get('/auth/sessions')
}

export const terminateUserSession = (sid) => {
    return instance.delete(`/auth/sessions/${sid}`)
}

export const uploadFile = (file, onProgress) => {
    const formData = new FormData();
    formData.append("uploaded_file", file);
    return instance.post('/files/', formData, {
        onUploadProgress: function (progressEvent) {
            onProgress({ percent: Math.ceil(progressEvent.loaded / progressEvent.total * 100) });
        }
    })
}



export const getProcessingFiles = (page, size) => {
    return instance.get('/files/', {params: {
        page: page,
        size: size,
        state: "processing"
    }})
}
export const getErrorFiles = (page, size) => {
    return instance.get('/files/', {params: {
        page: page,
        size: size,
        state: "error"
    }})
}
export const getPrivateFiles = (page, size) => {
    return instance.get('/files/', {params: {
        page: page,
        size: size,
        state: "private"
    }})
}



export const deleteFile = (id) => {
    return instance.delete(`/files/${id}`)
}