import wave, struct, math, os

def save_tone(path, duration, freq_start, freq_end, sample_rate=22050):
    n = int(sample_rate * duration)
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(sample_rate)
        for i in range(n):
            t = i / sample_rate
            f = freq_start + (freq_end - freq_start) * (t / duration)
            v = int(128 + 100 * math.sin(2 * math.pi * f * t))
            w.writeframes(struct.pack('B', max(0, min(255, v))))

def note_freq(n):
    return 440.0 * (2 ** ((n - 69) / 12.0))

def save_bgm(path, sample_rate=22050):
    def square(t, freq):
        return 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0

    melody = [
        (72, 0.2), (76, 0.2), (79, 0.2), (84, 0.4),
        (79, 0.2), (76, 0.2), (72, 0.2), (76, 0.2),
        (79, 0.2), (84, 0.2), (86, 0.2), (84, 0.4),
    ]

    samples = []
    t = 0.0
    for note, dur in melody:
        freq = note_freq(note)
        n = int(sample_rate * dur)
        for i in range(n):
            sample = square(t, freq) * 0.2
            samples.append(sample)
            t += 1.0 / sample_rate

    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        for s in samples:
            w.writeframes(struct.pack('<h', int(s * 32767)))

save_tone('jump.wav', 0.15, 440, 880)
save_tone('coin.wav', 0.1, 1200, 2000)
save_tone('stomp.wav', 0.08, 200, 100)
save_tone('hurt.wav', 0.3, 400, 100)
save_tone('win.wav', 0.5, 523, 1047)

# 水管音效 - 短促降调啵声
def save_pipe(path, sample_rate=22050):
    n = int(sample_rate * 0.25)
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(sample_rate)
        for i in range(n):
            t = i / sample_rate
            f = 400 - t * 800
            v = int(128 + 80 * (1 - t / 0.25) * (1 if int(t * f) % 2 else -1))
            w.writeframes(struct.pack('B', max(0, min(255, v))))

save_pipe('pipe.wav')
save_bgm('bgm.wav', 22050)
print("音效生成完成")
