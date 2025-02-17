from django.shortcuts import render, redirect
from django.utils import timezone
from .form import UserInfoForm
from .models import UserInfo, UserResponse
import pandas as pd
import csv, os
import random
import time

from django.conf import settings


def save_response_to_csv(user_info, question, response, vraie_reponse, tempsmis):
    responses_dir = os.path.join(settings.BASE_DIR, 'reponses')
    if not os.path.exists(responses_dir):
        os.makedirs(responses_dir)
    csv_file_path = os.path.join(responses_dir, f'reponses_{user_info.id}.csv')
    file_exists = os.path.isfile(csv_file_path)
    data = {
        'timestamp': time.time(),
        'tempsmis': tempsmis,
        'user_id': user_info.id,
        'question': question,
        'response': response,
        'vrairep': vraie_reponse,
    }
    fieldnames = ['timestamp', 'tempsmis', 'user_id', 'question', 'response', 'vrairep']
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def save_users_to_csv(user_info):
    users_dir = os.path.join(settings.BASE_DIR, 'utilisateur')
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)
    csv_file_path = os.path.join(users_dir, 'users.csv')
    file_exists = os.path.isfile(csv_file_path)
    data = {
        'user_id': user_info.id,
        'age': user_info.age,
        'genre': user_info.genre,
        'niveau_scolaire': user_info.niveau_scolaire,
        'ethnie': user_info.ethnie,
    }
    fieldnames = ['user_id', 'age', 'genre', 'niveau_scolaire', 'ethnie']
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def get_question(question_index):
    df = pd.read_excel('C:/Users/Khalil/Desktop/MYAPP/Dataset_francais_mai2024.xlsx')
    questions = df[['News', 'Label']].dropna().to_dict(orient='records')
    
    if question_index >= len(questions):
        return None

    return questions[question_index]


def user_info(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            user_info = form.save()
            request.session['user_info_id'] = user_info.id
            request.session['question_index'] = 0 
            # Enregistrer l'utilisateur dans le fichier CSV
            save_users_to_csv(user_info)
            return redirect('check_news')
    else:
        form = UserInfoForm()
    return render(request, 'myapp/user_info.html', {'form': form})


def check_news(request):
    user_info_id = request.session.get('user_info_id')
    if not user_info_id:
        return redirect('user_info')

    user_info = UserInfo.objects.get(id=user_info_id)
    question_index = request.session.get('question_index', 0)
    # Vérifier si nous avons atteint la fin des questions
    if request.method == 'POST':
        start_time = request.session.get('start_time')
        end_time = timezone.now()
        elapsed_time = (end_time - timezone.datetime.fromisoformat(start_time)).total_seconds() if start_time else None
        response = request.POST.get('response')
        question_text = request.session.get('current_question')
        vraie_reponse = request.session.get('current_vraie_reponse')
        # Enregistrer la reponse en base de données
        if response and question_text and vraie_reponse:
            UserResponse.objects.create(
                user_info=user_info,
                question=question_text,
                response=response,
                vrairep=vraie_reponse,
                tempsmis=elapsed_time
            )
        
            # Enregistrer aussi dans le fichier CSV spécifique à chaque utilisateur
            save_response_to_csv(
                user_info=user_info,
                question=question_text,
                response=response,
                vraie_reponse=vraie_reponse,
                tempsmis=elapsed_time
            )

            request.session['start_time'] = timezone.now().isoformat()
            request.session['question_index'] = question_index + 1

        return redirect('check_news')
    
    question_data = get_question(question_index)
    if not question_data:
        return render(request, 'myapp/error.html', {'message': "Toutes les questions ont été répondues."})

    question_text = question_data['News']
    vraie_reponse = "Vrai" if question_data['Label'] else "Faux"

    request.session['current_question'] = question_text
    request.session['current_vraie_reponse'] = vraie_reponse
    request.session['start_time'] = timezone.now().isoformat()

    return render(request, 'myapp/check_news.html', {'question': question_text})


