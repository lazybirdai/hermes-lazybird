# Lazybird for Hermes Agent

Realistic [Lazybird](https://lazybird.app) voices for [Hermes Agent](https://github.com/NousResearch/hermes-agent): text to speech, voice bubbles on messaging platforms, and your own cloned or designed voices.

## Install

```bash
hermes plugins install lazybird
# or straight from GitHub: hermes plugins install lazybirdai/hermes-lazybird/lazybird
```

Create an API key at [lazybird.app/platform](https://www.lazybird.app/platform) (free plan: 10,000 characters a month) and add it to `~/.hermes/.env`:

```bash
LAZYBIRD_API_KEY=your-key
```

Then pick Lazybird as the TTS provider in `~/.hermes/config.yaml`:

```yaml
tts:
  provider: lazybird
  voice: tgJ2Hes6DauwTg8kFrRPLN   # optional; this is Elyssia, the default
```

`tts.voice` takes any voice id from the [voice library](https://lazybird.app/voices), or a voice you cloned or designed in your Lazybird account. `tts.speed` is passed through as the voice speed.

## Skill and MCP server

For more than speech (voice search, cloning, designing voices, video projects), add the Lazybird skill or the MCP server:

```bash
# Skill: teaches the agent the whole Lazybird API
hermes skills install skills-sh/lazybirdai/skills/lazybird-api

# MCP server: signs in with OAuth in your browser
hermes mcp add lazybird --url https://api.lazybird.app/mcp --auth oauth
```

## What it sends

Each synthesis sends the text, the voice id and your API key (in the `X-API-Key` header) to `https://api.lazybird.app/v2/generate-speech`. Characters count against your Lazybird plan. The MP3 that comes back is saved where Hermes asks (its audio cache). The plugin has no telemetry and makes no other network calls.

## Development

```bash
pytest                                          # inside a Hermes checkout's venv
hermes plugins validate --install-deps lazybird
```

## License

MIT
