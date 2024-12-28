:exclamation: **This addon is in the BETA state. Use it carefully. Try on a few notes first. Please, share your feedback
in this topic.**

Hello all,

I'd introduce new addon for language learners.

## Introduction

[Cross-Field Highlighter](https://ankiweb.net/shared/info/1312127886) takes word or collocation from the source field
and highlights it in the destination fields for better readability:  
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/short-description-3.png)

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
    11. Support of furigana.
2. Erase:
    1. CFH removes previously added highlightings from fields.
    2. CFH marks its own formatting, so it can erase exactly only its formatting and preserve other formatting.
    3. Erasing notes selected in Browser or current note in Editor.
3. Find: search for highlighted notes in Browser

## Remarks

* Current version is tested mostly for English and little for Japanese. If it doesn't work correctly for your language,
  leave a comment. It'd be great to add support for many languages. But most likely I'll need your assistance as I'm
  familiar only with English.
* If you're going to use this addon, please consider voting
  on [the addon page](https://ankiweb.net/shared/info/1312127886). It shows me that it's worth continuing to improve it.

## Introduction

"Cross-Field Highlighter" takes word or collocation from the source field and highlights it in the destination
fields:  
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/short-description-3.png)

## Screenshots

### Browser menu

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/browser-menu.png)

### Buttons in Editor

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/editor-buttons.png)

### "Highlight" dialog

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/dialog-highlight.png)

### Supported formats

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/formats.png)

### Languages without spaces (Japanese, Chinese, Thai, etc.)

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/space-delimited-language.png)  
![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/furigana.png)

### Highlighting progress

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/progress-highlight.png)

### Highlighting statistics

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/statistics-highlight.png)

### "Erase" dialog (removes previously added highlighting)

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/dialog-erase.png)

### Addon configuration

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/addon-configuration-open.png)

### About addon

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/about-dialog-open.png)

### Test cases

![](https://raw.githubusercontent.com/Aleks-Ya/cross-field-highlighter-anki-addon/master/docs/images/test-cases-open.png)

## Links

- [Addon Page](https://ankiweb.net/shared/info/1312127886)
- [Support forum thread](https://forums.ankiweb.net/t/cross-field-highlighter-addon-support-page/52592)
- [GitHub](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon)
- [Changelog](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/blob/master/CHANGELOG.md)
- [SonarQube](https://sonarcloud.io/project/overview?id=Aleks-Ya_cross-field-highlighter-anki-addon)
- [Test cases](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/blob/master/docs/cases.md)

[![Unit-tests](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/actions/workflows/python-app.yml/badge.svg)](https://github.com/Aleks-Ya/cross-field-highlighter-anki-addon/actions/workflows/python-app.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Aleks-Ya_cross-field-highlighter-anki-addon&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Aleks-Ya_cross-field-highlighter-anki-addon)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Aleks-Ya_cross-field-highlighter-anki-addon&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Aleks-Ya_cross-field-highlighter-anki-addon)
