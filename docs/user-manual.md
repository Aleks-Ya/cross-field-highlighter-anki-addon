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
    11. Shortcut support ("Ctrl+Shift+H" by default)
2. Erase:
    1. CFH removes previously added highlightings from fields.
    2. CFH marks its own formatting, so it can erase exactly only its formatting and preserve other formatting.
    3. Erasing notes selected in Browser or current note in Editor.
    4. Shortcut support (not set by default)
3. Show in Browser:
    1. Show all highlighted notes
    2. Show notes modified by the latest run

## Customize formatting

CFH supports 4 formats: Bold, Italic, Underlined and Yellow background.  
In HTML these formats are represented like:

```html
<b class="cross-field-highlighter">Bold</b>
<i class="cross-field-highlighter">Italic</i>
<u class="cross-field-highlighter">Underlined</u>
<mark class="cross-field-highlighter">Yellow Background</mark>
```

User can customize these formats using CSS styles in card template.  
Example of CSS style:

```css
.cross-field-highlighter {
    color: DarkSlateGray;
    background-color: LightGray;
    font-size: 1.5em;
    font-family: sans-serif;
}
```

This style on screenshot:
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/custom-style.png)
