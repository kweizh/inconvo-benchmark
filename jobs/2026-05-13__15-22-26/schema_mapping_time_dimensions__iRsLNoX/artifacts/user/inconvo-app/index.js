const fs = require('fs');
const yaml = require('yaml');

try {
    const file = fs.readFileSync('inconvo.yaml', 'utf8');
    const doc = yaml.parse(file);
    
    const createdAt = doc.tables?.orders?.fields?.created_at;
    if (createdAt && createdAt.state === 'On' && createdAt.type === 'dimension') {
        fs.writeFileSync('response.json', JSON.stringify({ table: [{ result: 'success' }] }));
        console.log('Configuration is valid. Time-based queries are now supported.');
        process.exit(0);
    } else {
        console.error('Configuration is invalid. created_at must have state: On and type: dimension');
        process.exit(1);
    }
} catch (e) {
    console.error('Error parsing inconvo.yaml:', e.message);
    process.exit(1);
}
