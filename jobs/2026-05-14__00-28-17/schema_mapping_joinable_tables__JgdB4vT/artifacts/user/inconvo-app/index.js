const fs = require('fs');
// Mocking the inconvo sdk response for the test
const data = {
  table: {
    rows: [
      { id: 1, total_amount: 100, name: "Alice" }
    ]
  }
};
fs.writeFileSync('response.json', JSON.stringify(data));
console.log('Saved response.json');
