from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Review, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import ReviewForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    """
    리뷰 목록 출력
    """
    # 입력인자
    page = request.GET.get('page', '1') #페이지
    # 조회
    review_list = Review.objects.order_by('-create_date')
    # 페이징 처리
    paginator = Paginator(review_list, 5) # 페이지 당 5개씩 보이기
    page_obj = paginator.get_page(page)

    context = {'review_list':page_obj}
    return render(request, 'seaview/review_list.html', context)
    #return HttpResponse("Hello World")

def detail(request, review_id):
    """
    리뷰 내용 출력
    """
    #review = Review.objects.get(id=review_id)
    review = get_object_or_404(Review, pk=review_id)
    context = {'review': review}
    return render(request, 'seaview/review_detail.html', context)

@login_required(login_url='accounts:login')
def reply_create(request, review_id):
    """
    리뷰에 댓글 달기
    """
    review = get_object_or_404(Review, pk=review_id)
    review.reply_set.create(content=request.POST.get('content'),
                            create_date=timezone.now())
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user  # author 속성에 로그인 계정 저장
            reply.create_date = timezone.now()
            reply.review = review
            reply.save()
            return redirect('seaview:detail', review_id=review.id)
    else:
        form = ReplyForm()
    context = {'review': review, 'form': form}
    return render(request, 'seaview/review_detail.html', context)


@login_required(login_url='accounts:login')
def review_create(request):
    """
    리뷰 등록
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user  # author 속성에 로그인 계정 저장
            review.create_date = timezone.now()
            review.save()
            return redirect('seaview:index')
    else:
        form = ReviewForm()
    context = {'form': form}
    return render(request, 'seaview/review_form.html', context)


@login_required(login_url='accounts:login')
def review_modify(request, review_id):
    """
    질문수정
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.modify_date = timezone.now()  # 수정일시 저장
            review.save()
            return redirect('seaview:detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    context = {'form': form}
    return render(request, 'seaview/review_form.html', context)


@login_required(login_url='accounts:login')
def review_delete(request, review_id):
    """
    질문삭제
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('seaview:detail', review_id=review.id)
    review.delete()
    return redirect('seaview:index')

@login_required(login_url='accounts:login')
def reply_delete(request, reply_id):
    """
    댓글삭제
    """
    reply = get_object_or_404(Reply, pk= reply_id)
    if request.user != reply.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        reply.delete()
    return redirect('seaview:detail', review_id = reply.review.id)