# Offline pip wheels (optional)

Bootstrap / Phase A–B pass `--find-links ./wheels` so a local cache can satisfy
packages when PyPI is slow or offline.

This folder is intentionally empty in the repo. Drop `.whl` files here if you
want offline installs; they are gitignored by default.
