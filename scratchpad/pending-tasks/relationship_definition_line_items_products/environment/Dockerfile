FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Inconvo project pre-seeded with line_items and products tables but missing the line_item_to_product relation."

RUN mkdir -p /home/user/inconvo-app && \
    cd /home/user/inconvo-app && \
    npm init -y && \
    npm install @inconvoai/node dotenv

RUN cat > /home/user/inconvo-app/inconvo.yaml <<'EOF'
tables:
  line_items:
    state: Queryable
    fields:
      id: { state: On }
      order_id: { state: On }
      product_id: { state: On }
      quantity: { state: On, type: measure }
  products:
    state: Queryable
    fields:
      id: { state: On }
      name: { state: On, type: dimension }
      price: { state: On, type: measure }
EOF

RUN cat > /home/user/inconvo-app/index.js <<'EOF'
const fs = require('fs');
const path = require('path');
const { randomUUID } = require('node:crypto');
const Inconvo = require('@inconvoai/node').default;

async function main() {
  const inconvo = new Inconvo({
    apiKey: process.env.INCONVO_API_KEY,
  });

  const agentConvo = await inconvo.agents.conversations.create(
    process.env.INCONVO_AGENT_ID,
    {
      userIdentifier: randomUUID().toString(),
      userContext: {
        organisationId: 1,
      },
    },
  );

  const agentResponse = await inconvo.agents.conversations.response.create(
    agentConvo.id,
    {
      agentId: process.env.INCONVO_AGENT_ID,
      message: "Hello agent!",
      stream: false,
    },
  );

  fs.writeFileSync(
    path.join(__dirname, 'response.json'),
    JSON.stringify(agentResponse, null, 2),
  );
  console.log('Saved response.json');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
EOF

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for running the Inconvo SDK script
#   - /home/user/inconvo-app: Inconvo project with @inconvoai/node and dotenv installed
#   - /home/user/inconvo-app/inconvo.yaml: starter semantic model with line_items and products tables but NO relations entry
#   - /home/user/inconvo-app/index.js: starter SDK script that the agent must update to ask the relation-aware question

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
