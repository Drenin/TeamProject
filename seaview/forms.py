from django import forms
from seaview.models import Review, Reply


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['postname', 'content']

        labels = {
            'postname': '제목',
            'content': '내용',
        }
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

        labels = {
            'content': '댓글',
        }