from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import speech_recognition as sr
from flask import Flask, render_template, request
# To get timestamp
import pvleopard
# To get the audio file
from pydub import AudioSegment
# To play audio file
from pydub.playback import play
import os
app = Flask(__name__)


app.config['uploaded_file_name']=""
app.config['full_path']=""

class Transcribe():
    def doTranscribe(self,filename):
        file_path="D:/SEM-VI/sampleMiniproject"
        file_name=filename
        app.config['full_path']=os.path.join(file_path,file_name)
        leopard = pvleopard.create(
                access_key='EbpK3AYedSZLrHX7QuTa+13vH0W29fR8LccMy11cFcORav9NpDy7Xw==')
        return leopard.process_file(app.config['full_path'])


@app.route("/upload")
def upload_file():
   return render_template("upload.html")


@app.route("/uploader",endpoint='save_file',methods = ["GET", "POST"])
def save_file():
   if request.method == "POST":
      f = request.files["file"]
      f.save(secure_filename(f.filename))
      app.config['uploaded_file_name']=f.filename

    #   TransObj=Transcribe(f.filename)
    #   transcript=TransObj.transcirption
    #   print(transcript)
      callMethod=Transcribe()
      transcript,wordByword=callMethod.doTranscribe(f.filename)
    #   print(transcript)
      return render_template("transcript.html", transcript=transcript)
   
@app.route('/search', methods=['GET', 'POST'])
def searching():
    if request.method == 'POST':
        textToBeSearched = request.form.get('wordToBeSearched')

        callMethod=Transcribe()
        transcript,wordByword=callMethod.doTranscribe(app.config['uploaded_file_name'])
        
        totalWordCount = len(wordByword)
        countInLoop = 0
        endSec = 0
        startSec=0
        if_block_executed = False
        # searching for the given word
        for word in wordByword:
            countInLoop += 1
            if (word.word == textToBeSearched and not if_block_executed):  # getting the starting time of the word
                startSec = word.start_sec
                if_block_executed = True

            if (countInLoop == totalWordCount):  # collecting the total length of the audio file
                endSec = word.end_sec
                break
                
        #     print("{word=\"%s\" start_sec=%.2f end_sec=%.2f confidence=%.2f}"
        #   % (word.word, word.start_sec, word.end_sec, word.confidence))
   
       
        StartTime =startSec*1000
        EndTime =endSec*1000
        print(app.config['full_path'])
        audio = AudioSegment.from_file(app.config['full_path'],format="wav")
        extraction = audio[StartTime:EndTime]
        play(extraction)
        # extraction.export(out_f="new.wav",format="wav")

    return render_template("final.html",text=textToBeSearched,time=startSec)

if __name__ == "__main__":
   app.run(debug = True)