FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        ffmpeg ripgrep libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 libxshmfence1 libgbm1 chromium-browser && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @getpochi/cli agent-browser && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN agent-browser install || true

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Next.js task environment with Inconvo SDKs and browser verification dependencies."

RUN cd /home/user && \
    npx create-next-app@14 app --typescript --eslint --app --src-dir --import-alias "@/*" --use-npm --tailwind --yes && \
    cd app && \
    npm install @inconvoai/node @inconvoai/vercel-ai-sdk ai

# Container contents:
#   - Node.js v24 and browser verification dependencies
#   - /home/user/app: Next.js app with @inconvoai/node, @inconvoai/vercel-ai-sdk, and ai installed

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
