from django.shortcuts import redirect


def check_url_active(get_response):
    def middleware(request):
        response = get_response(request)
        link = ['/ru/dasdas',]
        try:
            #print(request.path)
            # if request.path in link:
            if response.status_code == 500:
                return redirect('404')
        except:
            return redirect('index')


        return response
    return middleware
