# 21BCE3885_ML
# Document Retrieval System

## Overview

This document retrieval system is designed to efficiently handle and process user requests for document information. It includes functionalities for document search, user management, and response caching to ensure faster retrieval and improved system performance.

## Caching Strategy

### Chosen Caching Method: Redis

#### Reasoning

For this system, Redis has been chosen as the caching mechanism for the following reasons:

1. **Performance and Speed:** Redis operates in-memory, which makes it exceptionally fast for read and write operations. This is crucial for a system where quick retrieval of search results is necessary to improve user experience and system responsiveness.

2. **Persistence Options:** Redis provides various persistence options, including snapshots and append-only files. This ensures that cached data can be recovered in case of a server restart or failure, adding a layer of reliability.

3. **Scalability:** Redis supports sharding and clustering, which allows the caching layer to scale horizontally. This is important for handling increased load and ensuring consistent performance as the system grows.

4. **Advanced Features:** Redis supports various data structures such as strings, hashes, lists, sets, and sorted sets. For our use case, Redis hashes can be used to store and manage cached search results efficiently.

5. **Built-in Expiration:** Redis provides built-in support for key expiration. This allows for automatic removal of stale cache entries, ensuring that the system does not serve outdated information.

6. **Community and Support:** Redis has a strong community and extensive documentation, making it easier to find solutions to potential issues and integrate Redis effectively into the system.

### Implementation

In the current implementation, Redis is used to cache search query results. When a query is made, the system first checks if the results are available in the Redis cache. If available, the cached results are returned directly, reducing the need for repeated computation and improving response times. If not available, the system processes the query, stores the results in Redis, and then returns them to the user.

### Setup Instructions

To set up Redis for this system, follow these steps:

1. **Install Redis:**
   - On Ubuntu: `sudo apt-get install redis-server`
   - On macOS: `brew install redis`
   - On Windows, use WSL or download the Redis binaries from the Redis website.

2. **Start Redis Server:**
   ```sh
   redis-server
