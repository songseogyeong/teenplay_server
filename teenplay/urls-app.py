from django.contrib import admin
from django.urls import path, include

from teenplay.views import TeenplayMainListAppView, TeenplayMainListAPIView

app_name = 'app-teenplay'

urlpatterns = [
    path('all/', TeenplayMainListAppView.as_view(), name='teenplay-main-list'),
    path('all/new/', TeenplayMainListAPIView.as_view(), name='teenplay-main-list-new'),
]


# 실제로 예상하는 url
# 틴플레이 접근 방식은 총 2가지가 있다.
# 1. 메인페이지에서 접근하는 방식
# 2. 모임에서 틴플레이 카테고리 접속 후 선택한 틴플레이를 띄우는 방식
# 3. 1번 url의 경우 ai 추천순을 배우기 전에 random으로 띄우고 두번째부터도 모두 랜넘으로 띄우는 방식을 사용하고 싶음
# 유튜브 쇼츠 확인 했을 때 최초로 쇼츠에 접속을 했을 떄 random 으로 10개를 띄우고 맨 아래쪽에 내려갔을 때는 10개씩 증가하는 형태를 띄우고 있음
# 4. 2번의 경우 선택한 모임의 틴플레이 번호로 띄워야 한다.(화면에 있는 번호를 e.target으로 받아와서 띄우는 방법도 있을 것 같다)
# 5. 또한 2번의 경우 만약 3번을 눌렀으면 위로 올렸을때 2번 1번 이런식으로 띄워야하고, 1번의 경우에는 random의 경우로 띄우는 것을 목표로 한다.
# , 그리고 random으로 띄우지만 최초로 띄웠을 때는 최신순 또는 근시일 내에 랜덤으로 띄워야 한다.

