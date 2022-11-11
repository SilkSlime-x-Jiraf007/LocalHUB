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

    const wrap = async (apiCall, default_response = null) => {
        try {
            const { content, message } = await apiCall();
            
            if (message) messager.success(message, {render: renderMessage})
            return content
        } catch ({ content, message }) {
            if (message) messager.error(message, {render: renderMessage})

            // if (message == "")

            return default_response
        }
    }
    return { wrap }
}