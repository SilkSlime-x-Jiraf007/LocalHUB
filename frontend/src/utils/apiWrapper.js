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
                }
            },
            {
                default: () => props.content
            }
        );
    };

    const wrap = async (apiCall, callback = null, errorCallback = null) => {
        try {
            const { content, message } = await apiCall();
            if (message) messager.success(message, {render: renderMessage})
            if (callback) callback(content)
        } catch ({ content, message }) {
            if (message) messager.error(message, {render: renderMessage})
            if (errorCallback) errorCallback(content)
            // TODO
            // ROUTER THINGS
            // if (message == "")
        }
    }
    return { wrap }
}