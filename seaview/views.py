from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Review, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import ReviewForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,Count


# Create your views here.
def index(request):
    """
    리뷰 목록 출력
    """
    # 입력인자
    page = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw','') #검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        review_list = Review.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    else:  # recent
        review_list = Review.objects.order_by('-create_date')
    if kw:
        review_list = review_list.filter(
            Q(postname__icontains=kw) |  #제목검색
            Q(author__username__icontains=kw)  #글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(review_list, 5) # 페이지 당 5개씩 보이기
    page_obj = paginator.get_page(page)
    max_page = len(paginator.page_range)

    context = {'review_list':page_obj, 'max_page':max_page, 'page': page, 'kw': kw,'so': so}
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
    리뷰 수정
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
    리뷰 삭제
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('seaview:detail', review_id=review.id)
    review.delete()
    return redirect('seaview:index')

@login_required(login_url='accounts:login')
def reply_modify(request, reply_id):
    """
    댓글수정
    """
    reply = get_object_or_404(Reply, pk = reply_id)
    if request.user != reply.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('seaview:detail', review_id = reply.review.id)

    if request.method == "POST":
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.modify_date = timezone.now()
            reply.save()
            return redirect('seaview:detail', review_id=reply.review.id)
        else:
            form = ReplyForm(instance=reply)

        context = {'reply': reply, 'form': form}
        return render(request, 'seaview/reply_form.html', context)

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

@login_required(login_url='accounts:login')
def vote_review(request, review_id):
    """
    추천
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        review.voter.add(request.user)
    return redirect('seaview:detail', review_id=review.id)