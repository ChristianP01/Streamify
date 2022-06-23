from django.shortcuts import render


def chatws(request):
    return render(request, "chatify/chatpage.html", context={
        "msg":"ChatPageRoom!"
        })

def chatroom(request, room):
    return render(request, "chatify/chatpage2.html", context={
        "msg": room
    })