---
name: sync-characters
description: Re-sync character reference images when files are deleted or moved. Use when user says "sync characters", "re-sync", or reports missing character references.
---

# Sync Characters

Re-syncs the character reference image library at `sample/characters/`.

## When to Use

- User deleted files and wants to restore character references
- Character images got moved or renamed
- User wants to see what characters are available
- User wants to add a new character

## Steps

1. **List current characters:**
   ```bash
   ls -la sample/characters/
   ```

2. **Check each character directory for images:**
   ```bash
   for dir in sample/characters/*/; do
     echo "=== $(basename $dir) ==="
     ls -la "$dir"
   done
   ```

3. **If a character directory is missing or empty**, report it and ask the user to provide new reference images.

4. **Known characters and their sources:**
   - `clawd` — The Claude Code mascot (orange pixel robot). Source images originally from `sample/` directory. Files:
     - `clawd_logo.png` — Flat pixel art logo
     - `clawd_sticker.png` — Sticker version with >< eyes and white outline
     - `clawd_welcome.png` — Welcome screen version

5. **To restore missing characters**, copy from original sources:
   ```bash
   # Restore clawd from sample/ originals (if they still exist)
   mkdir -p sample/characters/clawd
   cp sample/image.png sample/characters/clawd/clawd_logo.png
   cp "sample/image copy.png" sample/characters/clawd/clawd_sticker.png
   cp "sample/image copy 2.png" sample/characters/clawd/clawd_welcome.png
   ```

6. **To add a new character**, create a directory and add reference images:
   ```bash
   mkdir -p sample/characters/{character_name}
   # Then copy reference images into the directory
   ```

7. **Report final state** — list all characters and their image counts.
