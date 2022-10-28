import axios from "axios";
const apiBaseUrl = "http://localhost:3030/api";
const instance = axios.create({
    baseURL: apiBaseUrl
});

const authorizedRequestConfig = { headers: { Authorization: "Bearer " + localStorage.getItem("accessToken") } }

const getData = (response) => {
    let res = {
        content: null,
        message: null
    }
    if ('data' in response)
        if ('content' in response.data && 'message' in response.data)
            if ('content' in response.data)
                res.content = response.data.content
            if ('message' in response.data)
                res.content = response.data.content
        else
            res.content = response.data
    return res
}

const getError = (error) => {
    if ('response' in error)
        if ('data' in error.response)
            if ('detail' in error.response.data)
                return {error: error.response.data.detail}
    return {error: "Unknown error"}
}


export const userSignIn = (fd) => instance.post("/auth/signin", fd).then(result => getData(result)).catch(thing => getError(thing));
export const userEdit = (username, password) => instance.put("/users/self", {username: username, password: password}, authorizedRequestConfig).then(result => result.data);