# wanted_pre_onboarding
wanted_pre_onboarding Backend System


## 서비스 개요
- 크라우드 펀딩기능(게시자는 크라우드 펀딩을 받기위한 상품 등록)
- 유저는 펀딩하기 버튼을 클릭하여 해당 상품 '1회 펀딩금액' 만큼 펀딩


## 요구사항
- 상품등록(제목, 게시자명, 상품설명, 목표금액, 펀딩종료일, 1회펀딩금액) -> 완료
- 상품수정(목표금액 제외 전부 수정 가능) -> 완료
- 상품삭제 -> 완료
- 상품목록 -> 전체 완료
  - 제목, 게시자명, 총 펀딩금액, 달성률 및 D-day(펀딩 종료일까지) 포함 -> 완료
  - 상품 검색 기능 -> 완료
  - 상품 정렬 기능(생성일기준, 총펀딩금액 두가지 정렬) -> 완료
  - 상품 상세페이지 -> 완료

## 구현 과정
해당 과제를 구현하기 위해서는, 크게 **products app**과 **users app**이 필요했다.

### users
#### users/model.py
```python
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    USERNAME_FIELD = 'nickname'


    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.nickname

```
```python
class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, nickname, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
```
User 모델은 AbstractBaseUser를 상속받아 만들었고, `UserManager` 헬퍼클래스를 이용했다.

#### users/serializers.py
```python
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['nickname', 'email', 'name', 'password']
```
user는 email, nickname, name, password 입력을 통해 가입을 하고, 로그인할 수 있다.

#### users/views.py
```python
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```
회원가입을 위한 `UserCreate` 클래스는 위와 같이 작성했다.
```python
# config/urls.py 중 일부
    path('api-auth/', include('rest_framework.urls')),
```
로그인이 가능해야할 것 같아 DRF Authentication 공식문서를 참조하여 config app의 urls.py 에 인증 관련
라이브러리를 따로 사용해 테스트했다.

### products

#### products/models.py
```python
import datetime

from django.db import models

# Create your models here.
from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='products')
    total_amount = models.IntegerField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    description = models.TextField()
    onetime_amount = models.IntegerField(blank=False, null=False)
    now_amount = models.IntegerField(default=0)
    customers = models.ManyToManyField("users.User")
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    # D-day 계산
    def d_day(self):
        now = datetime.date.today()
        tmp = list(map(int, str(self.end_date).split("-")))
        target = datetime.date(tmp[0], tmp[1], tmp[2])
        return (target - now).days

    def customer_check(self):
        return self.customers.count()

    def achievement_rate(self):
        return f'{(self.now_amount / self.total_amount) *100 :.0f}%'
```
Product 모델은 다음과 같이 작성했다.

- title(제목)
- writer(작성자)
- total_amount(목표펀딩금액)
- end_date(펀딩종료일)
- description(상품설명)
- onetime_amount(1회펀딩금액)
- now_amount(총펀딩금액)
- customers(참여자)
- created_at(생성일)
- d_day(D-Day)
- customer_check(참여자 수)
- achievement_rate(달성률)


#### 상품 목록
```python
# products/serializers.py
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'title',
            'writer',
            'description',
            'total_amount',
            'end_date',
            'onetime_amount',
            'now_amount',
        ]
        read_only_fields = ('now_amount', )
        read_only_fields = ('customers', 'now_amount')



```
```python
# products/views.py
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    ordering_fields = ['created_at', 'total_amount']
    search_fields = ['title']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

```
요구사항에 기재되어있던
제목, 게시자명, 총펀딩금액, 달성률 및 d-day 게시 완료했다.

[이미지 첨부]

또한 상품 검색 기능과 상품 정렬기능은 drf 의 filters 라이브러리를 이용해 구현했다.


#### 상품 수정,삭제,상세페이지

```python
# products/serializers.py
class ProductDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='writer.nickname')

    class Meta:
        model = Product
        fields = [
            'title',
            'username',
            'now_amount',
            'achievement_rate',
            'd_day',
            'description',
            'total_amount',
            'customer_check',
            'end_date',
            'onetime_amount',
        ]

        read_only_fields = ('total_amount', 'now_amount')

        extra_kwargs = {
            'end_date' : {'write_only': True},
            'onetime_amount': {'write_only': True}
        }
```
```python
# products/views.py
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
```

목표금액(total_amount) 제외 수정이 가능하게끔 구현했고,
상세페이지는 제목(title), 게시자명(username), 총펀딩금액(now_amount), 달성률(ahcievement_rate),
D-day(d_day), 상품설명(description), 목표금액(total_amount), 참여자수(customer_check)를 뿌려준다.

#### 클라우드 펀딩 기능

```python
# products/serializers.py
class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = []
```
```python
# products/views.py
class FundingView(generics.RetrieveUpdateAPIView):

    queryset = Product.objects.all()
    serializer_class = FundingSerializer

    # 로그인된 사용자만
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        product.customers.add(request.user)
        product.now_amount += product.onetime_amount
        product.save()
        return Response(status=status.HTTP_200_OK)
```
```python
products/urls.py
    path('products/<int:pk>/funding', FundingView.as_view()),
```
로그인한 사용자라면 특정 게시물(상품)에 funding을 선택하여 1회펀딩금액(onetime_amount)만큼 펀딩이 가능하다.
funding 하게 되면 해당 게시물의 총펀딩금액(now_amount)은 1회펀딩금액만큼 증가하고,
해당 funding을 진행한 사용자가 이 전에 해당 상품에 펀딩한적이 없다면, 참여자에 추가시켜 구현했다.

로그인의 여부는 restframework 의 permissions 라이브러리를 활용했다.


