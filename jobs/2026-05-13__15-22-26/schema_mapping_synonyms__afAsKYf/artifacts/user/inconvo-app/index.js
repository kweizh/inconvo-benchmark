const fs = require('fs');
const yaml = require('yaml'); // We will install yaml package
try {
  const file = fs.readFileSync('./inconvo.yaml', 'utf8');
  console.log("YAML parsed successfully");
} catch (e) {
  console.error(e);
  process.exit(1);
}
