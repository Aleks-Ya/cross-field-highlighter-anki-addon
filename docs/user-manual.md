# User Manual for "Cross-Field Highlighter" Anki addon

"Cross-Field Highlighter" (CFH) takes word or collocation from the source field and highlights it in the destination
fields:

## Features

1. Highlight:
    1. CFH takes word from the source field and highlights it in the destination fields.
    2. Supported formats: Bold, Italic, Underlined, Yellow Background.
    3. Word endings can differ: e.g. source word `study` will be also highlighted in forms of `studies`, `studied`,
       `studying`, etc.
    4. Collocations are supported: if the source field contains several words (collocation), all these words will be
       highlighted excluding stop words.
    5. Stop words: given stop words will be excluded from the source field (e.g. stop words `a` from `a cat` will be
       treated as `cat`).
    6. Case-insensitive: the source collocation can be in any case.
    7. Non-space-delimited languages (Japanese, Chinese, Thai, etc.) are supported.
    8. Idempotence: repeating highlighting the same notes doesn't duplicate highlighting.
    9. HTML tags are skipped from highlighting.
    10. Highlighting notes selected in Browser or current note in Editor.
2. Erase:
    1. CFH removes previously added highlightings from fields.
    2. CFH marks its own formatting, so it can erase exactly only its formatting and preserve other formatting.
    3. Erasing notes selected in Browser or current note in Editor.
3. Find: search for highlighted notes in Browser
