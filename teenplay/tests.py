from datetime import datetime
from django.db.models.functions import Rank, RowNumber

# , RowNumber
from django.db.models import Count, F, Window, Q, Exists
from django.test import TestCase
from django.utils import timezone

from activity.models import Activity
from member.models import Member
from teenplay.models import TeenPlay, TeenPlayLike


class TeenplaySelect(TestCase):
    clubId = TeenPlay.enable_objects.get(id=1)
    print(clubId.club_id)

    # # 입력받은 변수 : selectedNumber
    # club_id =1
    # select_number = 3
    #
    # # 각 인스턴스에 대해 순차 번호(행 번호)를 부여합니다.
    # # 우선 모든 값에 대해서 row_number 로 각각의 행 번호를 입력해준다
    # videos = TeenPlay.enable_objects.annotate(row_number=Window(expression=RowNumber(),order_by=F('id').asc()))
    # print(videos)
    #
    # # 선택한 틴플레이 아이디가 있으면 해당 filter 를 통해 해당 id 의 Rownum을 알아내서 page 변수를 저장합니다.
    # if select_number:
    #     video = videos.filter(club_id= club_id,id=select_number).values('row_number').first()
    #     print(video)
    #     page= video.get('row_number')
    #     print(page)



# annotate(
# row_number=Window(expression=RowNumber(), order_by=F('id').asc()))
#
#
# ↑ page - 1
# ↓ page + 1
# 해당 페이지의 영상 조회
# videos = all().annotate(row_number)
#
# selectedNumber가 있으면
# video = videos.filter(id=selectedNumber)
# page = video.row_number
#
# 전달받은 페이지 번호가 row_number일 경우
# video = videos.filter(row_number=page)