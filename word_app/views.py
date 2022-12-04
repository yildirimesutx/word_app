from word_app.models import Word
from django.shortcuts import get_object_or_404, redirect, render
from decouple import config
import requests
from pprint import pprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url ='/auth/login')
def home(request):
    API_Key = config('API_KEY')
    API_Host =config('API_HOST')
    word = request.GET.get('name')
    request_headers= {"X-RapidAPI-Key":API_Key, "X-RapidAPI-Host":API_Host}

    if word:
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"
        response = requests.get(url, headers=request_headers)
        print(response)
        content = response.json()

        if response.ok:
            content = response.json()
            r_word = content['word']
            if Word.objects.filter(name=r_word):
                messages.warning(request, 'Word already exists!')

            elif  content['definitions'] == [] : 
                messages.error(request, 'This word has no meaning, search again!')

            else:
                Word.objects.create(name=r_word)
                messages.success(request, 'Word created!')
        else:
            messages.error(request, 'There is not Word!')
        return redirect('home')
    
    word_data = []
    words = Word.objects.all()
    for word in words:
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"
        response = requests.get(url, headers=request_headers)
        content = response.json()
        data = {
            
            # 'word': content['word'],
            'word': word,
            'definition': content['definitions'][0]["definition"]
        }
        word_data.append(data)
        pprint(word_data)
        
    context = {
        'word_data': word_data,
    }
    return render(request, 'word_app/home.html', context)


def list(request):
    API_Key = config('API_KEY')
    API_Host =config('API_HOST')
    word = request.GET.get('name')
    request_headers= {"X-RapidAPI-Key":API_Key, "X-RapidAPI-Host":API_Host}

    word_data = []
    words = Word.objects.all()
    for word in words:
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"
        response = requests.get(url, headers=request_headers)
        content = response.json()
        data = {
            
            # 'word': content['word'],
            'word': word,
            'definition': content['definitions'][0]["definition"]
        }
        word_data.append(data)
        pprint(word_data)
        
    context = {
        'word_data': word_data,
    }
    return render(request, 'word_app/list.html', context)




def delete_city(request, id):
    city = get_object_or_404(Word, id=id)
    city.delete()
    messages.success(request, 'Word deleted!')
    return redirect('home')



def about(request):
    return render(request, 'word_app/about.html')