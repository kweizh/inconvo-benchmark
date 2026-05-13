
const originalFetch = global.fetch;
global.fetch = async (...args) => {
    const url = args[0].toString();
    // Intercept inconvo API calls
    if (url.includes('inconvo')) {
        return new Response(JSON.stringify({ id: "conv_mock_123", message: "Mocked response" }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    return originalFetch(...args);
};
