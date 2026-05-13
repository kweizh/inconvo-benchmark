const { Inconvo } = require('@inconvoai/node');

const client = new Inconvo({
  apiKey: 'your-api-key-here'
});

global.inconvoClient = client;

console.log('Inconvo client initialized and saved to global.inconvoClient');
