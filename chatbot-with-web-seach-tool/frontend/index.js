const query = document.getElementById("query")
const container = document.getElementById("container")
const btn = document.querySelector("button")


query.addEventListener("keyup", handleEnter)
const loading = document.createElement('div');
loading.className = "animate-pulse"
loading.textContent = "Thinking...."

const threadId = Date.now().toString(36) + Math.random().toString(36).substring(2,8)


async function handleEnter(e) {
    if(e.code == "Enter") {
        query.disabled = true;
        const q = e.target.value;
        query.value = '';

        let msg = document.createElement('div');
        msg.className = "bg-neutral-700 w-fit p-2 px-3 rounded-2xl  ml-auto max-w-xs";
        msg.textContent = q;
        container.appendChild(msg);
        container.appendChild(loading);

        const response = await getResponse(q);

        msg = document.createElement('div')
        msg.className = "w-fit rounded-full my-4 whitespace-pre-line";
        msg.textContent = response;
        loading.remove();
        container.appendChild(msg);
        container.scrollTop = container.scrollHeight;
        query.disabled = false;
        query.focus();
    }
}



async function getResponse(query) {
    const response = await axios.post(`http://localhost:3001/chat`, {
        query: query,
        threadId: threadId
    })
    console.log(response.data.response);
    return response.data.response;
}