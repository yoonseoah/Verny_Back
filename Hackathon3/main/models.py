from django.conf import settings
from django.db import models


"""
class User 부분 관련해서 settings.py에 AUTH_USER_MODEL = "main.User" 추가함.
class User 부분은 임의로 해놓은 부분!(서아 account부분이랑 합치면 다시 수정 예정)
대부분의 코드 멋사 세션 자료 DRF #2 자료 참고해서 작성함.
"""


# Create your models here.
#class User(AbstractUser):
    #email = models.EmailField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey('account.User', null=True, on_delete=models.CASCADE)  # 게시물 작성자
    title = models.CharField(max_length=200, null=True)
    painter = models.CharField(max_length=30, null=True)  # 그림 작품 작가
    drawing_technique = models.CharField(
        max_length=50, null=True
    )  # 피그마 탭1 oil on canvas 부분. 작품 형식 작성 부분
    work_year = models.CharField(max_length=20, null=True)  # 피그마 탭1 1916-1919. 작품 연도 부분.
    content = models.TextField(null=True)  # 작품 detail 설명
    type_choices = [
        ("고전미술", "고전미술"),
        ("현대미술", "현대미술"),
    ]  # 게시글 등록할 때 고전미술인지, 현대미술인지 체크하는 코드
    type = models.CharField(max_length=128, choices=type_choices, null=True)
    # 고전미술, 현대미술 체크하고 해시태그 기능 사용해서 나중에 나눠서 보여줄 때 사용할 코드.
    image = models.ImageField(upload_to="images/", blank=True, null=True)  # 작품 이미지 첨부
    scraps = models.ManyToManyField('account.User', related_name="scraped_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey('account.User', null=True, on_delete=models.CASCADE)  # 댓글 작성자
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # 댓글 내용
    likes = models.ManyToManyField('account.User',related_name="liked_comments", blank=True )
    #def get_comment_like_count(self):
        #return self.comment_like.count()

    #def update_like_count(self):
        #self.like_count = self.get_comment_like_count()
        #self.save()


class Recomment(models.Model):
    author = models.ForeignKey('account.User', null=True, on_delete=models.CASCADE)  # 대댓글 작성자
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="recomments")
    # 대댓글이 달린 댓글
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # 대댓글 내용
    relikes = models.ManyToManyField('account.User',related_name="liked_recomments", blank=True )

class Place(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=128, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    category_choices = [
        ("레저/체육/공원", "레저/체육/공원"),
        ("문화관광/명소", "문화관광/명소"),
        ("전시/공연", "전시/공연"),
    ]  # 게시글 등록할 때 고전미술인지, 현대미술인지 체크하는 코드
    category = models.CharField(max_length=50, choices=category_choices, null=True)  
    parking_choices = [
        ("무료주차", "무료주차"),
        ("유료주차", "유료주차"),
    ]  
    parking = models.CharField(max_length=50, choices=parking_choices, null=True)
    dis_parking_choices = [
        ("장애인 주차구역 있음", "장애인 주차구역 있음"),
        ("장애인 주차구역 없음", "장애인 주차구역 없음"),
    ]  
    dis_parking = models.CharField(max_length=50, choices=dis_parking_choices, null=True)
    big_parking_choices = [
        ("대형차 주차 불가", "대형차 주차 불가"),
        ("대형차 주차 가능", "대형차 주차 가능"),
    ]  
    big_parking = models.CharField(max_length=50, choices=big_parking_choices, null=True)
    wheelchair_choices = [
        ("휠체어 대여 불가", "휠체어 대여 불가"),
        ("휠체어 대여 가능", "휠체어 대여 가능"),
    ]  
    wheelchair = models.CharField(max_length=50, choices=wheelchair_choices, null=True)
    toilet_choices = [
        ("장애인 화장실 없음", "장애인 화장실 없음"),
        ("장애인 화장실 있음", "장애인 화장실 있음"),
    ]  
    toilet = models.CharField(max_length=50, choices=toilet_choices, null=True)
    braille_choices = [
        ("장애인 안내 점자 없음", "장애인 안내 점자 없음"),
        ("장애인 안내 점자 있음", "장애인 안내 점자 있음"),
    ]  
    braille = models.CharField(max_length=50, choices=braille_choices, null=True)
    audio_choices = [
        ("오디오 가이드 없음(한국어)", "오디오 가이드 없음(한국어)"),
        ("오디오 가이드 있음(한국어)", "오디오 가이드 있음(한국어)"),
    ]  
    audio = models.CharField(max_length=50, choices=audio_choices, null=True)