# Language Text Files

Each site has two editable text files:

- `*.ko.json`: Korean mode text
- `*.en.json`: English mode text

The JSON files are generated from the current HTML and the existing translation catalog. To synchronize every page after changing Korean copy, run:

```powershell
node scripts/sync-i18n.mjs
```

Add new or corrected English translations to `scripts/i18n-overrides.en.json`. The synchronizer preserves existing keys and script-generated strings while adding newly discovered HTML text.

When an English `text` value is empty, the page falls back to the Korean text. This makes it safe to translate the site gradually.
