import math

from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.models import Activity, ActivityImage, ActivityMember, ActivityReply, ActivityLike
from alarm.models import Alarm
from club.models import Club, ClubMember, ClubNotice
from festival.models import Festival
from member.models import Member, MemberProfile
from pay.models import Pay
from search.models import RecentSearch
from teenplay_server.category import Category
import re

from teenplay_server.models import Region
from bootpay_backend import BootpayBackend

def make_datetime(date, time="00:00"):
    date = date.split("/")
    date = "-".join([date[2], date[0], date[1]])
    time = time + ":00"
    datetime = timezone.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S')
    return datetime


class ActivityCreateWebView(View):
    def get(self, request):
        club_id = request.GET['club_id']
        festival_id = request.GET.get('festival_id')

        club = Club.enabled_objects.filter(id=club_id).first()
        categories = Category.objects.filter(status=True)
        context = {
            'club': club,
            'categories': categories,
            'festival_id': festival_id,
        }
        return render(request, 'activity/web/activity-new-web.html', context=context)

    @transaction.atomic
    def post(self, request):
        data = request.POST
        # 우선 받아온 데이터를 정리합니다.
        club = Club.enabled_objects.get(id=data.get('club-id'))
        pay_id = data.get('pay-id')
        pay = Pay.objects.filter(status=True, id=pay_id).first()
        try:
            activity_content = data.get('activity-content')
            recruit_start = make_datetime(data.get('recruit-start-date'), data.get('recruit-start-time'))
            recruit_end = make_datetime(data.get('recruit-end-date'), data.get('recruit-end-time'))
            category = Category.objects.get(id=data.get('category'))
            thumbnail = request.FILES.get('thumbnail-path')
            banner = request.FILES.get('banner-path')
            activity_start = make_datetime(data.get('activity-start-date'), data.get('activity-start-time'))
            activity_end = make_datetime(data.get('activity-end-date'), data.get('activity-end-time'))
            festival_id = data.get('festival-id')
            festival = None
            if festival_id is not None:
                festival = Festival.objects.get(id=festival_id)

            data = {
                'club': club,
                'activity_title': data.get('activity-title'),
                'activity_content': activity_content,
                'recruit_start': recruit_start,
                'recruit_end': recruit_end,
                'category': category,
                'activity_intro': data.get('activity-intro'),
                'activity_address_location': data.get('activity-address-location'),
                'activity_address_detail': data.get('activity-address-detail'),
                'thumbnail_path': thumbnail,
                'banner_path': banner,
                'activity_start': activity_start,
                'activity_end': activity_end,
                'festival': festival,
                'pay': pay,
            }

            # 정리한 데이터로 activity 정보를 insert한 후 객체를 저장
            activity = Activity.objects.create(**data)

            # summernote에서 미리 업로드한 이미지들을 대상으로 activity_id 및 status 업데이트
            image_ids = request.POST.get('image-id')
            if image_ids:
                for image_id in image_ids:
                    activity_image = ActivityImage.objects.filter(id=image_id)
                    if activity_image.exists():
                        activity_image = activity_image.first()
                        activity_image.status = 1
                        activity_image.activity_id = activity.id
                        activity_image.updated_date = timezone.now()
                        activity_image.save(update_fields=['status', 'activity_id', 'updated_date'])

            # 모임 구성원 중 알림을 켜놓은 사람들을 대상으로 알림 전송
            alarmed_member_ids = ClubMember.objects.filter(status=True, club_id=club.id, alarm_status=1).values('member_id')
            for alarmed_member_id in alarmed_member_ids:
                id = alarmed_member_id.get('member_id')
                member = Member.enabled_objects.filter(id=id)
                if not member.exists():
                    continue
                member = member.first()
                data = {
                    'target_id': activity.id,
                    'alarm_type': 6,
                    'sender': Member(**request.session.get('member')),
                    'receiver': member,
                }
                Alarm.objects.create(**data)

            return redirect(activity.get_absolute_url())

        except:
            # 오류 시 결제 취소하기
            receipt_id = pay.receipt_id
            bootpay = BootpayBackend('65e44626e57a7e001be37370',
                                     'NQmDRBsgOfziMiNXUEKrJGQ+YhXZncneSVG/auKihFA=')

            token = bootpay.get_access_token()

            if 'error_code' not in token:
                response = bootpay.cancel_payment(receipt_id=receipt_id,
                                                  cancel_price=pay.price,
                                                  cancel_username='관리자', cancel_message='취소됨')

            pay.status = 0
            pay.updated_date = timezone.now()
            pay.save(update_fields=['status', 'updated_date'])

            return redirect(f'/activity/create?club_id={club.id}')


class ActivityDetailWebView(View):
    def get(self, request):
        activity_id = request.GET['id']
        activity = Activity.objects.filter(id=activity_id).first()
        activity_content = activity.activity_content
        for i in range(len(activity_content)):
            if activity_content[i] == '"':
                activity_content = activity_content[i+1:]
            elif activity_content[i] == '<':
                break
        for i in range(len(activity_content)-1, -1, -1):
            if activity_content[i] == '"':
                activity_content = activity_content[:i]
            elif activity_content[i] == '>':
                break
        activity.activity_content = activity_content

        category = activity.category
        club = activity.club
        member_id = request.session['member']['id']
        activity_member_count = ActivityMember.enabled_objects.filter(activity_id=activity_id).count()
        activity_recruit_check = activity.recruit_end >= timezone.now() >= activity.recruit_start
        activity_replies = list(ActivityReply.enabled_objects.filter(activity_id=activity_id))
        activity_member_check = activity.club.member_id == member_id

        # 댓글 작성자 프사
        for reply in activity_replies:
            member_profile = MemberProfile.enabled_objects.filter(member_id=reply.member_id).first()
            reply.member_profile = member_profile

        club_notices = list(ClubNotice.objects.filter(status=True, club_id=club.id).order_by('-id')[:4])
        # 추천 활동
        recommended_activities = list(Activity.enabled_objects.exclude(id=activity_id)[0:4])

        # 각 추천활동별 참가자 수 및 관심 여부
        for recommended_activity in recommended_activities:
            member_count = ActivityMember.enabled_objects.filter(activity_id=recommended_activity.id).count()
            recommended_activity.member_count = member_count
            is_liked = ActivityLike.enabled_objects.filter(activity_id=recommended_activity, member_id=member_id).exists()
            recommended_activity.is_liked = is_liked
        # 관심 활동 여부
        is_like = ActivityLike.enabled_objects.filter(activity_id=activity_id, member_id=member_id).exists()

        context = {
            'activity': activity,
            'category': category,
            'club': club,
            'activity_member_count': activity_member_count,
            'activity_recruit_check': activity_recruit_check,
            'activity_replies': activity_replies,
            'club_notices': club_notices,
            'recommended_activities': recommended_activities,
            'is_like': is_like,
            'activity_member_check': activity_member_check
        }

        return render(request, 'activity/web/activity-detail-web.html', context)


class ActivityLikeAPI(APIView):
    def get(self, request):
        activity_id = request.GET['id']
        is_create = request.GET['is-create']
        member_id = request.session['member']['id']
        if is_create == "true":
            activity_like, created = ActivityLike.objects.get_or_create(activity_id=activity_id, member_id=member_id)
            if not created:
                activity_like.status = 1
                activity_like.updated_date = timezone.now()
                activity_like.save(update_fields=['status', 'updated_date'])
            return Response("added")

        activity_like = ActivityLike.objects.filter(activity_id=activity_id, member_id=member_id).first()
        activity_like.status = 0
        activity_like.updated_date = timezone.now()
        activity_like.save(update_fields=['status', 'updated_date'])
        return Response("deleted")


class ActivityLikeCountAPI(APIView):
    def get(self, request):
        activity_id = request.GET['id']
        # 관심활동으로 등록한 회원 수
        activity_like_count = ActivityLike.enabled_objects.filter(activity_id=activity_id).count()

        return Response(activity_like_count)

class ActivityMemberCountAPI(APIView):
    def get(self, request):
        activity_id = request.GET['id']
        activity_member_count = ActivityMember.enabled_objects.filter(activity_id=activity_id).count()

        return Response(activity_member_count)


class ActivityReplyAPI(APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        activity_id = request.GET.get('activity-id')

        row_count = 3
        offset = (page - 1) * row_count
        limit = page * row_count

        replies = ActivityReply.enabled_objects.filter(activity_id=activity_id).order_by('-id') \
            .annotate(member_nickname=F('member__member_nickname'), \
                      member_path=F('member__memberprofile__profile_path'),
                      member_email=F('member__member_email'))\
            .values('reply_content', 'id', 'member_nickname', 'created_date', 'member_id', 'member_email')

        return Response(replies[offset:limit])

    def post(self, request):
        data = request.data
        data = {
            'reply_content': data['reply_content'],
            'activity_id': data['activity_id'],
            'member_id': data['member_id']
        }

        activity_reply = ActivityReply.objects.create(**data)

        # 모임장에게 활동 상세글 댓글 알림 전송
        activity = Activity.enabled_objects.filter(id=data['activity_id']).first()
        club = Club.enabled_objects.filter(id=activity.club.id).first()
        if activity and club:
            alarm_data = {
                'target_id': activity.id,
                'alarm_type': 2,
                'sender_id': activity_reply.member.id,
                'receiver_id': club.member.id,
            }
            Alarm.objects.create(**alarm_data)

        return Response("success")

    def patch(self, request):
        activity_id = request.data['activity_id']
        member_id = request.data['member_id']
        reply_content = request.data['reply_content']
        id = request.data['id']

        activity_reply = ActivityReply.enabled_objects.get(id=id, activity_id=activity_id, member_id=member_id)
        activity_reply.reply_content = reply_content
        activity_reply.updated_date = timezone.now()
        activity_reply.save(update_fields=['reply_content', 'updated_date'])

        return Response("success")

    def delete(self, request):
        id = request.data['id']

        activity_reply = ActivityReply.enabled_objects.get(id=id)
        activity_reply.status = 0
        activity_reply.updated_date = timezone.now()
        activity_reply.save(update_fields=['status', 'updated_date'])

        return Response("success")


class ActivityListWebView(View):
    def get(self, request):
        selected_category = ''
        regions = Region.objects.filter(status=True)
        categories = Category.objects.filter(status=True)
        keyword = ''
        context = {
            'selected_category': selected_category,
            'categories': categories,
            'regions': regions,
            'keyword': keyword
        }
        return render(request, 'activity/web/activity-web.html', context=context)

    def post(self, request):
        selected_category = request.POST.get('category-id')
        regions = Region.objects.filter(status=True)
        categories = Category.objects.filter(status=True)
        keyword = request.POST.get('keyword', '')

        if keyword:
            recent_search, created = RecentSearch.objects.get_or_create(member_id=request.session.get('member').get('id'), keyword=keyword)
            if not created:
                recent_search.status = 1
                recent_search.updated_date = timezone.now()
                recent_search.save(update_fields=['status', 'updated_date'])

        context = {
            'selected_category': selected_category,
            'categories': categories,
            'regions': regions,
            'keyword': keyword
        }
        return render(request, 'activity/web/activity-web.html', context=context)


class ActivityListAPI(APIView):
    def post(self, request):
        data = request.data

        member_id = request.session.get('member').get('id')

        # 검색했을 시
        keyword = data.get('keyword', '')
        if keyword == "None":
            keyword = ""
        # 나머지들
        page = int(data.get('page', 1))
        date = data.get('date', '모든날')
        region = data.get('region', '')
        categories = data.get('categories', [])
        show_finished = data.get('showFinished', False)
        ordering = data.get('ordering', '새 행사순')
        order_options = {
            '추천순': '-id',
            '새 행사순': '-id',
            '모집 마감일순': 'recruit_end'
        }
        row_count = 12
        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q()

        condition &= Q(activity_title__icontains=keyword) | Q(activity_content__icontains=keyword)

        condition &= Q(activity_address_location__icontains=region)

        if date == '오늘':
            condition &= Q(activity_start__lte=timezone.now(), activity_end__gte=timezone.now())
        elif date == '이번주':
            condition &= Q(activity_start__lte=timezone.now() + timezone.timedelta(days=7),
                           activity_end__gte=timezone.now())
        elif date == '이번달':
            condition &= Q(activity_start__lte=timezone.now() + timezone.timedelta(weeks=4),
                           activity_end__gte=timezone.now())
        elif date == '모든날':
            condition = condition
        else:
            start_date, end_date = date.split(' - ')
            start_date = make_datetime(start_date)
            end_date = make_datetime(end_date)
            condition &= Q(activity_start__lte=end_date, activity_end__gte=start_date)

        if categories:
            condition &= Q(category_id__in=categories)
        if not show_finished:
            condition &= Q(recruit_start__lte=timezone.now(), recruit_end__gte=timezone.now())

        total_count = Activity.enabled_objects.filter(condition).count()

        page_count = 5
        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total_count / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        page_info = {
            'totalCount': total_count,
            'startPage': start_page,
            'endPage': end_page,
            'page': page,
            'realEnd': real_end,
            'pageCount': page_count,
        }
        activities = list(Activity.enabled_objects.filter(condition)\
                          .values().order_by(order_options[ordering])[offset:limit])
        for activity in activities:
            activity['member_count'] = ActivityMember.enabled_objects.filter(activity_id=activity['id']).count()
            activity['is_like'] = ActivityLike.enabled_objects.filter(activity_id=activity['id'], member_id=member_id).exists()
        activities.append(page_info)
        activities.append(total_count)

        return Response(activities)


class ActivityCategoryAPI(APIView):
    def get(self, request):
        categories = list(Category.objects.filter(status=True).values())

        return Response(categories)


class ActivityJoinWebView(View):
    def get(self, request):
        activity_id = request.GET.get('id')
        activity = Activity.enabled_objects.get(id=activity_id)
        member_count = ActivityMember.enabled_objects.filter(activity_id=activity_id).count()
        context = {
            'activity': activity,
            'member_count': member_count
        }

        return render(request, 'activity/web/activity-join-web.html', context=context)

    def post(self, request):
        data = request.POST
        data = {
            'activity_id': data.get('activity-id'),
            'member_id': data.get('member-id'),
            'status': -1
        }
        activity_member, created = ActivityMember.objects.get_or_create(**data)
        if not created and activity_member.status == 0:
            activity_member.status = -1
            activity_member.updated_date = timezone.now()
            activity_member.save(update_fields=['status', 'updated_date'])

        # 활동 가입 신청 알림 모임장에게 전송하기
        activity = Activity.enabled_objects.filter(id=request.POST.get('activity-id')).first()
        club = Club.enabled_objects.filter(id=activity.club.id).first()
        if activity and club:
            alarm_data = {
                'target_id': activity.id,
                'alarm_type': 11,
                'sender_id': request.POST.get('member-id'),
                'receiver_id': club.member.id
            }
            Alarm.objects.create(**alarm_data)

        return redirect('/member/mypage-activity/')


class ActivityImageUploadAPI(APIView):
    def post(self, request):
        upload_image = request.FILES.get('image')
        activity_image = ActivityImage.objects.create(image_path=upload_image)
        activity_image.status = 0
        activity_image.save(update_fields=['status'])
        image_path = activity_image.image_path.url
        image_id = activity_image.id

        return Response({
            'image_path': image_path,
            'image_id': image_id
        })
