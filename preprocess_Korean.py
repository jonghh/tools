!pip install konlpy
from konlpy.tag import Hannanum
import re

def preprocess_nouns(document):
    ''' 한국어 명사 추출해 문장별로 단어 리스트로 정리'''
    sentences=re.split('\.\s+', document.strip())
    results = []
    for sent in sentences:
        try:
            # 국어영어 아닌 문자 제거
            letters_only = re.sub('[^ㄱ-힣a-zA-Z]', ' ', sent)
            # 형태소 분석기 불러와 단어 분리
            hannanum = Hannanum()
            # 명사만 선택할 경우
            morph_words = hannanum.nouns(letters_only)
            # stopwords 적용해 불용어 제거
            stopwords =['특파원', '기자', '단독', '앵커', '취재','특종','신문','방송', '보도','외신','뉴스']# 필요한 불용어 추가
            meaningful_words = [w for w in morph_words if w not in stopwords]
            # 2음절 이상만 선택
            meaningful_words2 = [w for w in meaningful_words if len(w)>1]
            results.append(meaningful_words2)
        except:
            results.append([''])
    return results

def preprocess_npm(document):
    ''' 한국어 체언(n), 용언(p), 수식언(m) 추출해 문장별로 단어 리스트로 정리'''
    sentences=re.split('\.\s+', document.strip())
    results = []
    for sent in sentences:
        try:
            # 국어영어 아닌 문자 제거
            letters_only = re.sub('[^ㄱ-힣a-zA-Z]', ' ', sent)
            # 형태소 분석기 불러와 단어 분리
            hannanum = Hannanum()
            morp_words = hannanum.pos(letters_only)
            # 특정 형태소 단어만 선택. 용언의 경우 '다'를 붙여 기본형으로.
            morph_words =[]
            for w in morp_words:
                if w[1] in ['N','M']:    # N 체언 P 용언 M 수식언
                    morph_words.append(w[0])
                elif w[1] == 'P':
                    morph_words.append(w[0]+"다")
                else:
                    pass
            # stopwords 적용해 불용어 제거
            stopwords =['특파원', '기자', '단독', '앵커', '취재','특종','신문','방송', '보도','외신','뉴스']# 필요한 불용어 추가
            meaningful_words = [w for w in morph_words if w not in stopwords]
            # 2음절 이상만 선택
            meaningful_words2 = [w for w in meaningful_words if len(w)>1]
            results.append(meaningful_words2)
        except:
            results.append([''])
    return results
