import datetime
from oauth2_provider.decorators import protected_resource
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import Account, Transaction
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from banking_system.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import xlwt


User = get_user_model()


@csrf_exempt
@login_required
def index(request):
    try:
        account = Account.objects.get(user=request.user)
        context = {
            'account': account
        }
    except:
        context = {
            'account': None
        }
    if request.method == 'POST':
        account_number = request.POST.get('acc_no')
        try:
            account = Account(user=request.user, account_number=account_number)
        except:
            print('Error')
        account.save()
        return redirect('/')
    return render(request, 'accounts/index.html', context)


@csrf_exempt
def deposit(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        deposit_amt = Decimal(request.POST.get('deposit_amt'))
        updated_balance = account.balance + deposit_amt
        transaction = Transaction(account=account, balance=account.balance,
                                  updated_balance=updated_balance, deposit=deposit_amt)
        transaction.save()
        account.deposit(deposit_amt)
        account.save()
        subject = 'Transaction Alert'
        message = f'Rs. {str(deposit_amt)} has been credited to your account.'
        recipient = request.user.email
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        return redirect('/')
    return render(request, 'accounts/deposit.html', {'account': account})


def withdraw(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        withdraw_amt = Decimal(request.POST.get('withdraw_amt'))
        updated_balance = account.balance - withdraw_amt
        if updated_balance < 0:
            message = 'Balance should be positive!'
            return render(request, 'accounts/withdraw.html', {'account': account, 'message': message})
        transaction = Transaction(account=account, balance=account.balance,
                                  updated_balance=updated_balance, withdrawn=withdraw_amt)
        transaction.save()
        account.withdraw(withdraw_amt)
        account.save()
        subject = 'Transaction Alert'
        message = f'Rs. {str(withdraw_amt)} has been debited from your account.'
        recipient = request.user.email
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        return redirect('/')
    return render(request, 'accounts/withdraw.html', {'account': account})


def transactions(request):
    account = Account.objects.get(user=request.user)
    all_transactions = account.transactions.all()
    context = {
        'account': account,
        'all_transactions': all_transactions
    }
    return render(request, 'accounts/transactions.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context['form'] = LoginForm()
            return redirect('/')
        else:
            messages.info(request, 'No user found with the given credentials!')
            return redirect('/login')
    return render(request, 'auth/login.html', context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        login(request, new_user)
        return redirect('/')
    return render(request, 'auth/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('/')


def export_users_xls(request):
    account = Account.objects.get(user=request.user)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="transactions.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Transactions')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Account Number', 'Balance', 'Updated Balance', 'Deposit', 'Withdrawn', 'Time', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = account.transactions.all().values_list('account', 'balance', 'updated_balance',
                                                  'deposit', 'withdrawn', 'time')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@protected_resource()
def oauth_login(request):
    return redirect('/')
