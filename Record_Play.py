import pyaudio
import wave
import time
from pydub import AudioSegment

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100  # 采样率


def mixFiles(file1_path,file2_path,mix_path):
    toMix=[file1_path,file2_path]
    currentMixes=len(toMix)
    maxLen = 0
    for file in toMix: # loop to find the longest file length
        tempSeg = AudioSegment.from_file(file)
        tempSeg = AudioSegment.frame_count(tempSeg)
        maxLen = max(tempSeg,maxLen)
    mixed = AudioSegment.silent(1000*maxLen/44100) # conver to mS
    for file in toMix:
        temp = AudioSegment.from_file(file)
        mixed = mixed.overlay(temp)
        # os.remove(file) # delete original file after being mixed
    mixed.export(mix_path.format(currentMixes+1), format="wav")

def record_play(Play_Path,Record_Path,RECORD_SECONDS=-1,countdown=3):#只能使用44100以下的播放源,可以设定录制和播放的时间（默认无）,和倒计时（默认3秒倒计时）
    #########播放设置
    # 只读方式打开wav文件
    wf_write = wave.open(Play_Path, 'rb')
    p_write = pyaudio.PyAudio()
    # 打开数据流
    stream_write = p_write.open(format=p_write.get_format_from_width(wf_write.getsampwidth()),
                    channels=wf_write.getnchannels(),
                    rate=wf_write.getframerate(),
                    output=True)
    ##########播放设置
    ##########录音设置
    WAVE_OUTPUT_FILENAME = Record_Path
    p_read = pyaudio.PyAudio()
    stream_read = p_read.open(format=FORMAT,
                    channels=CHANNELS,#通道数
                    rate=RATE,#指定速率（单位Hz）
                    input=True,
                    frames_per_buffer=CHUNK)#帧 缓冲
    frames = []
    ##########录音设置


    #倒计时
    count = 0
    while (count <= countdown):
        count_now = countdown - count
        print(count_now)
        time.sleep(1)  # sleep 1 second
        count += 1


    # 读取数据
    data_write = wf_write.readframes(CHUNK)
    print("*Begin Recording and Playing")
    # 播放

    if RECORD_SECONDS<0:
        while len(data_write)>0:
            stream_write.write(data_write)
            data_write = wf_write.readframes(CHUNK)
            data_read = stream_read.read(CHUNK)
            frames.append(data_read)
    else:
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            stream_write.write(data_write)
            data_write = wf_write.readframes(CHUNK)
            data_read = stream_read.read(CHUNK)
            frames.append(data_read)
            if len(data_write) <= 0:break
    # 停止数据流
    print("*End")
    stream_write.stop_stream()
    stream_write.close()
    stream_read.stop_stream()
    stream_read.close()
    p_read.terminate()
    # 关闭 PyAudio
    p_write.terminate()

    wf_read = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf_read.setnchannels(CHANNELS)
    wf_read.setsampwidth(p_read.get_sample_size(FORMAT))
    wf_read.setframerate(RATE)
    wf_read.writeframes(b''.join(frames))
    wf_read.close()

def record(Record_Path,RECORD_SECONDS):
    WAVE_OUTPUT_FILENAME = Record_Path

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,  # 通道数
                    rate=RATE,  # 指定速率（单位Hz）
                    input=True,
                    frames_per_buffer=CHUNK)  # 帧 缓冲

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play(Play_Path,PLAY_SECONDS=-1):
    wf = wave.open(Play_Path, 'rb')  # (sys.argv[1], 'rb')
    p = pyaudio.PyAudio()

    # 打开数据流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 读取数据
    data = wf.readframes(CHUNK)
    # 播放
    if PLAY_SECONDS>0:
        for i in range(0, int(RATE / CHUNK * PLAY_SECONDS)):
            stream.write(data)
            data = wf.readframes(CHUNK)
            if len(data)>0:break
    else:
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭 PyAudio
    p.terminate()
