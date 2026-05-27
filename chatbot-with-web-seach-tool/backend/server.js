import express from 'express'
import { generate } from './chatbot.js';
import cors from 'cors';
const app = express();
const PORT = 3001;

app.use(cors())
app.use(express.json());


app.get("/", (req,res) => {
    res.send("Hi There, I am Creating Chat GPT Clone");
});

app.post("/chat", async (req, res) => {
    const {query, threadId} = req.body;

    if(!query || !threadId) {
        res.status(400).json({message: "Query and threadId both are required"})
    }
    const result = await generate(query, threadId);
    // const result = "Gotcha";
    res.send({response: result});
});


app.listen(PORT, () => {
    console.log(`Server Listening to Port : ${PORT}`);
})