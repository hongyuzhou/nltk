# coding=utf8

import pynlpir
from pynlpir import nlpir

# from settings import JAVA_DIR
# import jnius_config
# classpath = str(JAVA_DIR) + "/FudanNLP/lib/trove.jar:"
# classpath = classpath + str(JAVA_DIR) + "/FudanNLP/lib/lucene-queryparser-4.0.0.jar:"
# classpath = classpath + str(JAVA_DIR) + "/FudanNLP/lib/lucene-core-4.0.0.jar:"
# classpath = classpath + str(JAVA_DIR) + "/FudanNLP/lib/commons-cli-1.2.jar:"
# classpath = classpath + str(JAVA_DIR) + "/FudanNLP/fudannlp.jar:"
# classpath = classpath + str(JAVA_DIR) + "/bot/bot_handler/news/newsqueryanalysis"
# jnius_config.set_classpath('.',classpath)
# from jnius import autoclass


def word_segment(text):
    pynlpir.open()
    segments = nlpir.segment_pos(text)
    segment_result = []
    pos_result = []
    for segment in segments:
        segment_result.append(segment[0])
        pos_result.append(segment[1])
    pynlpir.close()
    return segment_result, pos_result

def get_key_words(text):
    pynlpir.open()
    result = []
    keywords = pynlpir.get_key_words(text, weighted=True)
    if len(keywords) == 0:
        return result
    for i in range(len(keywords)):
        keyword = keywords[i][0]
        result.append(keyword)
    pynlpir.close()
    return result


def import_userdict(file_dir):
    pynlpir.open()
    nlpir.import_userdict(file_dir)
    pynlpir.close()

if __name__ == '__main__':
    import_userdict("pynlpir/userdict.txt")
