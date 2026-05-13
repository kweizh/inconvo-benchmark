const fs = require('fs');
const yaml = fs.readFileSync('inconvo.yaml', 'utf8');
if (!yaml.includes('line_item_to_product') || !yaml.includes('line_items.product_id') || !yaml.includes('products.id')) {
    console.error('Relationship not found or incorrect');
    process.exit(1);
}
console.log('Success');
