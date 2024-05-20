from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.models import Activity, ActivityLike
from club.models import Club, ClubMember
from notice.models import Notice
from search.models import RecentSearch


class MainView(View):
    def get(self, request):
        member = request.session.get('member')
        member_id = 0
        if member is not None:
            member_id = member.get('id')

        popular_activities = Activity.enabled_objects\
                                 .annotate(member_count=Count('activitymember')).order_by('-member_count')[:8]


        for activity in popular_activities:
            likes = ActivityLike.enabled_objects.filter(activity_id=activity.id).count()
            activity.like_count = likes
            is_like = ActivityLike.enabled_objects.filter(activity_id=activity.id, member_id=member_id).exists()
            activity.is_like = is_like

        new_activities = Activity.enabled_objects.\
                             annotate(member_count=Count('activitymember'), like_count=Count('activitylike')).order_by('-id')[:8]

        for activity in new_activities:
            is_like = ActivityLike.enabled_objects.filter(activity_id=activity.id, member_id=member_id).exists()
            activity.is_like = is_like

        # AI 추천 부분은 추후에 구현하겠습니다. 우선 최신순으로 하겠습니다.
        recommend_activities = Activity.enabled_objects\
                                   .annotate(member_count=Count('activitymember'), like_count=Count('activitylike')).order_by('-id')[:8]

        for activity in recommend_activities:
            is_like = ActivityLike.enabled_objects.filter(activity_id=activity.id, member_id=member_id).exists()
            activity.is_like = is_like

        popular_clubs = Club.enabled_objects.annotate(member_count=Count('clubmember')).order_by('-member_count')[:8]
        for popular_club in popular_clubs:
            club_id = popular_club.id
            activity_count = Activity.enabled_objects.filter(club_id=club_id).count()
            popular_club.activity_count = activity_count
            popular_club.is_manager = popular_club.member_id == member_id
            is_member = ClubMember.objects.filter(club_id=club_id, member_id=member_id)
            if is_member.exists():
                is_member = is_member.first()
                is_member = is_member.status
            else:
                is_member = 0
            popular_club.is_member = is_member


        context = {
            'popular_activities': popular_activities,
            'new_activities': new_activities,
            'recommend_activities': recommend_activities,
            'popular_clubs': popular_clubs
        }

        return render(request, 'main/web/main-web.html', context=context)


# 푸터에서 최신 공지사항 1개 띄우기
class FooterNoticeLatestAPI(APIView):
    def get(self, request):
        notices = Notice.objects.filter(status=True).values()
        notices = {
            'notices': notices
        }
        return Response(notices)


# 최근 검색어
class RecentSearchKeywordAPI(APIView):
    def get(self, request):
        member_id = request.session.get('member').get('id')
        keywords = list(RecentSearch.enabled_objects.filter(member_id=member_id).values().order_by('-id')[:6])

        return Response(keywords)

    def delete(self, request):
        id = request.data.get('id')
        recent_search = RecentSearch.enabled_objects.filter(id=id)
        if recent_search.exists():
            recent_search = recent_search.first()
            recent_search.status = 0
            recent_search.updated_date = timezone.now()
            recent_search.save(update_fields=['status', 'updated_date'])

        return Response("success")


# 최근 검색어 전체 삭제
class RecentSearchKeywordDeleteAllAPI(APIView):
    def get(self, request):
        member_id = request.session.get('member').get('id')
        recent_searches = RecentSearch.enabled_objects.filter(member_id=member_id)
        for recent_search in recent_searches:
            recent_search.status = 0
            recent_search.updated_date = timezone.now()
            recent_search.save(update_fields=['status', 'updated_date'])

        return Response("success")


# 검색어 입력 시마다 활동 검색결과 동적으로 출력
class RealTimeSearchAPI(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        condition = Q(activity_title__icontains=keyword)
        found_activities = list(Activity.enabled_objects.filter(condition).values('id', 'activity_title')[:5])

        return Response(found_activities)