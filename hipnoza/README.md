# Mózg w hipnozie - krótki film edukacyjny

Animowany film z lektorką (ok. 1:36) o tym, co dzieje się w mózgu w czasie hipnozy. Napisany prostym językiem, z myślą o klientach gabinetu hipnoterapii. Część treści (np. podświadomość) jest pokazana z perspektywy hipnoterapii, a nie jako fakt naukowy. Dwie wersje:

- `mozg_w_hipnozie_pion_9x16.mp4` - 1080×1920 (TikTok, Reels, Shorts)
- `mozg_w_hipnozie_poziom_16x9.mp4` - 1920×1080 (YouTube)

## Sceny
1. **Mózg w hipnozie** - cząsteczki układają się w mózg.
2. **To nie jest sen** - skupienie i relaks, uwaga jak światło latarki.
3. **Masz kontakt i świadomość** - głos terapeuty, możesz otworzyć oczy, nic wbrew sobie.
4. **Mózg zwalnia** - szybkie fale przechodzą w wolne fale theta.
5. **Cichnie wewnętrzny alarm** - przednia kora obręczy się uspokaja.
6. **Krytyk odpoczywa** - oko wewnętrznego krytyka się zamyka.
7. **Furtka do podświadomości** - góra lodowa, furtka, ziarna sugestii (perspektywa hipnoterapii).
8. **Ciało się rozluźnia** - oddech i serce zwalniają.
9. **Ból mniej przeszkadza** - sygnał dociera, ale mniej przeszkadza.
10. **To ty masz kontrolę** - zakończenie.

Tekst lektora: `narracja.json` (zmień tekst i uruchom `zbuduj.sh`, czasy scen i napisy dopasują się same).

## Źródła
- Jiang H. i in. (2016). *Brain activity and functional connectivity associated with hypnosis.* Cerebral Cortex.
- Rainville P. i in. (1997). *Pain affect encoded in human anterior cingulate but not somatosensory cortex.* Science.

## Pliki
- `scena.html` - animacja (canvas). W przeglądarce: `scena.html#h` (poziom) lub `scena.html#v` (pion).
- `lektor.py` - głos lektora (Piper TTS, głos `pl_PL-gosia-medium`) + `timeline.js` z czasami.
- `muzyka.py` - muzyka ambient, przejścia, miks z lektorem (muzyka ścisza się pod głosem).
- `render.js` - renderowanie klatek do MP4, `podglad.js` - zrzuty pojedynczych klatek.
- `zbuduj.sh` - całość od początku.

Schemat mózgu jest uproszczony. Film ma charakter edukacyjny.
