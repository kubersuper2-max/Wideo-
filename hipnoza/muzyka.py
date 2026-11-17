"""Generuje ambientową ścieżkę dźwiękową do filmu (numpy, bez zewnętrznych sampli)."""
import sys, wave
import numpy as np

SR, DUR = 44100, 148.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(5)
L = np.zeros(N); Rr = np.zeros(N)

def hz(note):  # MIDI -> Hz
    return 440.0 * 2 ** ((note - 69) / 12)

# --- pad: progresja akordów (Am9 – Fmaj7 – Cmaj7 – G6), 8 s na akord, przenikanie ---
chords = [[45, 57, 60, 64, 71], [41, 57, 60, 64, 69], [48, 55, 59, 64, 67], [43, 55, 59, 62, 64]]
seg = 8.0
for i in range(int(DUR / seg) + 1):
    ch = chords[i % 4]
    s0, s1 = i * seg - 2.0, (i + 1) * seg + 2.0
    a, b = max(0, int(s0 * SR)), min(N, int(s1 * SR))
    if a >= b: continue
    tt = t[a:b]
    k = (tt - s0) / (s1 - s0)
    env = np.sin(np.pi * np.clip(k, 0, 1)) ** 1.5
    for j, n in enumerate(ch):
        f = hz(n)
        amp = 0.05 if n < 50 else 0.032
        for det, pan in ((-0.6, 0.75), (0.6, 0.25)):
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2 * np.pi * (f + det) * tt + ph) + 0.25 * np.sin(2 * np.pi * 2 * (f + det) * tt + ph)
            trem = 1 + 0.15 * np.sin(2 * np.pi * (0.07 + 0.03 * j) * tt + j)
            L[a:b] += amp * env * w * trem * pan
            Rr[a:b] += amp * env * w * trem * (1 - pan)

# --- podkład „theta”: 110 Hz / 116 Hz w kanałach (różnica 6 Hz) od indukcji ---
fade = np.clip((t - 20) / 6, 0, 1) * np.clip((140 - t) / 4, 0, 1)
L += 0.035 * fade * np.sin(2 * np.pi * 110 * t)
Rr += 0.035 * fade * np.sin(2 * np.pi * 116 * t)

# --- delikatny szum „oddechu” ---
noise = rng.standard_normal(N)
for _ in range(3):  # prosty filtr dolnoprzepustowy
    noise = np.convolve(noise, np.ones(40) / 40, mode='same')
breath = 0.5 + 0.5 * np.sin(2 * np.pi * t / 8.0 - np.pi / 2)
L += 0.25 * noise * breath * 0.12
Rr += 0.25 * np.roll(noise, 900) * breath * 0.12

# --- dzwonki na początku scen ---
for st, note in [(0.3, 76), (8, 81), (20, 76), (30, 79), (46, 83), (62, 81), (78, 76), (90, 79), (102, 84), (114, 81), (126, 76), (140, 81)]:
    a = int(st * SR); b = min(N, a + int(5 * SR))
    tt = t[a:b] - st
    f = hz(note)
    env = np.exp(-tt * 1.1) * np.clip(tt / 0.005, 0, 1)
    w = np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 2) + 0.2 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 4)
    L[a:b] += 0.06 * env * w
    Rr[a:b] += 0.06 * env * np.roll(w, 300)

# --- pogłos (splot z zanikającym szumem, FFT) ---
def reverb(x, seed):
    ir_len = int(3.0 * SR)
    r = np.random.default_rng(seed).standard_normal(ir_len) * np.exp(-np.arange(ir_len) / SR * 2.2)
    r[0] = 0
    n = 1 << int(np.ceil(np.log2(len(x) + ir_len)))
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(r, n), n)[:len(x)]
    return y / np.max(np.abs(y)) * np.max(np.abs(x))
Lw, Rw = reverb(L, 1), reverb(Rr, 2)
L = 0.6 * L + 0.55 * Lw; Rr = 0.6 * Rr + 0.55 * Rw

# --- fade in/out, normalizacja ---
master = np.clip(t / 3, 0, 1) * np.clip((DUR - t) / 4, 0, 1)
out = np.stack([L * master, Rr * master], axis=1)
out = out / np.max(np.abs(out)) * 0.85
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', sys.argv[1])
