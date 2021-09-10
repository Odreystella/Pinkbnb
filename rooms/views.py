from django.core.paginator import InvalidPage, Paginator, EmptyPage
from django.shortcuts import render, redirect
from .models import Room


def enter_home(request):
    page_num = request.GET.get("page", 1)
    room_list = Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)     # room object의 리스트와 per_page를 넣고 paginator 만들기, paginator 클래스 리턴함
    
    try: 
        page_obj = paginator.page(int(page_num))  # get_page(페이지가 음수 or 총 페이지보다 클 경우 마지막 페이지 리턴) or page(페이지 없으면 에러) 메서드는 page object를 리턴함
        return render(request, "rooms/home.html", context={"page_obj": page_obj})
    
    except ValueError:
        page_obj = paginator.page(1)
        return redirect("/")
    except EmptyPage:
        page_obj = paginator.page(1)
        return redirect("/")


