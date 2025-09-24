# masterbrain2.0

## Project Structure

```
masterbrain2.0/
├── main.py
├── railway.json
├── requirements.txt
├── start.sh
└── README.md
```

## FastAPI Application

The FastAPI service exposes two endpoints:

- `POST /ingest` &ndash; accepts commit metadata and persists it through `mem0.add_memory` when the dependency is available. The
  JSON response includes the original payload, whether mem0 is enabled, and an optional memory reference.
- `GET /` &ndash; a lightweight health check endpoint suitable for uptime probes.

### Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Launch the API with the helper script (defaults to port `8000` if `PORT` is unset):

   ```bash
   ./start.sh
   ```

3. Navigate to `http://127.0.0.1:8000/docs` to access the interactive Swagger UI. Execute the `POST /ingest` request with sample
   commit data (for example, SHA, author, and message) and confirm that the response contains `"status": "received"`.

### Railway Deployment

Railway reads `railway.json` during deployments and executes `./start.sh`, ensuring that the service binds to the platform-provided
port. Configure any required environment variables (such as credentials for mem0) in the Railway dashboard.

### mem0 Troubleshooting

The `mem0` package is listed in `requirements.txt`, but it may not be publicly available. If you encounter an import error or see a
`mem0.add_memory is unavailable` warning in the API response:

1. Confirm whether mem0 is distributed privately (for example, a Git repository or internal package index). Update
   `requirements.txt` with the appropriate reference, such as `mem0 @ git+https://github.com/example/mem0.git`.
2. Reinstall dependencies after updating the requirement specification:

   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. Restart the FastAPI service (`./start.sh`) so the new dependency is loaded.
4. Repeat the Swagger UI smoke test (`POST /ingest`) to verify that the response now includes a `memory_reference` key, which
   indicates that `mem0.add_memory` executed successfully.
