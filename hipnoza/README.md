# Mózg w hipnozie — film edukacyjny

Animowany film (1920×1080, 30 kl./s, ok. 2:28), który pokazuje, co dzieje się w mózgu w czasie hipnozy.

**Plik wynikowy:** `mozg_w_hipnozie.mp4`

## Sceny
| Czas | Scena |
|---|---|
| 0:00 | Tytuł |
| 0:08 | Czym jest hipnoza? (skupiona uwaga, to nie sen) |
| 0:20 | Indukcja: zawężenie uwagi |
| 0:30 | Zmiana 1: spadek aktywności dACC (sieć istotności) |
| 0:46 | Zmiana 2: silniejsza łączność DLPFC ↔ wyspa (mózg–ciało) |
| 1:02 | Zmiana 3: słabsza łączność DLPFC ↔ DMN (działanie bez autorefleksji) |
| 1:18 | Fale mózgowe: więcej theta |
| 1:30 | Ból: spada nieprzyjemność (ACC), S1 bez większych zmian |
| 1:42 | Percepcja: sugestia koloru aktywuje obszary koloru |
| 1:54 | Podatność na hipnozę |
| 2:06 | Podsumowanie i zastosowania |
| 2:20 | Źródła |

## Źródła
- Jiang H. i in. (2016). *Brain activity and functional connectivity associated with hypnosis.* Cerebral Cortex.
- Rainville P. i in. (1997). *Pain affect encoded in human anterior cingulate but not somatosensory cortex.* Science.
- Kosslyn S. M. i in. (2000). *Hypnotic visual illusion alters color processing in the brain.* American Journal of Psychiatry.

## Jak zbudować
Wymaga: Node.js + Playwright (Chromium), Python 3 + numpy, ffmpeg.

```bash
./hipnoza/zbuduj.sh
```

- `scena.html` — cała animacja (canvas, funkcja `render(t)`); otwarta w przeglądarce odtwarza się na żywo.
- `render.js` — renderuje klatki w kilku przeglądarkach równolegle i koduje je do MP4.
- `muzyka.py` — generuje ścieżkę ambient (akordy, dzwonki przy scenach, cichy podkład stereo z różnicą 6 Hz).
- `podglad.js` — zrzuty pojedynczych klatek: `node podglad.js <katalog> 10 42 90`.

Schemat mózgu jest uproszczony i nie w skali. Film ma charakter edukacyjny.
