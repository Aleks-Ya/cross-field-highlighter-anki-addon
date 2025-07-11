
Test cases for Cross-Field Highlighter (CFH)
============================================

CFH has highlighting and erasing algorithms which are verified by auto-tests.
Test cases listed in the table below are used to verify these algorithms.

Auto-tests perform for each test case:
1. Highlight "Collocation" in "Original text" using Bold format
2. Verify that the highlighted text is the same as in "Expected text"
3. Erase the highlighted text
4. Verify that the erased text is the same as "Original text"


|#|Title|Collocation|Original text|Highlighted text|
| :---: | :---: | :---: | :---: | :---: |
|[1](#case-1)|General: single word repeats one time|`beautiful`|`Hello, beautiful world!`|`Hello, <b class="cross-field-highlighter">beautiful</b> world!`|
|[2](#case-2)|General: single word repeats several times|`beautiful`|`Hello, beautiful world and beautiful day!`|`Hello, <b class="cross-field-highlighter">beautiful</b> world and <b class="cross-field-highlighter">beautiful</b> day!`|
|[3](#case-3)|General: case insensitive|`beautiful`|`Hello, Beautiful world!`|`Hello, <b class="cross-field-highlighter">Beautiful</b> world!`|
|[4](#case-4)|General: collocation|`take forever`|`Downloading a movie takes forever.`|`Downloading a movie <b class="cross-field-highlighter">takes</b> <b class="cross-field-highlighter">forever</b>.`|
|[5](#case-5)|General: the beginning of a sentence|`hello`|`Hello beautiful world!`|`<b class="cross-field-highlighter">Hello</b> beautiful world!`|
|[6](#case-6)|General: empty collocation||`Hello, beautiful world!`|`Hello, beautiful world!`|
|[7](#case-7)|General: entire collocation as token (+case insensitive)|`to hurry up`|`Need to hurry up. He Hurries everyone up.`|`Need to <b class="cross-field-highlighter">hurry</b> <b class="cross-field-highlighter">up</b>. He <b class="cross-field-highlighter">Hurries</b> everyone <b class="cross-field-highlighter">up</b>.`|
|[8](#case-8)|Word forms: s-suffix|`intrusion`|`Resistant to intrusions.`|`Resistant to <b class="cross-field-highlighter">intrusions</b>.`|
|[9](#case-9)|Word forms: ing base (append)|`drown`|`Protection against drowning.`|`Protection against <b class="cross-field-highlighter">drowning</b>.`|
|[10](#case-10)|Word forms: ing base (case insensitive)|`abstain`|`Abstaining from chocolate`|`<b class="cross-field-highlighter">Abstaining</b> from chocolate`|
|[11](#case-11)|Word forms: ing (dropping e)|`overtake`|`A driver was overtaking a slower vehicle.`|`A driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.`|
|[12](#case-12)|Word forms: ing (ie-ending)|`lie`|`A cat was lying on the floor.`|`A cat was lying on the floor.`|
|[13](#case-13)|Word forms: forgotten|`forget`|`I've forgotten your name.`|`I've <b class="cross-field-highlighter">forgotten</b> your name.`|
|[14](#case-14)|Word forms: forgetting|`forget`|`I am forgetting my keys again.`|`I am <b class="cross-field-highlighter">forgetting</b> my keys again.`|
|[15](#case-15)|Short words: be|`be`|`To be is to have been while being beautiful.`|`To <b class="cross-field-highlighter">be</b> is to have <b class="cross-field-highlighter">been</b> while <b class="cross-field-highlighter">being</b> beautiful.`|
|[16](#case-16)|Short words: minimum length (should not highlight 'our')|`phase out`|`Our meetings phased out last year.`|`Our meetings <b class="cross-field-highlighter">phased</b> <b class="cross-field-highlighter">out</b> last year.`|
|[17](#case-17)|Short words: limit max length (should not highlight 'society')|`so`|`Society changes so quickly.`|`Society changes <b class="cross-field-highlighter">so</b> quickly.`|
|[18](#case-18)|Stop words: to|`to overtake`|`Driver was overtaking a slower vehicle.`|`Driver was <b class="cross-field-highlighter">overtaking</b> a slower vehicle.`|
|[19](#case-19)|Stop words: a|`a driver`|`Driver was overtaking a slower vehicle.`|`<b class="cross-field-highlighter">Driver</b> was overtaking a slower vehicle.`|
|[20](#case-20)|Stop words: an|`an automobile`|`Automobile was overtaking a slower vehicle.`|`<b class="cross-field-highlighter">Automobile</b> was overtaking a slower vehicle.`|
|[21](#case-21)|Stop words: entire collocation comprises stop words|`an a to`|`An automobile is going to overtake a slower vehicle.`|`An automobile is going to overtake a slower vehicle.`|
|[22](#case-22)|Short words: should not highlight 'Measure'|`mesh`|`Measure and mark the mesh size.`|`Measure and mark the <b class="cross-field-highlighter">mesh</b> size.`|
|[23](#case-23)|HTML tags: li|`lid`|`<li>I opened the lid of the jar to get some jam.</li>`|`<li>I opened the <b class="cross-field-highlighter">lid</b> of the jar to get some jam.</li>`|
|[24](#case-24)|HTML tags: div|`ivy`|`<li><div>There is ivy trailing all over the wall.</div></li>`|`<li><div>There is <b class="cross-field-highlighter">ivy</b> trailing all over the wall.</div></li>`|
|[25](#case-25)|HTML tags: collocation touches tag|`hello`|`<li>Hello, beautiful world!</li>`|`<li><b class="cross-field-highlighter">Hello</b>, beautiful world!</li>`|
|[26](#case-26)|HTML tags: tag contains spaces|`hello`|`<p class="big">Hello, beautiful world!</p>`|`<p class="big"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>`|
|[27](#case-27)|HTML tags: tag contains collocation|`hello`|`<p class="hello">Hello, beautiful world!</p>`|`<p class="hello"><b class="cross-field-highlighter">Hello</b>, beautiful world!</p>`|
|[28](#case-28)|HTML tags: non-breakable space|`beautiful`|`Hello,&nbsp;beautiful&nbsp;world!`|`Hello,&nbsp;<b class="cross-field-highlighter">beautiful</b>&nbsp;world!`|
|[29](#case-29)|HTML tags: tag in collocation|`<i>beautiful</i>`|`Hello, beautiful world!`|`Hello, <b class="cross-field-highlighter">beautiful</b> world!`|
|[30](#case-30)|HTML tags: tags in collocation|`<i>beautiful</i> <b>world</b>`|`Hello, <i>beautiful</i> world!`|`Hello, <i><b class="cross-field-highlighter">beautiful</b></i> <b class="cross-field-highlighter">world</b>!`|
|[31](#case-31)|Cloze note: entire|`study`|`I {{c1:study}} every day.`|`I {{c1:<b class="cross-field-highlighter">study</b>}} every day.`|
|[32](#case-32)|Cloze note: sub-word|`study`|`He {{c2:also studies hard}} every day.`|`He {{c2:also <b class="cross-field-highlighter">studies</b> hard}} every day.`|
|[33](#case-33)|Furigana: ruby collocation, ruby text|`<ruby>東京<rt>とうきょう</rt></ruby>`|`<p><ruby>東京<rt>とうきょう</rt></ruby>は首都です。</p>`|`<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>`|
|[34](#case-34)|Furigana: ruby collocation, brackets text|`<ruby>東京<rt>とうきょう</rt></ruby>`|`<p>東京[とうきょう]は首都です。</p>`|`<p><b class="cross-field-highlighter">東京</b>[<b class="cross-field-highlighter">とうきょう</b>]は首都です。</p>`|
|[35](#case-35)|Furigana: brackets collocation, ruby text|`東京[とうきょう]`|`<p><ruby>東京<rt>とうきょう</rt></ruby>は首都です。</p>`|`<p><ruby><b class="cross-field-highlighter">東京</b><rt><b class="cross-field-highlighter">とうきょう</b></rt></ruby>は首都です。</p>`|
|[36](#case-36)|Furigana: brackets collocation, brackets text|`東京[とうきょう]`|`<p>東京[とうきょう]は首都です。</p>`|`<p><b class="cross-field-highlighter">東京[とうきょう]</b>は首都です。</p>`|
|[37](#case-37)|Special symbols: collocation touches dot|`hip`|`Her child is at her hip.`|`Her child is at her <b class="cross-field-highlighter">hip</b>.`|
|[38](#case-38)|Special symbols: collocation contains forward slash|`beautiful/nice`|`Hello, beautiful and nice world!`|`Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!`|
|[39](#case-39)|Special symbols: collocation contains back slash|`beautiful\nice`|`Hello, beautiful and nice world!`|`Hello, <b class="cross-field-highlighter">beautiful</b> and <b class="cross-field-highlighter">nice</b> world!`|
|[40](#case-40)|Special symbols: collocation contains angle brackets|`beautiful>nice<perfect`|`Hello, beautiful, nice, and perfect world!`|`Hello, <b class="cross-field-highlighter">beautiful</b>, <b class="cross-field-highlighter">nice</b>, and <b class="cross-field-highlighter">perfect</b> world!`|
|[41](#case-41)|Special symbols: collocation contains square brackets|`beautiful[nice]`|`Hello, [beautiful] and nice [world]!`|`Hello, [<b class="cross-field-highlighter">beautiful</b>] and <b class="cross-field-highlighter">nice</b> [world]!`|
|[42](#case-42)|Special symbols: curly quotes (smart quites)|`rally`|`It is a “rally.”`|`It is a “<b class="cross-field-highlighter">rally</b>.”`|
|[43](#case-43)|Special symbols: hyphen, em dash|`rally`|`rally-rally—rally`|`<b class="cross-field-highlighter">rally</b>-<b class="cross-field-highlighter">rally</b>—<b class="cross-field-highlighter">rally</b>`|
|[44](#case-44)|Thai language|`ดี`|`วันนี้เป็นวันที่ดีมาก`|`วันนี้เป็นวันที่<b class="cross-field-highlighter">ดี</b>มาก`|
|[45](#case-45)|Korean language|`좋은`|`오늘은 정말 좋은 날이에요`|`오늘은 정말 <b class="cross-field-highlighter">좋은</b> 날이에요`|
|[46](#case-46)|Chinese language|`天气`|`今天天气非常好`|`今天<b class="cross-field-highlighter">天气</b>非常好`|
|[47](#case-47)|Arabic language|`جميل`|`الطقس اليوم جميل`|`الطقس اليوم <b class="cross-field-highlighter">جميل</b>`|
|[48](#case-48)|Hebrew language|`נהדר`|`היום יום נהדר`|`היום יום <b class="cross-field-highlighter">נהדר</b>`|
