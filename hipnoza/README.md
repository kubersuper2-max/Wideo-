# Mózg w hipnozie - krótki film edukacyjny

Animowany film z lektorem (ok. 53 s) o tym, co dzieje się w mózgu w czasie hipnozy. Dwie wersje:

- `mozg_w_hipnozie_pion_9x16.mp4` - 1080×1920 (TikTok, Reels, Shorts)
- `mozg_w_hipnozie_poziom_16x9.mp4` - 1920×1080 (YouTube)

## Sceny
1. **Intro** - cząsteczki układają się w mózg.
2. **To nie jest sen** - uwaga jak światło latarki, rozpraszacze odpływają.
3. **Cichnie wewnętrzny alarm** - przednia kora obręczy się uspokaja.
4. **Mózg mocniej słyszy ciało** - oddech i serce zwalniają (kora przedczołowa + wyspa).
5. **Obserwator odpoczywa** - słabnie połączenie z siecią spoczynkową mózgu.
6. **Ból mniej przeszkadza** - sygnał dociera, ale mniej przeszkadza.
7. **Nie tracisz kontroli** - zakończenie.

Tekst lektora: `narracja.json` (zmień tekst i uruchom `zbuduj.sh`, czasy scen i napisy dopasują się same).

## Źródła
- Jiang H. i in. (2016). *Brain activity and functional connectivity associated with hypnosis.* Cerebral Cortex.
- Rainville P. i in. (1997). *Pain affect encoded in human anterior cingulate but not somatosensory cortex.* Science.

## Pliki
- `scena.html` - animacja (canvas). W przeglądarce: `scena.html#h` (poziom) lub `scena.html#v` (pion).
- `lektor.py` - głos lektora (Piper TTS, głos `pl_PL-mc_speech-medium`) + `timeline.js` z czasami.
- `muzyka.py` - muzyka ambient, przejścia, miks z lektorem (muzyka ścisza się pod głosem).
- `render.js` - renderowanie klatek do MP4, `podglad.js` - zrzuty pojedynczych klatek.
- `zbuduj.sh` - całość od początku.

Schemat mózgu jest uproszczony. Film ma charakter edukacyjny.
