import tweepy
import os
import ffmpeg
import time
import speech_recognition as sr
from PIL import Image, ImageFont, ImageDraw 
from google_trans_new import google_translator

translator = google_translator()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

################################################################################################################################

def text2png(text, fullpath, color = "#000", bgcolor = "#FFF", fontfullpath = None, fontsize = 13, leftpadding = 3, rightpadding = 3, width = 200):
    REPLACEMENT_CHARACTER = u'\uFFFD'
    NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '

    font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(fontfullpath, fontsize)
    text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

    lines = []
    line = u""

    for word in text.split():
        print(word)
        if word == REPLACEMENT_CHARACTER: #give a blank line
            lines.append( line[1:] ) #slice the white space in the begining of the line
            line = u""
            lines.append( u"" ) #the blank line
        elif font.getsize( line + ' ' + word )[0] <= (width - rightpadding - leftpadding):
            line += ' ' + word
        else: #start a new line
            lines.append( line[1:] ) #slice the white space in the begining of the line
            line = u""

			#TODO: handle too long words at this point
            line += ' ' + word #for now, assume no word alone can exceed the line width

    if len(line) != 0:
        lines.append( line[1:] ) #add the last line

    line_height = font.getsize(text)[1]
    img_height = line_height * (len(lines) + 1)

    img = Image.new("RGBA", (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)

    y = 0
    for line in lines:
        draw.text( (leftpadding, y), line, color, font=font)
        y += line_height

    img.save(fullpath)
    
#################################################################################################################################
    
def transcribe_original(tweet_ids, tweet, tweet_text, lang_codes, tweet_embedded):
    if tweet_text[-1] in lang_codes:
        stream = ffmpeg.input(tweet_embedded.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream) 
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
        os.remove(r'.\video.mp4')
                    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = tweet_text[-1])
        os.remove(r'.\audio.wav')
        
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')

        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        os.remove(r'.\text.png')
        tweet_ids.append(tweet.id)
                        
    else:
        stream = ffmpeg.input(tweet_embedded.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream)  
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
        os.remove(r'.\video.mp4')
                    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
        os.remove(r'.\audio.wav')
                    
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')
                    
        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        os.remove(r'.\text.png')
        tweet_ids.append(tweet.id)

#################################################################################################################################        
        
def transcribe(tweet_ids, tweet, tweet_text, lang_codes):
    if tweet_text[-2] in lang_codes:
        stream = ffmpeg.input(tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream)  
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
        os.remove(r'.\video.mp4')
    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = tweet_text[-2])
        os.remove(r'.\audio.wav')
        
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')
    
        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        os.remove(r'.\text.png')
        tweet_ids.append(tweet.id)
        
    else:
        stream = ffmpeg.input(tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream)  
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
        os.remove(r'.\video.mp4')
    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
        os.remove(r'.\audio.wav')
    
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')
    
        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        os.remove(r'.\text.png')
        tweet_ids.append(tweet.id)
        
################################################################################################################################

def mention_reply(api):
    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        lang_codes = ['pt-BR', 'en-GB', 'en-US', 'fr-FR', 'fr-CA', 'gl-ES', 'de-DE', 'de-CH', 'it-IT', 'ja-JP', 'ko-KR', 'pt-PT', 'ru-RU', 'es-AR', 'es-BO', 'vi-VN']
        raw_tweet_text = tweet.text
        tweet_text = raw_tweet_text.split()
        tweet_ids = []
        print(tweet.entities)
        
        if tweet in tweet_ids:
            print(tweet_text)
            pass
        
        else:
            if len(raw_tweet_text) < 140:
                tweet.extended_entities
                print(tweet_text)
                transcribe(tweet_ids, tweet, tweet_text, lang_codes)
                
                
            else:
                if tweet.in_reply_to_screen_name == "closedcapbot":
                    print(tweet_text)
                    tweet_ids.append(tweet.id)
                    pass
                
                else:
                    try:
                        tweet_embedded = api.get_status(tweet.in_reply_to_status_id)
                        tweet_embedded.extended_entities
                        print(tweet_text)
                        if 'media' in tweet_embedded.entities: 
                            if tweet_text[-1] in lang_codes:
                                print(tweet_text)
                                lang = tweet_text[-1].split('-')
                                text = translator.translate('There is no video in this tweet', lang_src='en', lang_tgt=lang[0])
                                api.update_status(status='@'+ tweet.user.screen_name + '\n' + text, in_reply_to_status_id = tweet.id)
                                tweet_ids.append(tweet.id)
                            else:
                                print(tweet_text)
                                api.update_status(status='@'+ tweet.user.screen_name + '\n' + 'There is no video in this tweet', in_reply_to_status_id = tweet.id)
                                tweet_ids.append(tweet.id)
                        else:
                            tweet_embedded = api.get_status(tweet.in_reply_to_status_id, tweet_mode = 'extended')
                            print(tweet_text)
                            transcribe_original(tweet_ids, tweet, tweet_text, lang_codes, tweet_embedded)
                                 
                    except AttributeError:
                        if 'media' in tweet_embedded.entities: 
                            if tweet_text[-1] in lang_codes:
                                print(tweet_text)
                                lang = tweet_text[-1].split('-')
                                text = translator.translate('There is no video in this tweet', lang_src='en', lang_tgt=lang[0])
                                api.update_status(status='@'+ tweet.user.screen_name + '\n' + text, in_reply_to_status_id = tweet.id)
                                tweet_ids.append(tweet.id)
                            else:
                                print(tweet_text)
                                api.update_status(status='@'+ tweet.user.screen_name + '\n' + 'There is no video in this tweet', in_reply_to_status_id = tweet.id)
                                tweet_ids.append(tweet.id)
                        else:
                            tweet_embedded = api.get_status(tweet.in_reply_to_status_id, tweet_mode = 'extended')
                            print(tweet_text)
                            transcribe_original(tweet_ids, tweet, tweet_text, lang_codes, tweet_embedded)
            
            
while True:
    mention_reply(api)
    time.sleep(1)