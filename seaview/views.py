from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Review
from django.utils import timezone
from django.core.paginator import Paginator

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
    content = {'review_list':page_obj}
    return render(request, 'seaview/review_list.html', content)
    #return HttpResponse("Hello World")

def detail(request, review_id):
    """
    리뷰 내용 출력
    """
    #review = Review.objects.get(id=review_id)
    review = get_object_or_404(Review, pk=review_id)
    content = {'review': review}
    return render(request, 'seaview/review_detail.html', content)

def reply_create(request, review_id):
    """
    리뷰에 댓글 달기
    """
    review = get_object_or_404(Review, pk=review_id)
    review.reply_set.create(content=request.POST.get('content'),
                            create_date=timezone.now())
    return redirect('seaview:detail', review_id=review.id)