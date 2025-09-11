from django.shortcuts import render
from .models import Citation, Like, Dislike
import random
import string

def index(request,opinion=0,citation_pk=0):
    citations=Citation.objects.all()
    if len(citations)==0:
        context={
			'title': "Цитаты",
			'isEmpty': True
		}
        return render(request,'main/index.html',context)
    
    if opinion:
        ip=0
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        activeLike=False
        activeDislike=False
        citation=Citation.objects.get(pk=citation_pk)
        dislike_entry=Dislike.objects.filter(user=ip, citation=citation)
        like_entry=Like.objects.filter(user=ip, citation=citation)
        if not dislike_entry.exists() and not like_entry.exists():
            if opinion==1:
                likes=citation.likes+1
                if likes%10 or citation.weight==10:
                    Citation.objects.filter(pk=citation_pk).update(likes=likes)
                else:
                    Citation.objects.filter(pk=citation_pk).update(likes=likes, weight=citation.weight+1)
                activeLike=True
                Like.objects.create(user=ip, citation=citation)
            else:
                dislikes=citation.dislikes+1
                if dislikes%10 or citation.weight==1:
                    Citation.objects.filter(pk=citation_pk).update(dislikes=dislikes)
                else:
                    Citation.objects.filter(pk=citation_pk).update(dislikes=dislikes, weight=citation.weight-1)
                activeDislike=True
                Dislike.objects.create(user=ip, citation=citation)
        elif like_entry.exists() and opinion==2:
            Citation.objects.filter(pk=citation_pk).update(likes=citation.likes-1)
            dislikes=citation.dislikes+1
            if dislikes%10 or citation.weight==1:
                Citation.objects.filter(pk=citation_pk).update(dislikes=dislikes)
            else:
                Citation.objects.filter(pk=citation_pk).update(dislikes=dislikes, weight=citation.weight-1)
            activeDislike=True
            Like.objects.filter(user=ip, citation=citation).delete()
            Dislike.objects.create(user=ip, citation=citation)
        elif dislike_entry.exists() and opinion==1:
            Citation.objects.filter(pk=citation_pk).update(dislikes=citation.dislikes-1)
            likes=citation.likes+1
            if likes%10 or citation.weight==10:
                Citation.objects.filter(pk=citation_pk).update(likes=likes)
            else:
                Citation.objects.filter(pk=citation_pk).update(likes=likes, weight=citation.weight+1)
            activeLike=True
            Dislike.objects.filter(user=ip, citation=citation).delete()
            Like.objects.create(user=ip, citation=citation)
        elif dislike_entry.exists():
            activeDislike=True
        elif like_entry.exists():
            activeLike=True
        citation=Citation.objects.get(pk=citation_pk)
        context={
            'title': 'Цитаты', 'citation': citation, 'activeLike': activeLike, 'activeDislike': activeDislike, 'isEmpty': False
        }
        return render(request,'main/index.html',context)
    
    selected=[]
    rand=random.randint(1,10)
    while(True):
        for citation in citations:
            if citation.weight<=rand:
                selected.append(citation)
        if len(selected):
            break
        rand+=1
    length=len(selected)
    rand=random.randrange(length)
    chosen=citations[rand]
    views=chosen.views+1
    ip=0
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    dislike_entry=Dislike.objects.filter(user=ip, citation=chosen)
    like_entry=Like.objects.filter(user=ip, citation=chosen)
    activeLike=False
    activeDislike=False
    if dislike_entry.exists():
        activeDislike=True
    elif like_entry.exists():
        activeLike=True
    Citation.objects.filter(pk=chosen.pk).update(views=views)
    citation=Citation.objects.get(pk=chosen.pk)
    context={
		'title': 'Цитаты',
		'citation': citation,
		'isEmpty': False,
		'activeLike': activeLike,
		'activeDislike': activeDislike
	}
    return render(request,'main/index.html',context)

def popular(request):
    citations=Citation.objects.all()
    if len(citations)==0:
        context={
			'title': "Цитаты",
			'isEmpty': True
		}
        return render(request,'main/index.html',context)
    length=len(citations)
    prev_max_likes=0
    selected=[]
    run=0
    while(True):
        max_likes=-1
        for citation in citations:
            if run==0:
                if max_likes<citation.likes:
                    max_likes=citation.likes
            else:
                if max_likes<citation.likes and citation.likes<prev_max_likes:
                    max_likes=citation.likes
        for citation in citations:
            if citation.likes==max_likes:
                selected.append(citation)
                if len(selected)==10 or len(selected)==length:
                    break
        if len(selected)==10  or len(selected)==length:
            break
        run+=1
        prev_max_likes=max_likes
    context={
		'title': "Популярные",
		'citations': selected
	}
    return render(request,'main/popular.html',context)

def add(request):
    if request.method == 'POST':
        source=request.POST.get("source")
        text=request.POST.get("text")
        weight=request.POST.get("weight")
        citations=Citation.objects.all()
        if citations is None:
            Citation.objects.create(source=source, text=text, weight=weight)
            context={
                'title': 'Добавить',
                'alert': 'Цитата добавлена'
            }
            return render(request,'main/add.html',context)
        translator = str.maketrans('', '', string.punctuation)
        for citation in citations:
            rival=citation.text
            stripped_rival=((rival.translate(translator)).lower()).strip()
            stripped_text=((text.translate(translator)).lower()).strip()
            if stripped_rival==stripped_text:
                context={
                'title': 'Добавить',
                'alert': 'Такая цитата уже существует'
            	}
                return render(request,'main/add.html',context)
        count=0
        for citation in citations:
            rival=citation.source
            stripped_rival=((rival.translate(translator)).lower()).strip()
            stripped_source=((source.translate(translator)).lower()).strip()
            if stripped_rival==stripped_source:
                count+=1
                if count==3:
                    context={
                        'title': 'Добавить',
                        'alert': 'Слишком много цитат из одного источника'
                    }
                    return render(request,'main/add.html',context)
        Citation.objects.create(source=source, text=text, weight=weight)
        context={
                'title': 'Добавить',
                'alert': 'Цитата добавлена'
            }
        return render(request,'main/add.html',context)
    context={ 'title': 'Добавить' }
    return render(request,'main/add.html',context)
    
def choice(request, citation_pk):
    chosen=Citation.objects.get(pk=citation_pk)
    views=chosen.views+1
    ip=0
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    dislike_entry=Dislike.objects.filter(user=ip, citation=chosen)
    like_entry=Like.objects.filter(user=ip, citation=chosen)
    activeLike=False
    activeDislike=False
    if dislike_entry.exists():
        activeDislike=True
    elif like_entry.exists():
        activeLike=True
    Citation.objects.filter(pk=chosen.pk).update(views=views)
    citation=Citation.objects.get(pk=chosen.pk)
    context={
		'title': 'Цитаты',
		'citation': citation,
		'isEmpty': False,
		'activeLike': activeLike,
		'activeDislike': activeDislike
	}
    return render(request,'main/index.html',context)    
