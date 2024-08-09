import math

from django.db import transaction
from django.db.models import Q, Count, F
from django.db.models.functions import Concat
from django.forms import CharField
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.models import Activity, ActivityReply
from club.models import Club, ClubPost, ClubPostReply
from festival.models import Festival
from letter.models import Letter
from member.models import AdminAccount, Member
from member.serializers import AdminAccountSerializer
from notice.models import Notice

from django.utils import timezone

from wishlist.models import Wishlist, WishlistReply, WishlistTag


# 관리자 로그인 페이지 이동
class AdminLoginView(View):
    # 관리자 로그인 페이지 이동
    def get(self, request):
        # 지정된 템플릿을 렌더링(render)하여 응답 변환
        return render(request, 'admin/web/admin-login-web.html')

    def post(self, request):
        # 응답받은 데이터를 data 변수로 선언
        data = request.POST

        # 응답받은 각 데이터를 dict 객체로 변환
        # 'admin_id'와 'admin_password' 값을 key로 사용
        data = {
            'admin_id': data['admin_id'],
            'admin_password': data['admin_password']
        }

        # 응답받은 데이터를 조건으로 admin 객체 생성
        admin = AdminAccount.objects.filter(**data)

        # 데이터베이스에서 응답받은 data가 존재하는지 확인
        # 응답받은 data가 데이터 베이스에 존재할 경우
        if admin.exists():
            # admin 계정을 세션에 저장
            request.session['admin'] = AdminAccountSerializer(admin.first()).data
            # url를 관리자 페이지로 설정
            url = 'admin-user'
        # 응답받은 data가 데이터베이스에 존재하지 않을 경우
        else:
            # url를 로그인 페이지로 설정
            url = 'admin-login'


        # redirect를 통해 view로 접근하여 해당하는 페이지로 이동
        return redirect(url)


# 관리자 로그아웃
class AdminLogoutView(View):
    def get(self, request):
        # 로그아웃 시 session은 비우기
        request.session.clear()

        # url를 로그인 페이지로 설정
        url = 'admin-login'

        # redirect를 통해 view로 접근하여 로그인 페이지로 이동
        return redirect(url)


# 관리자 유저 - 페이지 이동
class AdminUserView(View):
    def get(self, request):
        # 지정된 템플릿을 렌더링(render)하여 응답 변환
        return render(request, 'admin/web/user-web.html')


# 관리자 유저 - 데이터 가져오기
class AdminUserAPI(APIView):
    def post(self, request, page):
        # 응답받은 데이터를 data 변수로 선언
        data = request.data

        # 응답 받은 데이터 값을 가져오기 ('응답 값'. '기본값')
        order = data.get('order', 'recent')
        category = data.get('category', '')
        keyword = data.get('keyword', '')

        # 한 번에 보여질 데이터 개수를 row_count 변수로 선언
        row_count = 10

        # 현재 페이지에 따라 데이터를 몇 개 건너뛸지 계산하여 offset 변수로 선언
        offset = (page - 1) * row_count
        # 현재 페이지에서 마지막으로 가져올 데이터의 위치를 limit 변수로 선언
        limit = page * row_count

        condition = Q(status=1) | Q(status=-1)

        if category:
            condition &= Q(status=category)

        if keyword:
            condition &= Q(member_nickname__contains=keyword)

        total = Member.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'category': category,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'member_nickname',
            'created_date',
            'status'
        ]

        members = Member.objects.filter(condition).values(*columns).order_by(ordering)

        members_count = members.count()
        context['members_count'] = members_count

        members = members[offset:limit]

        club_count = members.values('id').annotate(club_count=Count('club'))
        club_action_count = members.values('id').annotate(club_action_count=Count('clubmember', filter=Q(clubmember__status=1)))
        activity_count = members.values('id').annotate(activity_count=Count('activitymember', filter=Q(activitymember__status=1)))
        activity_club_count = members.values('id').annotate(activity_club_count=Count('club__activity', filter=Q(club__activity__status=1)))

        for i in range(len(members)):
            members[i]['club_count'] = club_count[i]['club_count']
            members[i]['club_action_count'] = club_action_count[i]['club_action_count']
            members[i]['activity_count'] = activity_count[i]['activity_count'] + activity_club_count[i]['activity_club_count']

        context['members'] = list(members)

        return Response(context)


# 관리자 유저 - 상태 변경
class AdminUserUpdateAPI(APIView):
    @transaction.atomic
    def patch(self, request, member_id):
        updated_date = timezone.now()

        member = Member.objects.get(id=member_id)

        if member.status == 1:
            member.status = -1
        elif member.status == -1:
            member.status = 1

        member.updated_date = updated_date
        member.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 쪽지 - 페이지 이동
class AdminMessageView(View):
    def get(self, request):
        return render(request, 'admin/web/message-web.html')


# 관리자 쪽지 - 데이터 가져오기
class AdminMessageAPI(APIView):
    # 데이터 가져오기
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')
        category = data.get('category', '')
        type = data.get('type', '')
        keyword = data.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        # 삭제되지 않은 쪽지만 가져오기
        condition = Q(status=1)

        # 멤버의 상태에 따른 카테고리 조회
        if category:
            condition &= Q(sender__status=category)

        # 검색 타입에 따른 검색 결과 필터
        if type:
            if keyword:
                # 보낸 사람
                if type == 's':
                    condition &= Q(sender__member_nickname__contains=keyword)

                # 받은 사람
                elif type == 'r':
                    condition &= Q(receiver__member_nickname__contains=keyword)

        # total= 쪽지 개수 세기
        total = Letter.objects.filter(condition).all().count()

        # 보여질 데이터의 개수
        page_count = 5

        # 페이징 처리
        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        # context에 필드 담기
        context = {
            'type': type,
            'keyword': keyword,
            'category': category,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        # 정렬(내림차순, 최신순)
        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'sender_id',
            'receiver_id',
            'created_date',
            'status',
            'letter_content'
        ]

        # 쪽지 가져오기
        letter = Letter.objects.filter(condition).values(*columns).order_by(ordering)
        sender_name = letter.annotate(sender_name=F('sender_id__member_nickname'))
        receiver_name = letter.annotate(receiver_name=F('receiver_id__member_nickname'))
        is_read = letter.annotate(is_read=F('receivedletter__is_read')).filter(updated_date__isnull=False)
        read_date = letter.annotate(read_date=F('receivedletter__updated_date')).filter(updated_date__isnull=False)
        member_status = letter.annotate(member_status=F('sender_id__status'))

        for i in range(len(list(letter))):
            letter[i]['sender_name'] = sender_name[i]['sender_name']
            letter[i]['receiver_name'] = receiver_name[i]['receiver_name']
            letter[i]['is_read'] = is_read[i]['is_read']
            letter[i]['read_date'] = read_date[i]['read_date']
            letter[i]['member_status'] = member_status[i]['member_status']

        context['letter'] = list(letter[offset:limit])

        return Response(context)


# # 관리자 틴플레이 - 페이지 이동
# class AdminTeenplayView(View):
#     def get(self, request):
#         return render(request, 'admin/web/teenplay-web.html')
#
#
# # 관리자 틴플레이 - 데이터 가져오기
# class AdminTeenplayAPI(APIView):
#     def get(self, request, page):
#         pass
#
#
# # 관리자 틴플레이 - 삭제하기
# class AdminTeenplayDeleteAPI(APIView):
#     def delete(self, request):
#         pass


# 관리자 게시글 홍보글 - 페이지 이동
class AdminPromoteView(View):
    def get(self, request):
        return render(request, 'admin/web/promote-web.html')


# 관리자 게시글 홍보글 - 데이터 가져오기
class AdminPromoteAPI(APIView):
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')
        type = data.get('type', '')
        keyword = data.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)

        if type:
            if keyword:
                # 모임 이름
                if type == 'w':
                    condition &= Q(club__club_name__contains=keyword)

                # 제목
                elif type == 'p':
                    condition &= Q(post_title__contains=keyword)

        total = ClubPost.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'type': type,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'post_title',
            'post_content',
            'image_path',
            'created_date',
            'view_count'
        ]

        club_post = ClubPost.objects.filter(condition).values(*columns).order_by(ordering)
        club_name = club_post.annotate(club_name=F('club__club_name'))
        club_reply_count = club_post.annotate(club_reply_count=Count('clubpostreply__id'))
        club_post_category = club_post.annotate(club_post_category=F('category__category_name'))

        for i in range(len(list(club_post))):
            club_post[i]['club_name'] = club_name[i]['club_name']
            club_post[i]['club_reply_count'] = club_reply_count[i]['club_reply_count']
            club_post[i]['club_post_category'] = club_post_category[i]['club_post_category']

        context['club_post'] = list(club_post[offset:limit])

        return Response(context)


# 관리자 게시글 홍보글 - 데이터 삭제
class AdminPromoteDeleteAPI(APIView):
    # 게시글 삭제
    @transaction.atomic
    def delete(self, request, promote_id):
        status = 0
        updated_date = timezone.now()

        club_post = ClubPost.objects.get(id=promote_id)
        club_post.status = status
        club_post.updated_date = updated_date
        club_post.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 게시글 활동 모집 - 페이지 이동
class AdminActivityView(View):
    def get(self, request):
        return render(request, 'admin/web/activity-web.html')


# 관리자 게시글 활동 모집 - 데이터 가져오기
class AdminActivityAPI(APIView):
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')
        type = data.get('type', '')
        keyword = data.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)

        if type:
            if keyword:
                # 작성자
                if type == 'w':
                    condition &= Q(club__member__member_nickname__contains=keyword)

                # 제목
                elif type == 'p':
                    condition &= Q(activity_title__contains=keyword)

        total = Activity.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'type': type,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'activity_title',
            'activity_content',
            'created_date',
            'recruit_start',
            'recruit_end',
        ]

        activity = Activity.objects.filter(condition).values(*columns).order_by(ordering)
        activity_writer = activity.annotate(activity_writer=F('club__member__member_nickname'))
        member_count = activity.annotate(member_count=Count('activitymember__member__id'))

        for i in range(len(list(activity))):
            activity[i]['activity_writer'] = activity_writer[i]['activity_writer']
            activity[i]['member_count'] = member_count[i]['member_count']

        context['activity'] = list(activity[offset:limit])

        return Response(context)


# 관리자 게시글 활동 모집 - 게시글 삭제
class AdminActivityDeleteAPI(APIView):
    @transaction.atomic
    def delete(self, request, activity_id):
        status = 0
        updated_date = timezone.now()

        activity = Activity.objects.get(id=activity_id)
        activity.status = status
        activity.updated_date = updated_date
        activity.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 게시글 위시리스트 - 페이지 이동
class AdminWishlistView(View):
    def get(self, request):
        return render(request, 'admin/web/wishlist-web.html')


# 관리자 게시글 위시리스트 - 데이터 가져오기
class AdminWishlistAPI(APIView):
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')
        category = data.get('category', '')
        type = data.get('type', '')
        keyword = data.get('keyword', '')
        wishlist_id = data.get('wishlist_id', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(member__status=1, status=1)

        if category:
            if category == '1':
                condition &= Q(is_private=1)

            elif category == '0':
                condition &= Q(is_private=0)

        if type:
            if keyword:
                if type == 'p':
                    condition &= Q(member__member_nickname__contains=keyword)

                elif type == 'w':
                    condition &= Q(wishlist_content__contains=keyword)

        if wishlist_id:
            condition &= Q(wishlist_id=wishlist_id)

        total = Wishlist.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'category': category,
            'type': type,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'wishlist_content',
            'is_private',
            'member__id',
            'member__member_nickname',
            'member__status',
            'category__category_name'
        ]

        wishlist = Wishlist.objects.filter(condition).values(*columns).order_by(ordering)

        wishlist_like = wishlist.values('member__id').annotate(wishlist_like_count=Count('wishlistlike'))
        wishlist_reply = wishlist.values('member__id').annotate(wishlist_reply_count=Count('wishlistreply'))

        for i in range(len(list(wishlist))):
            wishlist[i]['wishlist_like_count'] = wishlist_like[i]['wishlist_like_count']
            wishlist[i]['wishlist_reply_count'] = wishlist_reply[i]['wishlist_reply_count']

        # context['wishlist'] = list(wishlist[offset:limit])
        # print(context['wishlist'])

        wishlist = list(wishlist[offset:limit])

        wishlist_ids = [item['id'] for item in wishlist]
        tag_info_by_wishlist = {}

        for wishlist_id in wishlist_ids:
            tag_info = WishlistTag.objects.filter(wishlist_id=wishlist_id).values_list('tag_name', flat=True)
            tag_info_by_wishlist[wishlist_id] = list(tag_info)

        context['wishlist'] = {
            'wishlist': wishlist,
            'tags': tag_info_by_wishlist
        }

        return Response(context)


# 관리자 게시글 위시리스트 - 게시글 삭제
class AdminWishlistDeleteAPI(APIView):
    def delete(self, request, wishlist_id):
        status = 0
        updated_date = timezone.now()

        wishlist = Wishlist.objects.get(id=wishlist_id)
        wishlist.status = status
        wishlist.updated_date = updated_date
        wishlist.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 전체 모임 - 페이지 이동
class AdminMeetingView(View):
    def get(self, request):
        return render(request, 'admin/web/meeting-web.html')


# 관리자 전체 모임 - 데이터 가져오기
class AdminMeetingAPI(APIView):
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')
        keyword = data.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)

        if keyword:
            condition &= Q(club_name__contains=keyword)

        total = Club.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'club_name',
            'club_intro',
            'club_profile_path',
            'club_banner_path',
            'status'
        ]

        club = Club.objects.filter(condition).values(*columns).order_by(ordering)

        club_member_count = club.annotate(club_member_count=Count('clubmember__member_id', filter=Q(clubmember__status=1)))
        club_activity_count = club.annotate(club_activity_count=Count('activity'))
        club_activity_action_count = club.annotate(club_activity_action_count=Count('activity', filter=Q(activity__status=1)))
        club_activity_done_count = club.annotate(club_activity_done_count=Count('activity', filter=Q(activity__status=0)))

        for i in range(len(list(club))):
            club[i]['club_member_count'] = club_member_count[i]['club_member_count']
            club[i]['club_activity_count'] = club_activity_count[i]['club_activity_count']
            club[i]['club_activity_action_count'] = club_activity_action_count[i]['club_activity_action_count']
            club[i]['club_activity_done_count'] = club_activity_done_count[i]['club_activity_done_count']

        context['club'] = list(club[offset:limit])

        return Response(context)


# 관리자 전체 모임 - 데이터 삭제
class AdminMeetingDeleteAPI(APIView):
    @transaction.atomic
    def delete(self, request, meeting_id):
        status = 0
        updated_date = timezone.now()

        club = Club.objects.get(id=meeting_id)
        club.status = status
        club.updated_date = updated_date
        club.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 축제 - 페이지 이동
class AdminFestivalView(View):
    def get(self, request):
        return render(request, 'admin/web/festival-list-web.html')

class AdminFestivalPaginationAPI(APIView):
    def post(self, request, page):
        order = request.GET.get('order', 'recent')
        keyword = request.GET.get('keyword', '')
        type = request.GET.get('type', '')
        targetId = request.GET.get('targetId', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)

        if keyword:
            condition &= Q(festival_title__contains=keyword)
        else:
            condition &= Q()

        if targetId:
            condition &= Q(id=targetId)

        total = Festival.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'type': type,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'festival_title',
            'festival_location',
            'festival_end',
            'festival_content',
            'thumbnail_path',
            'festival_price',
            'festival_address',
            'festival_address_detail',
            'festival_location',
            'festival_start',
            'host_info',
            'host_phone',
            'provider_info',
            'provider_url',
            'created_date',
            'festival_content',
        ]

        festivals = Festival.objects.filter(condition).values(*columns).order_by(ordering)

        context['festivals'] = list(festivals[offset:limit])

        return Response(context)

# 관리자 축제 - 데이터 삭제
class AdminFestivalDeleteAPI(APIView):
    @transaction.atomic
    def delete(self, request, festival_id):
        print("축제 늗널마ㅓㅏㅁㄴ")
        print(festival_id)
        print(request.data['festival_id'])

        status = 0
        updated_date = timezone.now()

        festival = Notice.objects.get(id=festival_id)
        festival.status = status
        festival.updated_date = updated_date
        festival.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 축제 작성 - 페이지 이동
class AdminFestivalWriteView(View):
    def get(self, request):
        return render(request, 'admin/web/festival-create-web.html')

    @transaction.atomic
    def post(self, request):
        data = request.POST
        data = {
            'festival_title': data['festival_title'],
            'festival_content': data.get('festival_content'),
            'festival_price': data.get('festival_price'),
            'festival_address': data.get('festival_address'),
            'festival_address_detail': data.get('festival_address_detail'),
            'festival_location': data.get('festival_location'),
            'festival_start': data.get('festival_start'),
            'festival_end': data.get('festival_end'),
            'host_info': data.get('host_info'),
            'host_phone': data.get('host_phone'),
            'provider_info': data.get('provider_info'),
            'provider_url': data.get('provider_url'),

        }

        print(data)
        Festival.objects.create(**data)
        return redirect('/admin/festival/')



# 관리자 공지사항 - 페이지 이동
class AdminNoticeView(View):
    def get(self, request):
        return render(request, 'admin/web/notice-list-web.html')


# 관리자 공지사항 - 데이터 가져오기
class AdminNoticePaginationAPI(APIView):
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')
        category = data.get('category', '')
        keyword = data.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)
        if category:
            condition &= Q(notice_type=category)

        if keyword:
            condition &= Q(notice_title__contains=keyword)

        total = Notice.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'category': category,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'notice_title',
            'created_date',
            'notice_content',
            'notice_type'
        ]

        notices = Notice.objects.filter(condition).values(*columns).order_by(ordering)

        context['notices'] = list(notices[offset:limit])

        return Response(context)


# 관리자 공지사항 - 데이터 삭제
class AdminNoticeUpdateAPI(APIView):
    # 공지사항 수정
    def post(self, request, notice_id):
        data = request.data

        title = data.get('title', '')
        content = data.get('content', '')

        updated_date = timezone.now()

        notice = Notice.objects.get(id=notice_id)
        notice.updated_date = updated_date
        notice.notice_title = title
        notice.notice_content = content
        notice.save(update_fields=['updated_date', 'notice_title', 'notice_content'])

        return Response('success')


    # 공지사항 삭제
    def delete(self, request, notice_id):
        status = 0
        updated_date = timezone.now()

        notice = Notice.objects.get(id=notice_id)
        notice.status = status
        notice.updated_date = updated_date
        notice.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 공지사항 작성
class AdminNoticeWriteView(View):
    # 페이지 이동
    def get(self, request):
        return render(request, 'admin/web/notice-create-web.html')

    # 작성
    @transaction.atomic
    def post(self, request):
        data = request.POST

        data = {
            'notice_title': data['notice_title'],
            'notice_content': data['notice_content'],
            'notice_type': data['notice_type']
        }

        Notice.objects.create(**data)
        return redirect('/admin/notice/')


# 관리자 댓글 - 페이지 이동
class AdminCommentView(View):
    def get(self, request):
        return render(request, 'admin/web/comment-web.html')


# 관리자 댓글 - 데이터 가져오기
class AdminCommentAPI(APIView):
    def post(self, request, page):
        data = request.data
        print(page)

        order = data.get('order', 'recent')
        category = data.get('category', '')
        type = data.get('type', '')
        keyword = data.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(member_status=1) | Q(member_status=-1)

        if category:
            condition &= Q(member_status=category)

        if type:
            if keyword:
                # 작성자
                if type == 'w':
                    condition &= Q(member_name__contains=keyword)

                # 포스트
                elif type == 'p':
                    condition &= Q(title__contains=keyword)

        columns = [
            'member_name',
            'member_id_num',
            'title',
            'created',
            'reply',
            'member_status',
            'reply_id',
            'reply_member_id',
            'reply_status',
            'reply_updated_date'
        ]

        activities = Activity.enabled_objects \
            .annotate(
                member_name=F('activityreply__member__member_nickname'),
                member_id_num=F('activityreply__member__id'),
                title=F('activityreply__activity__activity_title'),
                created=F('activityreply__created_date'),
                reply=F('activityreply__reply_content'),
                member_status=F('activityreply__member__status'),
                reply_id=F('activityreply__id'),
                reply_member_id=F('activityreply__member__id'),
                reply_status=F('activityreply__status'),
                reply_updated_date=F('activityreply__updated_date'),
            ) \
            .values(*columns).filter(member_name__isnull=False, reply_status=1)

        wishes = Wishlist.enabled_objects \
            .annotate(
                member_name=F('wishlistreply__member__member_nickname'),
                member_id_num=F('wishlistreply__member__id'),
                title=F('wishlist_content'),
                created=F('wishlistreply__created_date'),
                reply=F('wishlistreply__reply_content'),
                member_status=F('wishlistreply__member__status'),
                reply_id=F('wishlistreply__id'),
                reply_member_id=F('wishlistreply__member__id'),
                reply_status=F('wishlistreply__status'),
                reply_updated_date=F('wishlistreply__updated_date')
            ) \
            .values(*columns).filter(member_name__isnull=False, reply_status=1)

        club_posts = ClubPost.enabled_objects \
            .annotate(
                member_name=F('clubpostreply__member__member_nickname'),
                member_id_num=F('clubpostreply__member__id'),
                title=F('clubpostreply__club_post__post_title'),
                created=F('clubpostreply__created_date'),
                reply=F('clubpostreply__reply_content'),
                member_status=F('clubpostreply__member__status'),
                reply_id=F('clubpostreply__id'),
                reply_member_id=F('clubpostreply__member__id'),
                reply_status=F('clubpostreply__status'),
                reply_updated_date=F('clubpostreply__updated_date')
            ) \
            .values(*columns).filter(member_name__isnull=False, reply_status=1)

        activity = activities.filter(condition)
        wishlist = wishes.filter(condition)
        club_post = club_posts.filter(condition)

        total = activity.union(wishlist).union(club_post).count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'category': category,
            'type': type,
            'keyword': keyword,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-created'
        if order == 'popular':
            ordering = '-post_read_count'

        comment = activity.union(wishlist).union(club_post).order_by(ordering)
        print(comment)

        context['comment'] = list(comment[offset:limit])

        return Response(context)


# 관리자 댓글 - 데이터 삭제
class AdminCommentDeleteAPI(APIView):
    @transaction.atomic
    def delete(self, request):
        reply_id = request.GET.get('reply_id', '')
        reply_member_id = request.GET.get('reply_member_id', '')
        created_date = request.GET.get('created_date', '')

        columns = [
            'member_name',
            'member_id_num',
            'title',
            'created',
            'reply',
            'member_status',
            'reply_id',
            'reply_member_id',
            'reply_status',
            'reply_updated_date'
        ]

        activities = Activity.enabled_objects \
            .annotate(
            member_name=F('activityreply__member__member_nickname'),
            member_id_num=F('activityreply__member__id'),
            title=F('activityreply__activity__activity_title'),
            created=F('activityreply__created_date'),
            reply=F('activityreply__reply_content'),
            member_status=F('activityreply__member__status'),
            reply_id=F('activityreply__id'),
            reply_member_id=F('activityreply__member__id'),
            reply_status=F('activityreply__status'),
            reply_updated_date = F('activityreply__updated_date')
        ) \
            .values(*columns).filter(member_name__isnull=False)

        wishes = Wishlist.enabled_objects \
            .annotate(
            member_name=F('wishlistreply__member__member_nickname'),
            member_id_num=F('wishlistreply__member__id'),
            title=F('wishlist_content'),
            created=F('wishlistreply__created_date'),
            reply=F('wishlistreply__reply_content'),
            member_status=F('wishlistreply__member__status'),
            reply_id=F('wishlistreply__id'),
            reply_member_id=F('wishlistreply__member__id'),
            reply_status=F('wishlistreply__status'),
            reply_updated_date=F('wishlistreply__updated_date')
        ) \
            .values(*columns).filter(member_name__isnull=False)

        club_posts = ClubPost.enabled_objects \
            .annotate(
            member_name=F('clubpostreply__member__member_nickname'),
            member_id_num=F('clubpostreply__member__id'),
            title=F('clubpostreply__club_post__post_title'),
            created=F('clubpostreply__created_date'),
            reply=F('clubpostreply__reply_content'),
            member_status=F('clubpostreply__member__status'),
            reply_id=F('clubpostreply__id'),
            reply_member_id=F('clubpostreply__member__id'),
            reply_status=F('clubpostreply__status'),
            reply_updated_date=F('clubpostreply__updated_date')
        ) \
            .values(*columns).filter(member_name__isnull=False)

        activity = activities.filter(reply_id=reply_id, reply_member_id=reply_member_id, created=created_date)
        wishlist = wishes.filter(reply_id=reply_id, reply_member_id=reply_member_id, created=created_date)
        club_post = club_posts.filter(reply_id=reply_id, reply_member_id=reply_member_id, created=created_date)

        comment = activity.union(wishlist).union(club_post)
        comment = list(comment)[0]

        wishlist_replies = list(WishlistReply.objects\
            .filter(id=comment['reply_id'],
                    member_id=comment['reply_member_id'],
                    created_date=comment['created']))

        activity_replies = list(ActivityReply.objects\
            .filter(id=comment['reply_id'],
                    member_id=comment['reply_member_id'],
                    created_date=comment['created']))

        club_post_replies = list(ClubPostReply.objects\
            .filter(id=comment['reply_id'],
                    member_id=comment['reply_member_id'],
                    created_date=comment['created']))

        if wishlist_replies:
            for wishlist_reply in wishlist_replies:
                wishlist_reply.status = 0
                wishlist_reply.updated_date = timezone.now()
                wishlist_reply.save(update_fields=['status', 'updated_date'])

        elif activity_replies:
            for activity_reply in activity_replies:
                activity_reply.status = 0
                activity_reply.updated_date = timezone.now()
                activity_reply.save(update_fields=['status', 'updated_date'])

        elif club_post_replies:
            for club_post_reply in club_post_replies:
                club_post_reply.status = 0
                club_post_reply.updated_date = timezone.now()
                club_post_reply.save(update_fields=['status', 'updated_date'])

        return Response('success')





# ----------------------------------------------------------------------------------------------------------------------
# 회사 소개 페이지 이동
class CompanyIntroductionView(View):
    def get(self, request):
        return render(request, 'company-info/web/company-info-web.html')


# 회사 소개에서 공지사항 띄우기
class CompanyNoticeListAPI(APIView):
    def get(self, request, page):
        row_count = 7
        offset = (page - 1) * row_count
        limit = page * row_count

        notices = Notice.objects.filter(status=True).values()[offset:limit]

        has_next = Notice.objects.filter(status=True)[limit:limit+1].exists()

        total = Notice.objects.filter(status=True).count()

        notice_info = {
            'notices': notices,
            'hasNext': has_next,
            'total': total
        }

        return Response(notice_info)

