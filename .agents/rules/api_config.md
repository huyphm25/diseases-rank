---
description: API Configuration and Credentials
---

# API Config Guidelines

When writing code that interacts with external APIs requiring authentication (like API keys or tokens):
1. **Always use a configuration file** (such as `config.json` or `.env`) to manage keys instead of strictly relying on environment variables.
2. **Provide an example file** (like `config.example.json`) so it is easy for users to know what keys are needed and where to put them.
3. Update the codebase to gracefully load keys from this configuration file.
