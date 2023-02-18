const fetch = require("node-fetch");

async function query(data) {
  const response = await fetch(
    "https://api-inference.huggingface.co/models/xlnet-base-cased",
    {
      headers: { Authorization: "Bearer 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" },
      method: "POST",
      body: JSON.stringify(data),
    }
  );
  const result = await response.json();
  return result;
}

module.exports = {
  query: query,
};
