import os, subprocess, wave, hashlib, base64, json
from pathlib import Path

ROOT=Path.cwd()
A=ROOT/'assets'; A.mkdir(exist_ok=True)
S=ROOT/'segments'; S.mkdir(exist_ok=True)
O=ROOT/'output'; O.mkdir(exist_ok=True)

sources={
'sydney':A/'sydney.webm',
'cairo':A/'cairo.webm',
'vendors':A/'vendors.webm',
'aftermath':A/'aftermath.webm',
'candle':A/'candle.webm',
}

scripts=[
"My name is Abdulrahman. I'm Australian. I catch the seven fifteen from Lakemba. I complain about coffee prices like everyone else. But every year, on the fourteenth of August, I wake up before dawn. Because on that date, in twenty thirteen, I was standing in a square in Cairo, and I watched my world end.",
"The square was called Rabaa al Adawiya. For six weeks, tens of thousands of us camped there: students, doctors, grandmothers, kids. We were protesting a military coup. There were tents, food stalls, people reciting poetry at night. It felt like hope.",
"On the fourteenth of August, just after dawn, the bulldozers and armoured vehicles came in from every side.",
"Then the gunfire started. It did not stop for twelve hours. Human Rights Watch counted at least eight hundred and seventeen people killed in that one square, in that one day, and said the true number was likely more than one thousand.",
"They called it one of the largest killings of protesters in a single day in modern history. Likely a crime against humanity. Planned in advance.",
"I ran. My cousin Karim didn't. He was twenty two. He wanted to be a pharmacist. No one, not one official, has ever been held accountable.",
"People think a massacre ends when the shooting stops. It doesn't. Rabaa was the beginning.",
"Today, human rights groups estimate tens of thousands of political prisoners in Egypt: journalists, students, lawyers, people who posted the wrong thing online. Many are held for years without trial.",
"Others simply vanish. Taken from their homes at three in the morning. Families search morgues and police stations for someone the state says it never arrested.",
"And inside those prisons, people die: from torture, from denied medicine, from cells never built for human beings.",
"You'd think that in Australia, I'd be free of it. I'm not, not completely. Egypt refuses to renew passports for people like me. No passport, no identity document, for us and for our children. It's a message: come home and face prison, or cease to exist as an Egyptian.",
"Human rights groups have documented Egyptian embassies monitoring people in their host countries. Back in Egypt, our families get the knock on the door, asked about what we say abroad.",
"Even here. Even now. Some of us look over our shoulder on the way home from Friday prayers.",
"I'm not asking you to fix Egypt. I'm asking you to know. Because the people who died in that square wanted the same thing you already have: a vote that counts, a street you can protest in, a knock on the door that's only ever a neighbour.",
"Thirteen years. No justice. But as long as one witness keeps speaking, Rabaa is not finished. My name is Abdulrahman. I'm Australian. And I remember."
]
durations=[29.7,25.8,9.9,21.3,13.5,15.1,8.9,19.0,14.7,11.4,27.3,16.3,9.8,22.2,16.0]

# Produce a measured scene-by-scene narration track with pauses.
sr=22050
def silence(seconds):
    return b'\x00\x00'*int(sr*seconds)
audio=[silence(5.0)]
for i,(txt,dur) in enumerate(zip(scripts,durations),1):
    wav=A/f'voice_{i:02d}.wav'
    subprocess.run(['espeak','-v','en-gb','-s','135','-p','38','-a','165','-g','4','-w',str(wav),txt],check=True)
    with wave.open(str(wav),'rb') as wf:
        if (wf.getframerate(),wf.getsampwidth(),wf.getnchannels()) != (sr,2,1):
            raise RuntimeError('Unexpected espeak WAV format')
        data=wf.readframes(wf.getnframes())
    audio.append(data)
    audio.append(silence(max(0,dur-len(data)/(2*sr))))
audio.append(silence(8.0))
with wave.open(str(A/'narration.wav'),'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(b''.join(audio))

srt='''1
00:00:05,150 --> 00:00:07,264
My name is Abdulrahman.

2
00:00:07,264 --> 00:00:08,321
I'm Australian.

3
00:00:08,321 --> 00:00:12,020
I catch the seven fifteen from Lakemba.

4
00:00:12,020 --> 00:00:16,248
I complain about coffee prices like everyone else.

5
00:00:16,248 --> 00:00:23,118
But every year, on the fourteenth of August, I wake up before dawn.

6
00:00:23,118 --> 00:00:26,817
Because on that date, in twenty thirteen,

7
00:00:26,817 --> 00:00:34,215
I was standing in a square in Cairo, and I watched my world end.

8
00:00:34,815 --> 00:00:39,123
The square was called Rabaa al Adawiya.

9
00:00:39,123 --> 00:00:47,740
For six weeks, tens of thousands of us camped there: students, doctors, grandmothers, kids.

10
00:00:47,740 --> 00:00:51,433
We were protesting a military coup.

11
00:00:51,433 --> 00:00:57,587
There were tents, food stalls, people reciting poetry at night.

12
00:00:57,587 --> 00:01:00,049
It felt like hope.

13
00:01:00,649 --> 00:01:04,800
On the fourteenth of August, just after dawn,

14
00:01:04,800 --> 00:01:09,989
the bulldozers and armoured vehicles came in from every side.

15
00:01:10,589 --> 00:01:12,557
Then the gunfire started.

16
00:01:12,557 --> 00:01:16,002
It did not stop for twelve hours.

17
00:01:16,002 --> 00:01:23,876
Human Rights Watch counted at least eight hundred and seventeen people killed in that one square,

18
00:01:23,876 --> 00:01:31,258
in that one day, and said the true number was likely more than one thousand.

19
00:01:31,858 --> 00:01:35,986
They called it one of the largest killings

20
00:01:35,986 --> 00:01:40,631
of protesters in a single day in modern history.

21
00:01:40,631 --> 00:01:43,211
Likely a crime against humanity.

22
00:01:43,211 --> 00:01:44,760
Planned in advance.

23
00:01:45,360 --> 00:01:46,475
I ran.

24
00:01:46,475 --> 00:01:48,706
My cousin Karim didn't.

25
00:01:48,706 --> 00:01:50,937
He was twenty two.

26
00:01:50,937 --> 00:01:54,283
He wanted to be a pharmacist.

27
00:01:54,283 --> 00:01:59,861
No one, not one official, has ever been held accountable.

28
00:02:00,461 --> 00:02:05,438
People think a massacre ends when the shooting stops.

29
00:02:05,438 --> 00:02:06,544
It doesn't.

30
00:02:06,544 --> 00:02:08,755
Rabaa was the beginning.

31
00:02:09,355 --> 00:02:17,347
Today, human rights groups estimate tens of thousands of political prisoners in Egypt:

32
00:02:17,347 --> 00:02:23,494
journalists, students, lawyers, people who posted the wrong thing online.

33
00:02:23,494 --> 00:02:27,797
Many are held for years without trial.

34
00:02:28,397 --> 00:02:30,021
Others simply vanish.

35
00:02:30,021 --> 00:02:34,892
Taken from their homes at three in the morning.

36
00:02:34,892 --> 00:02:42,471
Families search morgues and police stations for someone the state says it never arrested.

37
00:02:43,071 --> 00:02:46,661
And inside those prisons, people die:

38
00:02:46,661 --> 00:02:53,841
from torture, from denied medicine, from cells never built for human beings.

39
00:02:54,441 --> 00:02:59,896
You'd think that in Australia, I'd be free of it.

40
00:02:59,896 --> 00:03:02,078
I'm not, not completely.

41
00:03:02,078 --> 00:03:06,987
Egypt refuses to renew passports for people like me.

42
00:03:06,987 --> 00:03:12,986
No passport, no identity document, for us and for our children.

43
00:03:12,986 --> 00:03:17,350
It's a message: come home and face prison,

44
00:03:17,350 --> 00:03:21,168
or cease to exist as an Egyptian.

45
00:03:21,768 --> 00:03:28,574
Human rights groups have documented Egyptian embassies monitoring people in their host countries.

46
00:03:28,574 --> 00:03:34,333
Back in Egypt, our families get the knock on the door,

47
00:03:34,333 --> 00:03:37,474
asked about what we say abroad.

48
00:03:38,074 --> 00:03:39,101
Even here.

49
00:03:39,101 --> 00:03:40,127
Even now.

50
00:03:40,127 --> 00:03:47,310
Some of us look over our shoulder on the way home from Friday prayers.

51
00:03:47,910 --> 00:03:51,120
I'm not asking you to fix Egypt.

52
00:03:51,120 --> 00:03:53,413
I'm asking you to know.

53
00:03:53,413 --> 00:04:00,291
Because the people who died in that square wanted the same thing you already have:

54
00:04:00,291 --> 00:04:09,463
a vote that counts, a street you can protest in, a knock on the door that's only ever a neighbour.

55
00:04:10,063 --> 00:04:11,298
Thirteen years.

56
00:04:11,298 --> 00:04:12,533
No justice.

57
00:04:12,533 --> 00:04:19,943
But as long as one witness keeps speaking, Rabaa is not finished.

58
00:04:19,943 --> 00:04:22,413
My name is Abdulrahman.

59
00:04:22,413 --> 00:04:23,648
I'm Australian.

60
00:04:23,648 --> 00:04:25,501
And I remember.
'''
(A/'subtitles.srt').write_text(srt,encoding='utf-8')

segments=[
('sydney',0,5.0,'SYDNEY — PRESENT DAY',"THE SQUARE I CAN'T FORGET",'cool'),
('sydney',8,durations[0],'SYDNEY — PRESENT DAY','14 AUGUST','cool'),
('sydney',40,durations[1],'SYDNEY — PRESENT DAY','','cool'),
('cairo',0,durations[2],'CAIRO — MEMORY TRANSITION','','warm'),
('vendors',0,durations[3],'ILLUSTRATIVE FOOTAGE — CAIRO, 2012','THE SQUARE WAS ALIVE','warm'),
('aftermath',0,durations[4],'ARCHIVAL FOOTAGE — EGYPT, 16 AUGUST 2013 (AFTERMATH)','','dark'),
('aftermath',11,durations[5],'ARCHIVAL FOOTAGE — EGYPT, 16 AUGUST 2013 (AFTERMATH)','','dark'),
('aftermath',29,durations[6],'ARCHIVAL FOOTAGE — EGYPT, 16 AUGUST 2013 (AFTERMATH)','','dark'),
('cairo',32,durations[7],'ILLUSTRATIVE FOOTAGE — CAIRO','','dark'),
('vendors',63,durations[8],'ILLUSTRATIVE FOOTAGE — CAIRO','','dark'),
('vendors',111,durations[9],'ILLUSTRATIVE FOOTAGE — CAIRO','','dark'),
('cairo',60,durations[10],'ILLUSTRATIVE FOOTAGE — CAIRO','','dark'),
('cairo',84,durations[11],'ILLUSTRATIVE FOOTAGE — CAIRO','','dark'),
('sydney',72,durations[12],'SYDNEY — PRESENT DAY','','cool'),
('sydney',98,durations[13],'SYDNEY HARBOUR — DAWN',"I'M ASKING YOU TO KNOW",'cool'),
('candle',0,durations[14],'MEMORIAL','AND I REMEMBER','dark'),
('candle',18,8.0,'14 AUGUST 2013','#REMEMBERRABAA','dark'),
]

def run(cmd):
    print('+',' '.join(map(str,cmd)),flush=True)
    subprocess.run([str(x) for x in cmd],check=True)

font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
for idx,(key,start,dur,label,title,grade) in enumerate(segments):
    label_file=A/f'label_{idx}.txt'; label_file.write_text(label,encoding='utf-8')
    title_file=A/f'title_{idx}.txt'; title_file.write_text(title,encoding='utf-8')
    eq={'cool':'eq=saturation=0.72:contrast=1.08:brightness=-0.035','warm':'eq=saturation=0.78:contrast=1.06:brightness=-0.02','dark':'eq=saturation=0.48:contrast=1.18:brightness=-0.10'}[grade]
    fadeout=max(0.0,dur-0.45)
    vf=(
      'scale=960:540:force_original_aspect_ratio=increase,crop=960:540,fps=24,'+eq+','
      'drawbox=x=0:y=0:w=iw:h=54:color=black@0.46:t=fill,'
      f'drawtext=fontfile={font}:textfile={label_file}:fontcolor=white:fontsize=18:x=34:y=17,'
      f'drawtext=fontfile={bold}:textfile={title_file}:fontcolor=white:fontsize=43:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.42:boxborderw=18,'
      f'fade=t=in:st=0:d=0.35,fade=t=out:st={fadeout:.3f}:d=0.45'
    )
    out=S/f'{idx:03d}.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-stream_loop','-1','-ss',start,'-i',sources[key],'-t',dur,'-vf',vf,'-an','-c:v','libx264','-preset','ultrafast','-crf','27','-pix_fmt','yuv420p',out])

concat=A/'concat.txt'
concat.write_text(''.join(f"file '{(S/f'{i:03d}.mp4').as_posix()}'\n" for i in range(len(segments))),encoding='utf-8')
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',concat,'-c','copy',A/'visuals.mp4'])
style='FontName=DejaVu Sans,FontSize=19,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101010,BackColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=26,Alignment=2'
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',A/'visuals.mp4','-i',A/'narration.wav','-vf',f"subtitles={A/'subtitles.srt'}:force_style='{style}'",'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','27','-c:a','aac','-b:a','96k','-ar','44100','-shortest','-movflags','+faststart',O/'The_Square_I_Cant_Forget_ACTUAL_VIDEO.mp4'])

video=O/'The_Square_I_Cant_Forget_ACTUAL_VIDEO.mp4'
raw=video.read_bytes(); sha=hashlib.sha256(raw).hexdigest(); b64=base64.b64encode(raw).decode('ascii')
chunk_size=400000
chunks=[b64[i:i+chunk_size] for i in range(0,len(b64),chunk_size)]
for i,c in enumerate(chunks):
    (O/f'chunk_{i:03d}.txt').write_text(c,encoding='ascii')
video.unlink()
manifest={'filename':'The_Square_I_Cant_Forget_ACTUAL_VIDEO.mp4','sha256':sha,'chunks':len(chunks),'chunk_size':chunk_size}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(O/'CREDITS.txt').write_text('''MOVING-FOOTAGE SOURCES
Sydney Harbour time-lapse — SIB technology — CC BY 3.0.
Cairo Wakes Up — Wex Major 98 — CC BY-SA 4.0.
Street Vendors of Cairo — Wex Major 98 — CC BY-SA 4.0.
Before Friday of Rage in Egypt, 16 Aug 2013 — Voice of America — Public Domain (US).
White candle video — Jahobr — CC0 1.0.

Important: the 16 August 2013 clip is labelled as aftermath and is not represented as footage of the 14 August Rabaa dispersal.
This derivative is provided under CC BY-SA 4.0 where required.
''',encoding='utf-8')
print(manifest)
