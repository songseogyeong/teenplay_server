import os
from pathlib import Path

import numpy as np
import pandas as pd
from django.test import TestCase
from django.utils import timezone

import re

from activity.models import Activity
from club.models import Club
from member.models import Member, MemberFavoriteCategory
import random
from tqdm import tqdm
import joblib
import sklearn

from teenplay_server.models import Region
from konlpy.tag import Mecab

@staticmethod
def clean_text(text):
    # 문자열로 변환한 후 특수 문자와 줄 바꿈 문자를 제거하고 단일 공백으로 변환하며, 앞뒤 공백을 제거
    return re.sub(r'[^\w\s]+', '', text).replace('\n', '').replace('\r', ' ').strip()


@staticmethod
def process_club_data(club):
    # Club 객체의 데이터를 정규 표현식을 사용하여 클린한 후 리스트로 반환
    text = ' '.join(club)
    features = clean_text(text)
    return features

class AiTests(TestCase):
    # member = Member.enabled_objects.get(id=13)
    # member_address = member.member_address
    #
    # if member_address is None or member_address.strip() == '':
    #     print('dd')
    # else:
    #     print('no')

    # keywords = {
    #     1: ['공예', 'DIY', '수집', '독서', '원예', '사진 촬영', '낚시', '요리', '그림 그리기', '보드게임'],
    #     2: ['미술관', '전시회', '공연', '연극', '오페라', '클래식 음악', '영화 감상', '문학', '조각', '건축'],
    #     3: ['헬스', '요가', '필라테스', '등산', '달리기', '자전거', '수영', '클라이밍', '축구', '농구'],
    #     4: ['미식', '와인 시음', '커피 테이스팅', '디저트 만들기', '베이킹', '쿠킹 클래스', '술집 탐방', '페어링', '한식 요리', '세계 음식'],
    #     5: ['배낭여행', '국내 여행', '해외 여행', '캠핑', '트레킹', '로드트립', '힐링 여행', '여행 사진', '여행 계획', '숙소 추천'],
    #     6: ['독서 모임', '강연', '세미나', '온라인 코스', '명상', '리더십', '시간 관리', '목표 설정', '심리학', '인생 코칭'],
    #     7: ['지역 모임', '커뮤니티', '친목회', '동네 카페', '반려동물 산책', '마을 축제', '지역 행사', '동호회', '프리마켓', '이웃 사귀기'],
    #     8: ['데이트', '미팅', '블라인드 데이트', '매칭 이벤트', '소셜 파티', '커플 여행', '로맨스', '연애 상담', '사랑 이야기', '소개팅 팁'],
    #     9: ['투자', '주식', '펀드', '부동산', '재무 계획', '예금', '절약', '금융 상품', '비트코인', '경제 뉴스'],
    #     10: ['영어 회화', '스페인어', '일본어', '중국어', '프랑스어', '독일어', '이탈리아어', '러시아어', '언어 교환', '번역'],
    #     11: ['독서실', '학습법', '자격증 준비', '그룹 스터디', '시험 대비', '논문 작성', '온라인 강의', '집중력 향상', '문제 풀이', '학습 계획'],
    #     12: ['전통 축제', '음악 페스티벌', '문화 행사', '푸드 페스티벌', '연극 축제', '지역 축제', '불꽃놀이'],
    #     13: ['없음', '그 외', '그외']
    # }

    # model_path = os.path.join(Path(__file__).resolve().parent, 'ai/club.pkl')
    # model = joblib.load(model_path)
    #
    # members = list(Member.objects.filter(id__lt=19))
    # for member in tqdm(members):
    #     member_model_path = f'ai/2024/05/22/club_model{member.id}.pkl'
    #     os.makedirs(os.path.dirname(member_model_path), exist_ok=True)
    #     joblib.dump(model, member_model_path)
    #     member.member_recommended_club_model = member_model_path
    #     member.save(update_fields=['member_recommended_club_model'])
        # member_favorite_categories = list(MemberFavoriteCategory.objects.filter(status=1, member=member))
        # chosen_categories = []
        # for category in member_favorite_categories:
        #     chosen_categories += keywords[category.category_id]
        # if not chosen_categories:
        #     for c_ks in keywords.values():
        #         chosen_categories += c_ks
        # member_keywords = random.sample(chosen_categories, k=3)
        # member.member_keyword1 = member_keywords[0]
        # member.member_keyword2 = member_keywords[1]
        # member.member_keyword3 = member_keywords[2]
        # member.updated_date = timezone.now()
        # member.save(update_fields=['member_keyword1', 'member_keyword2', 'member_keyword3', 'updated_date'])

    member = Member.enabled_objects.get(id=18)

    # 회원의 ai 모델 경로 찾아오기
    member_club_ai_path = member.member_recommended_club_model

    # 회원의 ai 모델 경로를 통해 불러오기 (pkl 파일)
    model = joblib.load(os.path.join(Path(__file__).resolve().parent.parent, member_club_ai_path))

    club = Club.enabled_objects.get(id=4)

    region = Region.objects.get(id=club.club_region_id)

    # 문제-학습 데이터 (지역, 모임명, 모임소개, 모임정보, 카테고리)
    add_X_trian = [region.region, club.club_name, club.club_intro, club.club_info]
    # 정답-학습 데이터 (카테고리)
    add_y_train = [club.club_main_category.id]

    # 정규표현식 함수를 통해 특수문자 등 제거 gn list로 변환
    add_X_train_clean = [process_club_data(add_X_trian)]

    # # 훈련 결과 확인
    # result_df = pd.DataFrame(model.cv_results_)[['params', 'mean_test_score', 'rank_test_score']]
    #

    # 교차 검증 인한 최적의 추정기를 반환
    model = model.best_estimator_

    # 추가적인 훈련 데이터 변환
    additional_X_train_transformed = model.named_steps['count_vectorizer'].transform(add_X_train_clean)
    # 추가 훈련 진행 (카테고리 1부터 11까지 가져오기)
    # partial_fit는 온라인 학습을 지원하는 메서드로, 데이터가 점진적으로 도착할 때마다 모델을 업데이트
    model.named_steps['multinomial_NB'].partial_fit(additional_X_train_transformed, add_y_train, classes=[i for i in range(1, 12)])

    ############################

    # activity = Activity.objects.filter(id=15).first()
    #
    # category = activity.category
    # club = activity.club
    #
    # # 회원에 맞는 활동 추천 ai 모델을 불러옵니다.
    # model_file_name = member.member_recommended_activity_model
    #
    # # path
    # model_file_path = os.path.join(Path(__file__).resolve().parent.parent, model_file_name)
    #
    # # pkl 파일을 열어 객체 로드
    # model = joblib.load(model_file_path)
    #
    # # 불러온 ai 모델에 추가 fit을 진행합니다.
    # additional_X_train = [
    #     activity.activity_title + activity.activity_intro + activity.activity_address_location]
    # additional_y_train = [activity.category.id]
    #
    # print(additional_X_train)
    # print(additional_y_train)
    # additional_X_train_transformed = model.named_steps['count_v'].transform(additional_X_train)
    # model.named_steps['mnnb'].partial_fit(additional_X_train_transformed, additional_y_train,
    #                                       classes=[i for i in range(1, 14)])
    # pass