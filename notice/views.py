import math

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from notice.models import Notice


class NoticeListWebView(View):
    def get(self, request):
        view = request.GET.get('view', '')

        context = {'view': view}

        return render(request, 'notice/web/notice-web.html', context=context)


class NoticeListAPIView(APIView):
    def post(self, request, page):
        data = request.data

        order = data.get('order', 'recent')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        # notice_type = 0(공지사항), 1(자주묻는질문)
        condition = Q(status=1)

        # total= 쪽지 개수 세기
        total = Notice.objects.filter(condition).all().count()

        # 보여질 데이터의 개수
        page_count = 10

        # 페이징 처리
        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        # context에 필드 담기
        context = {
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
            'notice_title',
            'notice_content',
            'created_date',
            'updated_date',
        ]

        notice_post = Notice.objects.filter(condition).values(*columns).order_by(ordering)

        context['notice_post'] = list(notice_post[offset:limit])

        return Response(context)