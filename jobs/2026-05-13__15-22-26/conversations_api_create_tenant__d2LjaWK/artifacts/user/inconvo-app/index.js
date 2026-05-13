require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');
const path = require('path');

const apiKey = process.env.INCONVO_API_KEY;
const agentId = process.env.INCONVO_AGENT_ID;
const outputPath = '/home/user/inconvo-app/output.json';

async function main() {
    const client = new Inconvo({
        apiKey: apiKey,
    });

    let result;
    try {
        result = await client.agents.conversations.create(agentId, {
            userIdentifier: "user_123",
            context: {
                tenant_id: "tenant_456"
            }
        });
    } catch (error) {
        result = {
            error: true,
            message: error.message,
            stack: error.stack
        };
    }

    fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
    console.log(`Result saved to ${outputPath}`);
}

main();
