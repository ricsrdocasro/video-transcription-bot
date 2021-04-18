import tweepy
import os
import ffmpeg
import time
import speech_recognition as sr
from PIL import Image, ImageFont, ImageDraw 
from google_trans_new import google_translator

translator = google_translator()
auth = tweepy.OAuthHandler("0yIf85cbzDjVwCcGqfVHV3gC9", "DB82MD634wffg63vjY2PSz09BO9so8WQwHoz3CJ7I0FLQr9qB3")
auth.set_access_token("1143989662970781696-E5ZWpo7FNPaoKn8Lqn0BS07sh5C4DF", "dSooCIiSOe7ayJdBP1l9ioCXpgHHqxObX9A0CxWKTVXGd")
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
    verify_path()
    lang = verify_lang(tweet_text, lang_codes)
    if lang in lang_codes:
        stream = ffmpeg.input(tweet_embedded.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream) 
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
                    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = lang)
        
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')

        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        #tweet_ids.append(tweet.id)
                        
    else:
        stream = ffmpeg.input(tweet_embedded.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream)  
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
                    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
                    
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')
                    
        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        #tweet_ids.append(tweet.id)

################################################################################################################################# 

def verify_path():
    files = [r'.\audio.wav', r'.\text.png', r'.\video.mp4']
    for x in files:
        if os.path.exists(x):
            os.remove(x)
        else:
            None
            
#################################################################################################################################
            
def transcribe(tweet_ids, tweet, tweet_text, lang_codes):
    verify_path()
    lang = verify_lang(tweet_text, lang_codes)
    print(lang)
    if lang in lang_codes:
        stream = ffmpeg.input(tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream)  
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language = lang)
        
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')
    
        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        #tweet_ids.append(tweet.id)
        
    else:
        stream = ffmpeg.input(tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"])
        stream = ffmpeg.output(stream, 'video.mp4')
        ffmpeg.run(stream)  
        audio = ffmpeg.input("video.mp4") 
        audio = ffmpeg.output(audio, "audio.wav")
        ffmpeg.run(audio)
    
        r = sr.Recognizer()
        filename = os.path.join(r'C:\Users\Darth\OneDrive\Área de Trabalho\programação\Python\PythonFundamentos\Cap04\Notebooks\audio.wav')
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
    
        text2png(text, 'text.png', fontfullpath = '/Windows/Fonts/Arial.ttf')
    
        api.update_with_media('text.png', status='@' + tweet.user.screen_name, in_reply_to_status_id = tweet.id)
        #tweet_ids.append(tweet.id)
        
################################################################################################################################
        
def error_msg(tweet_text, lang_codes, tweet_ids, tweet):
    lang = verify_lang(tweet_text, lang_codes)
    if lang in lang_codes:
        print(tweet_text)
        lang = lang.split('-')
        text = translator.translate('There is no video in this tweet or no speech', lang_src='en', lang_tgt=lang[0])
        api.update_status(status='@'+ tweet.user.screen_name + '\n' + text, in_reply_to_status_id = tweet.id)
        tweet_ids.append(tweet.id)
    else:
        print(tweet_text)
        api.update_status(status='@'+ tweet.user.screen_name + '\n' + 'There is no video in this tweet or no speech', in_reply_to_status_id = tweet.id)
        tweet_ids.append(tweet.id)
        
################################################################################################################################

def verify_lang(tweet_text, lang_codes):
    lang = list(set(lang_codes).intersection(set(tweet_text)))
    if lang == []:
        return ''
    else:
        lang = lang[0]
        return lang
        print(lang)
        
################################################################################################################################

def mention_reply(api):
    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        tweet = api.get_status(tweet.id, tweet_mode = 'extended')
        #print(tweet.extended_entities)
        lang_codes = ['pt-BR', 'en-GB', 'en-US', 'fr-FR', 'fr-CA', 'gl-ES', 'de-DE', 'de-CH', 'it-IT', 'ja-JP', 'ko-KR', 'pt-PT', 'ru-RU', 'es-AR', 'es-BO', 'vi-VN']
        raw_tweet_text = tweet.full_text
        tweet_text = raw_tweet_text.split()
        tweet_ids = []
        #print(tweet.entities)
        lang = ''
        
        if tweet.id in tweet_ids:
            #print(tweet_text)
            continue
        
        else:
            if 'media' in tweet.entities:
                tweet.extended_entities
                print(tweet_text)
                tweet_ids.append(tweet.id)
                transcribe(tweet_ids, tweet, tweet_text, lang_codes)
                    
            else: 
                try:
                    tweet_embedded = api.get_status(tweet.in_reply_to_status_id, tweet_mode = 'extended')
                    if tweet.in_reply_to_screen_name == "closedcapbot" or tweet.in_reply_to_screen_name == "ricardopaula26":
                        #print(tweet_text)
                        tweet_ids.append(tweet.id)
                        continue
                    
                    else:
                        try:
                            tweet_embedded.extended_entities
                            tweet_ids.append(tweet.id)
                            transcribe_original(tweet_ids, tweet, tweet_text, lang_codes, tweet_embedded)

                        except:
                            #error_msg(tweet_text, lang_codes, tweet_ids, tweet)
                            tweet_ids.append(tweet.id)
                            continue
                                    
                except:
                    #error_msg(tweet_text, lang_codes, tweet_ids, tweet)
                    tweet_ids.append(tweet.id)
                    continue
            
            
while True:
    mention_reply(api)