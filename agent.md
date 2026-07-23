# Project Agent

This agent is tailored for the `weather` GUI project.

## Purpose

- Help maintain and extend the weather GUI application.
- Focus on code quality, tests, and correctness for Python modules under `src/` and `test/`.
- Provide concise, actionable suggestions for bug fixes, refactors, and documentation.

## Project Scope

- `src/pico_w/`: Pico W-specific weather data handling and sensor integration.
- `src/rpi/`: Raspberry Pi GUI, widgets, and data transfer logic.
- `test/`: Unit tests for Pico W and Raspberry Pi components.

## Agent Behavior

- Prefer minimal, precise responses.
- Keep edits limited to relevant files unless tasked otherwise.
- Use the repository structure to guide fixes and improvements.
- Avoid unrelated Python or GUI frameworks outside this project.

## Expectations

- When asked to add features, include tests for new behavior.
- When asked to fix bugs, validate by referencing existing tests or file structure.
- When adding documentation, keep it consistent with the README and module responsibilities.
