from django.shortcuts import redirect


def pre_handle_request(get_response):
    def middleware(request):
        # 사용자가 요청한 경로를 가져와 uri변수에 담아줍니다.
        uri = request.get_full_path()

        # 로그인이 필요한 서비스와 필요하지 않은 서비스를 구분하여 로그인이 필요하지 않은 서비스들은 이곳에 적어줍니다.
        if 'accounts' not in uri and 'oauth' not in uri and 'api' not in uri and 'static' not in uri\
                and 'admin' not in uri and 'upload' not in uri and 'kakao' not in uri and 'favicon' not in uri:
            if 'join' not in uri and 'login' not in uri and uri != '/' and 'terms' not in uri \
                    and 'company' not in uri and 'club/intro' not in uri\
                    and 'notice' not in uri and 'festival' not in uri \
                    and 'pr-post-list' not in uri and 'teenplay' not in uri and 'wishlist' not in uri:
                # 여기까지 넘어왔다면, 로그인이 필요한 서비스라는 뜻이므로 로그인 여부를 세션에서 체크합니다.
                # 만약 세션에 'member'가 없다면, 즉 로그인하지 않은 상태라면
                if request.session.get('member') is None:
                    # 현재 요청 경로를 세션에 'previous_uri' 키값으로 담아준 후
                    request.session['previous_uri'] = uri
                    # 로그인 페이지로 redirect합니다.
                    return redirect('/member/login')

            # request객체의 user_agent.is_mobile을 통해 현재 요청한 기기가 모바일 환경인지를 판단합니다.
            if request.user_agent.is_mobile:
                # is_mobile이 True라면, uri 앞에 '/app'을 붙여준 후 해당 uri로 redirect합니다.
                # '/app'으로 시작하는 경로에 대한 요청을 urls-web.py가 아닌 urls-app.py에서 처리하며, Web에 대한 view와 App에 대한 view를 분리하였습니다.
                if 'app' not in uri:
                    uri = f'/app{uri}'
                    return redirect(uri)

            # 모바일(반응형) 환경이 아닐 경우,
            else:
                # uri에 'app'이 포함되어 있다면
                if 'app' in uri:
                    # '/app'를 빈 문자열로 replace한 후 해당 uri로 redirect합니다.
                    uri = uri.replace('/app', '')
                    return redirect(uri)

        # 관리자 페이지 및 관리자 로그인과 관련된 부분입니다.
        # 만약 'admin'이 uri에 포함되어 있다면
        if 'admin' in uri:
            # 만약 'login'이 포함되어 있지 않다면,
            if 'login' not in uri:
                # 세션에 'admin'이 없다면, 즉 관리자 페이지를 요청하였으나 관리자 로그인이 되지 않은 상태라면
                if request.session.get('admin') is None:
                    # 요청한 경로를 세션의 'previous_uri'에 담아준 후
                    request.session['previous_uri'] = uri
                    # 관리자 로그인 페이지로 redirect합니다.
                    return redirect('/admin/login/')

        # 로그인이 필요하지 않은 서비스라면 전달받은 콜백 함수에 request객체를 전달하여 return합니다.
        response = get_response(request)
        return response

    # 클로저 함수인 middleware를 return 해줍니다.
    return middleware