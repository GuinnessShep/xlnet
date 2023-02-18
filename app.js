const express = require("express");
const bodyParser = require("body-parser");
const fetch = require("node-fetch");
const app = express();
const chatbot = require('./chatbot');

app.use(express.static("public"));
app.use(bodyParser.json());

app.post("/", async (req, res) => {
  const data = req.body;
  const result = await chatbot.query(data);
  res.send(result);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
