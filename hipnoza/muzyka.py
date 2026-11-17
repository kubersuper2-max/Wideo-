"""Ścieżka dźwiękowa: ambient + przejścia + lektor (ze ściszaniem muzyki pod głosem).
Użycie: python3 muzyka.py <timeline.js> <lektor_44k.wav> <wyjście.wav>"""
import json, re, sys, wave
import numpy as np

SR = 44100
tl = json.loads(re.search(r'=\s*(\{.*\})\s*;', open(sys.argv[1], encoding='utf-8').read(), re.S).group(1))
DUR = tl['duration']; N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)
hz = lambda n: 440.0 * 2 ** ((n - 69) / 12)

# pad: Am9 - Fmaj7 - Cmaj7 - G6, 6 s na akord
chords = [[45, 57, 60, 64, 71], [41, 57, 60, 64, 69], [48, 55, 59, 64, 67], [43, 55, 59, 62, 64]]
seg = 6.0
for i in range(int(DUR / seg) + 1):
    s0, s1 = i * seg - 1.5, (i + 1) * seg + 1.5
    a, b = max(0, int(s0 * SR)), min(N, int(s1 * SR))
    if a >= b: continue
    tt = t[a:b]; env = np.sin(np.pi * np.clip((tt - s0) / (s1 - s0), 0, 1)) ** 1.5
    for j, n in enumerate(chords[i % 4]):
        f, amp = hz(n), (0.05 if n < 50 else 0.03)
        for det, pan in ((-0.6, 0.75), (0.6, 0.25)):
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2 * np.pi * (f + det) * tt + ph) + 0.25 * np.sin(4 * np.pi * (f + det) * tt + ph)
            w *= env * amp * (1 + 0.15 * np.sin(2 * np.pi * (0.07 + 0.03 * j) * tt + j))
            L[a:b] += w * pan; R[a:b] += w * (1 - pan)
# niski puls (bicie serca) w intro, zwalnia
for bt in np.arange(0.4, 6, 0.75):
    a = int(bt * SR); tt = t[a:a + int(0.4 * SR)] - bt
    k = np.exp(-tt * 14) * np.sin(2 * np.pi * 55 * tt) * 0.25
    L[a:a + len(k)] += k; R[a:a + len(k)] += k
# podkład theta 110/116 Hz
fade = np.clip((t - 6) / 4, 0, 1) * np.clip((DUR - 2 - t) / 3, 0, 1)
L += 0.03 * fade * np.sin(2 * np.pi * 110 * t); R += 0.03 * fade * np.sin(2 * np.pi * 116 * t)
# "whoosh" + dzwonek przy przejściach
noise = rng.standard_normal(N)
for s in tl['scenes'][1:]:
    st = s['start']
    a, b = int((st - 0.6) * SR), min(N, int((st + 0.7) * SR))
    tt = (t[a:b] - (st - 0.6)) / 1.3
    env = np.sin(np.pi * tt) ** 2
    nz = noise[a:b].copy()
    k = int(4 + 40 * 0.5)  # proste wygładzenie = lżejszy szum
    nz = np.convolve(nz, np.ones(k) / k, mode='same')
    L[a:b] += 0.35 * env * nz * (1 - tt); R[a:b] += 0.35 * env * nz * tt
for st, note in [(0.2, 76)] + [(s['start'] + 0.1, [81, 76, 79, 83, 81, 79, 76][i % 7]) for i, s in enumerate(tl['scenes'][1:])] + [(DUR - 3.0, 81)]:
    a = int(st * SR); b = min(N, a + int(4 * SR)); tt = t[a:b] - st; f = hz(note)
    env = np.exp(-tt * 1.3) * np.clip(tt / 0.005, 0, 1)
    w = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 2)) * env * 0.05
    L[a:b] += w; R[a:b] += np.roll(w, 300)

def reverb(x, seed):
    n_ir = int(2.5 * SR)
    r = np.random.default_rng(seed).standard_normal(n_ir) * np.exp(-np.arange(n_ir) / SR * 2.4); r[0] = 0
    n = 1 << int(np.ceil(np.log2(len(x) + n_ir)))
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(r, n), n)[:len(x)]
    return y / np.max(np.abs(y)) * np.max(np.abs(x))
L = 0.6 * L + 0.55 * reverb(L, 1); R = 0.6 * R + 0.55 * reverb(R, 2)
music = np.stack([L, R], 1)
music /= np.max(np.abs(music))

# lektor
with wave.open(sys.argv[2]) as w:
    assert w.getframerate() == SR
    v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2: v = v.reshape(-1, 2).mean(1)
v = np.pad(v, (0, max(0, N - len(v))))[:N]
# ściszanie muzyki pod głosem (obwiednia głosu, wygładzona)
env = np.abs(v); k = int(0.25 * SR)
env = np.convolve(env, np.ones(k) / k, mode='same'); env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = 1 - 0.55 * env
master = np.clip(t / 1.5, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
mixd = music * (0.42 * duck * master)[:, None] + v[:, None] * 0.95
mixd /= max(1.0, np.max(np.abs(mixd)) / 0.95)
with wave.open(sys.argv[3], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mixd * 32767).astype(np.int16).tobytes())
print('ok', sys.argv[3], f'{DUR:.1f} s')
