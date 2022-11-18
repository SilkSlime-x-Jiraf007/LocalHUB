import { h } from 'vue';
import { NBadge } from "naive-ui";
export const renderTextBadge = (text, count) => {
    return h(
        'div',
        { style: "display: flex; align-items: center; gap: 6px;" },
        [
            h('span', null, text),
            h(NBadge, { value: count, type: "kek", showZero: true })
        ]
    )
}