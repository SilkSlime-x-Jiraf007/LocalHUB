import { NAlert, useMessage } from "naive-ui";
import { useRouter } from 'vue-router'
import { h } from "vue";




export function apiWrapper() {
    const messager = useMessage()
    const router = useRouter()

    const renderMessage = (props) => {
        const { type } = props;
        return h(
            NAlert,
            {
                closable: false,
                type: type === "loading" ? "default" : type,
                style: {
                    boxShadow: "var(--n-box-shadow)",
                    maxWidth: "80vw"
                }
            },
            {
                default: () => props.content
            }
        );
    };

    const wrap = async (apiCall, callback = null, errorCallback = null, silent=false) => {
        // TODO
        try {
            const { content, message } = await apiCall();
            if (message && !silent) messager.success(message, {render: renderMessage})
            if (callback) callback(content)
        } catch ({ content, message }) {
            if (message && !silent) messager.error(message, {render: renderMessage})
            if (errorCallback) errorCallback(content)
            // TODO
            // ROUTER THINGS
            if (message == "There is no session with this refresh token") {
                localStorage.clear()
                router.push({name: "Sign In"})
            }
        }
    }
    return { wrap }
}