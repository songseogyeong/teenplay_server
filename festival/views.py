from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from festival.models import Festival

def make_datetime(date, time="00:00"):
    date = date.split("/")
    date = "-".join([date[2], date[0], date[1]])
    time = time + ":00"
    datetime = timezone.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S')
    return datetime


# web-festival 페이지 이동
class FestivalListWebView(View):
    def get(self, request):
        return render(request, 'festival/web/festival-web.html')


class FestivalListWebAPI(APIView):
    def get(self, request):
        data = request.GET
        # page, keyword, category, date, ongoing, including_end
        page = int(data.get('page', 1))
        keyword = data.get('keyword', '')
        category = int(data.get('category', 0))
        date = data.get('date', '')
        ongoing = data.get('ongoing', False)
        including_end = data.get('including_end', False)

        print(page, keyword, category, date, ongoing, including_end)

        row_count = 12
        offset = (page - 1) * row_count
        limit = page * row_count

        if including_end == 'true':
            condition = Q(festival_end__lt=timezone.now())
            if ongoing == 'true':
                condition |= Q(festival_start__lte=timezone.now())
        else:
            condition = Q(festival_end__gte=timezone.now())

        #
        # if ongoing == 'true':
        #     condition &= Q(festival_start__lte=timezone.now(), festival_end__gte=timezone.now())

        if date:
            start_date, end_date = date.split(' - ')
            start_date = make_datetime(start_date)
            end_date = make_datetime(end_date)
            condition &= Q(festival_start__lte=end_date, festival_end__gte=start_date)

        condition &= Q(festival_title__icontains=keyword) | Q(festival_location__icontains=keyword)

        if category > 0:
            condition &= Q(festival_category=category)

        festivals = Festival.enabled_objects.filter(condition).values()

        for festival in festivals:
            if festival.festival_start <= timezone.now() <= festival.festival_end:
                festival['type'] = '진행중'
            elif festival.festival_end < timezone.now():
                festival['type'] = '종료'
            elif timezone.now() < festival.festival_start:
                festival['type'] = f'D - {festival.festival_start - timezone.now()}'

        # post_info = {
        #     'fe'
        # }

        return Response('success')

        pass


# web-festival-detail 페이지 이동
class FestivalDetailtWebView(View):
    def get(self, request):
        return render(request, 'festival/web/festival-detail-web.html')


class FestivalDetailtWebAPI(APIView):
    def get(self, request, post):
        pass


class FestivalListAppView(View):
    pass

class FestivalListAppAPI(View):
    pass

class FestivalDetailAppView(View):
    pass

class FestivalDetailAppAPI(View):
    pass