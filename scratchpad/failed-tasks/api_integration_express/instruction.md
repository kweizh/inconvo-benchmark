# Task: API Integration with Express

Integrate Inconvo into an Express.js application to provide a 'chat-with-data' endpoint. You are provided with a PostgreSQL database containing `stores`, `products`, and `orders` tables.

## Requirements

1.  **Initialize Inconvo**: Run `inconvo init` to set up the project.
2.  **Configure Semantic Model**: Edit `inconvo.yaml` to map the database schema.
    *   `orders` should be `Queryable`.
    *   `products` and `stores` should be `Joinable`.
    *   Ensure relationships between `orders`, `products`, and `stores` are defined.
3.  **Implement Express Endpoint**:
    *   Create a file `server.js`.
    *   Implement a `POST /api/chat` endpoint.
    *   The endpoint should receive a JSON body: `{ "message": "...", "store_id": 123 }`.
    *   Use the `@inconvoai/node` SDK to create a conversation.
    *   **Crucial**: Pass the `store_id` into the Inconvo conversation context so that the results are filtered for that specific store.
    *   Return the Inconvo response as JSON.
4.  **Database**: Use the `DATABASE_URL` provided in the environment.

## Context
Inconvo handles the mapping of natural language to SQL via a semantic layer. Your job is to bridge the application's user context (the `store_id`) to Inconvo's query engine.

**Constraints:**
- Use `@inconvoai/node`, `express`, and `dotenv`.
- The server should listen on port 3000.
- Handle errors gracefully.
