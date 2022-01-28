from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Review
from django.utils import timezone

# Create your views here.
def index(request):
    """
    리뷰 목록 출력
    """
    review_list = Review.objects.order_by('-create_date')
    content = {'review_list':review_list}
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