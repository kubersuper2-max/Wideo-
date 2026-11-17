"""Generuje głos lektora (Piper, polski) i plik timeline.js z czasami scen i napisów.
Użycie: python3 lektor.py <katalog_z_modelami> <wyjście.wav> <timeline.js>"""
import json, sys, wave
from pathlib import Path
import numpy as np
from piper import PiperVoice, SynthesisConfig

models, out_wav, out_js = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
cfg = json.load(open(Path(__file__).with_name('narracja.json'), encoding='utf-8'))
v = cfg['glos']
voice = PiperVoice.load(str(next(models.glob(f'**/pl_PL-{v}-medium.onnx'))))
syn = SynthesisConfig(length_scale=cfg['tempo'], noise_scale=0.6, noise_w_scale=0.8)
SR = voice.config.sample_rate

def synth(text):
    pcm = b''.join(c.audio_int16_bytes for c in voice.synthesize(text, syn_config=syn))
    a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    loud = np.where(np.abs(a) > 0.02)[0]          # przytnij ciszę na brzegach
    a = a[max(0, loud[0] - int(0.03 * SR)): loud[-1] + int(0.08 * SR)]
    return a

LEAD, GAP_COMMA, GAP_SENT, GAP_SCENE, TAIL = 1.6, 0.18, 0.4, 0.9, 3.8
audio, t = [np.zeros(int(LEAD * SR))], LEAD
scenes, chunks = [], []
for si, sc in enumerate(cfg['sceny']):
    s_start = t if si else 0.0
    for fi, txt in enumerate(sc['fragmenty']):
        a = synth(txt)
        chunks.append({'scene': sc['id'], 'text': txt, 'start': round(t, 3), 'end': round(t + len(a) / SR, 3)})
        audio.append(a); t += len(a) / SR
        last = fi == len(sc['fragmenty']) - 1
        gap = (GAP_SCENE if si < len(cfg['sceny']) - 1 else TAIL) if last else (GAP_COMMA if txt.endswith(',') else GAP_SENT)
        audio.append(np.zeros(int(gap * SR))); t += gap
    scenes.append({'id': sc['id'], 'title': sc['naglowek'], 'label': sc.get('etykieta', ''), 'start': round(s_start, 3)})
for i, s in enumerate(scenes):
    s['end'] = scenes[i + 1]['start'] if i + 1 < len(scenes) else round(t, 3)
# sceny zaczynają się chwilę przed pierwszym słowem (płynne przejście)
for s in scenes[1:]:
    s['start'] = round(s['start'] - 0.35, 3)
for i in range(len(scenes) - 1):
    scenes[i]['end'] = scenes[i + 1]['start']

a = np.concatenate(audio)
a = a / np.max(np.abs(a)) * 0.9
with wave.open(out_wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((a * 32767).astype(np.int16).tobytes())
tl = {'duration': round(t, 3), 'scenes': scenes, 'chunks': chunks}
Path(out_js).write_text('window.TIMELINE = ' + json.dumps(tl, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
print(f'czas: {t:.1f} s')
for s in scenes: print(f"  {s['id']:<11} {s["start"]:6.2f} - {s["end"]:6.2f}")
