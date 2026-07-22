# Language Text Files

Each site has two editable text files:

- `*.ko.json`: Korean mode text
- `*.en.json`: English mode text

Edit only the `text` values. Keep `key` and `source` unchanged so the language toggle can match the original page text.

When an English `text` value is empty, the page falls back to the Korean text. This makes it safe to translate the site gradually.
