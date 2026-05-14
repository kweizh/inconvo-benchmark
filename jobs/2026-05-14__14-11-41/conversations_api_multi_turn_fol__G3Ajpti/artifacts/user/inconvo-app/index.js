require('dotenv').config();
const { Inconvo } = require('@inconvoai/node');
const fs = require('fs');

async function main() {
    const inconvo = new Inconvo({
        apiKey: process.env.INCONVO_API_KEY
    });
    
    const agentId = process.env.INCONVO_AGENT_ID;
    
    // Create a new conversation
    const conversation = await inconvo.agents.conversations.create(agentId, {
        userIdentifier: "test-user",
        userContext: { organisationId: 1, store_id: 1 }
    });
    
    const convId = conversation.id;
    fs.writeFileSync('/home/user/inconvo-app/conversation_id.txt', convId);
    
    // Send the first message
    const firstResponse = await inconvo.agents.conversations.response.create(convId, {
        agentId: agentId,
        message: "Show me my top 5 customers by total order amount.",
        stream: false
    });
    
    fs.writeFileSync('/home/user/inconvo-app/first_response.json', JSON.stringify(firstResponse, null, 2));
    
    // Send the followup message
    const secondResponse = await inconvo.agents.conversations.response.create(convId, {
        agentId: agentId,
        message: "Now show me only those located in the United States.",
        stream: false
    });
    
    fs.writeFileSync('/home/user/inconvo-app/second_response.json', JSON.stringify(secondResponse, null, 2));
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
