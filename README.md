# RapidAPI Hermes Plugin

A generic plugin for Hermes Agent to interact with the RapidAPI marketplace.

## Features
- Provides the `rapidapi_request` tool to hermes.
- Automatically handles injection of `X-RapidAPI-Key` and `X-RapidAPI-Host` headers.
- Supports `GET` and `POST` methods with JSON payloads.

## Setup

1. Copy this folder into `~/.hermes/plugins/rapidapi`.
2. Add your RapidAPI key to `~/.hermes/.env`:
   ```bash
   RAPIDAPI_KEY=your_key_here
   ```
3. Enable the plugin in `~/.hermes/config.yaml`:
   ```yaml
   plugins:
     enabled:
       - rapidapi
   ```
4. Add the `rapidapi` toolset to your active platform in `config.yaml` or enable it via `hermes tools`.
5. Restart the Hermes gateway or CLI.

## Usage Example

```python
rapidapi_request(
    host="weatherapi-com.p.rapidapi.com",
    endpoint="/current.json?q=London"
)
```
