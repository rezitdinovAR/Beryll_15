from src.ASR.cons.ASR import ASR

asr = ASR()

result = asr.transcribation('1711634944-12-3-2b3739383732323137383739.mp3')

print(type(result))
print(result)
