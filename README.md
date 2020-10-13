# Record_Play
Self integrated library for recording and playing

- import pyaudio
- import wave
- import time
- from pydub import AudioSegment
--------------------------------

### Record\_Play.mixFiles(file1\_path,file2\_path,mix\_path='mix\_audio')： ###

- 说明：混音
- 只需输入两个音频的路径即可轻松达成混音
- 默认将混合后的音频存储到当前库所在的文件夹，并命名mix_audio
- 需要库pydub
- 等待后期实现同步功能

### record\_play(Play\_Path,Record_Path,RECORD\_SECONDS=-1,countdown=3)： ###

- 说明：播放并录音
- Play_Path：播放Play_Path的音频文件
- Record_Path：录音存储到Record_Path中，
- RECORD_SECONDS：可以设置录制时间，default：不设置，将播放完整个音频
- countdown：录音倒计时，default：3秒

### record(Record\_Path,RECORD\_SECONDS)： ###

- 说明：单录音
- Record_Path：录音存储路径
- RECORD_SECONDS：录制时间

### play(Play\_Path,PLAY\_SECONDS=-1)： ###

- 说明：单播放
- Play_Path:单播放
- PLAY_SECONDS:播放时间
