
const fs = require('fs');
const path = require('path');

// Mock @inconvoai/node
const mockInconvo = {
    Inconvo: class {
        constructor(config) {
            this.config = config;
            this.conversations = {
                create: async (params) => {
                    return { id: 'conv_123', context: params.context };
                },
                messages: {
                    create: async (id, params) => {
                        return { text: 'mock response' };
                    }
                }
            };
        }
    }
};

// Override require to serve the mock for @inconvoai/node
const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(request) {
    if (request === '@inconvoai/node') {
        return mockInconvo;
    }
    return originalRequire.apply(this, arguments);
};

async function runTests() {
    try {
        const { askQuestion } = require('./index.js');
        if (typeof askQuestion !== 'function') {
            console.error(JSON.stringify({ error: 'askQuestion is not a function' }));
            process.exit(1);
        }

        // Test store_manager
        // To test the context passed to conversations.create, we need a way to spy on it.
        // Let's modify the mock to capture the context.
        let capturedContext = null;
        mockInconvo.Inconvo = class {
            constructor() {
                this.conversations = {
                    create: async (params) => {
                        capturedContext = params.context;
                        return { id: 'conv_123' };
                    },
                    messages: {
                        create: async () => ({ text: 'ok' })
                    }
                };
            }
        };

        await askQuestion('sales?', { role: 'store_manager', store_id: 42 });
        const storeManagerContext = capturedContext;

        capturedContext = null;
        await askQuestion('sales?', { role: 'admin' });
        const adminContext = capturedContext;

        console.log(JSON.stringify({
            storeManagerContext,
            adminContext
        }));
    } catch (e) {
        console.error(JSON.stringify({ error: e.message }));
        process.exit(1);
    }
}

runTests();
