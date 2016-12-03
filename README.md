# Toyoko Inn

Simple script to fetch reservable rooms.

[東横INN公式ホームページ](https://www.toyoko-inn.com/)

# Dependency

* python-pip

# Installation

Install required packages.

```
$ pip -r requirement.txt --user
```

# How to use

## Import

```python
>>> from ToyokoInn import ToyokoInn
```

## Specify hotel

Default is by name

### By name

```python
>>> hotel = ToyokoInn(name="大阪JR野田駅前")
>>> print hotel
<Hotel 東横INN大阪JR野田駅前: dataid='218', state='27', substateid='8'>
```

### Candidates

```python
>>> hotel = ToyokoInn("大阪")
Candidates are:
0.444444%: <Hotel 東横INN大阪船場: dataid='47', state='27', substateid='10'>
0.428571%: <Hotel 東横INN大阪船場2: dataid='292', state='27', substateid='10'>
0.400000%: <Hotel 東横INN大阪船場東: dataid='39', state='27', substateid='10'>
0.400000%: <Hotel 東横INN大阪梅田東: dataid='138', state='27', substateid='8'>
0.363636%: <Hotel 東横INN大阪伊丹空港: dataid='261', state='27', substateid='205'>
0.363636%: <Hotel 東横INN大阪鶴橋駅前: dataid='257', state='27', substateid='10'>
0.363636%: <Hotel 東横INN大阪通天閣前: dataid='279', state='27', substateid='10'>
0.363636%: <Hotel 東横INN大阪心斎橋西: dataid='23', state='27', substateid='10'>
0.363636%: <Hotel 東横INN新大阪駅東口: dataid='260', state='27', substateid='9'>
0.342857%: <Hotel 東横INN大阪JR野田駅前: dataid='218', state='27', substateid='8'>
0.333333%: <Hotel 東横INN大阪谷四交差点: dataid='164', state='27', substateid='10'>
0.307692%: <Hotel 東横INN大阪なんば日本橋: dataid='281', state='27', substateid='10'>
0.307692%: <Hotel 東横INN新大阪中央口新館: dataid='96', state='27', substateid='9'>
0.307692%: <Hotel 東横INN新大阪中央口本館: dataid='16', state='27', substateid='9'>
0.285714%: <Hotel 東横INN大阪阪急十三駅西口: dataid='165', state='27', substateid='9'>
0.235294%: <Hotel 東横INN大阪なんば府立体育会館西: dataid='55', state='27', substateid='10'>

Choose:
<Hotel 東横INN大阪船場: dataid='47', state='27', substateid='10'>
```

### By id

```python
>>> hotel = ToyokoInn(id=218)
>>> print hotel
<Hotel 東横INN大阪JR野田駅前: dataid='218', state='27', substateid='8'>
```

## Query rooms by date

```python
>>> rooms = hotel.rooms(year=2016, month=12, day=31)
>>> for r in rooms:
...     print r

<Room vod★カップルプラン♪お得にビデオ見放題！ 喫煙エコノミーダブル: <Member: price=8348, remain=4>, <Guest: price=8763, remain=4>>
<Room 喫煙ダブル: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room 禁煙ハートフルツイン: <Member: price=9120, remain=0>, <Guest: price=9600, remain=0>>
<Room 禁煙エコノミーダブル: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 喫煙ダブル: <Member: price=9298, remain=0>, <Guest: price=9763, remain=0>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 禁煙ダブル: <Member: price=9298, remain=0>, <Guest: price=9763, remain=0>>
<Room 喫煙ツイン: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 禁煙エコノミーダブル: <Member: price=8348, remain=0>, <Guest: price=8763, remain=0>>
<Room 禁煙ツイン: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room 禁煙ダブル: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room 喫煙エコノミーダブル: <Member: price=7885, remain=4>, <Guest: price=8300, remain=4>>
```

### Options

+ @people: Number of people in one room, default is 2
+ @num: Number of rooms, default is 1
+ @stay: Number of days, default is 1

```python
>>> rooms = hotel.rooms(year=2016, month=12, day=31, num=2, stay=2, people=1)
>>> for r in rooms:
...     print r

<Room 喫煙ダブル: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
<Room vod・映ガール集合★お得にビデオ見放題！ 禁煙シングル: <Member: price=7398, remain=2>, <Guest: price=7763, remain=2>>
<Room 【VISAギフト券付】ビジネスパック100★禁煙シングル: <Member: price=8035, remain=2>, <Guest: price=8400, remain=2>>
<Room 禁煙ダブル: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
<Room 【VOD】お部屋が映画館に！２００作品のビデオ見放題♪ 禁煙シングル: <Member: price=7398, remain=2>, <Guest: price=7763, remain=2>>
<Room 【VISA3000+VOD】出張パック300★禁煙シングル: <Member: price=10698, remain=2>, <Guest: price=11063, remain=2>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 喫煙ダブル: <Member: price=8348, remain=0>, <Guest: price=8763, remain=0>>
<Room 【VISA3000+VOD】出張パック300★喫煙シングル: <Member: price=10698, remain=3>, <Guest: price=11063, remain=3>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 禁煙エコノミーダブル: <Member: price=7398, remain=0>, <Guest: price=7763, remain=0>>
<Room 喫煙エコノミーダブル: <Member: price=6935, remain=0>, <Guest: price=7300, remain=0>>
<Room 【VISAギフト券付】ビジネスパック100★喫煙シングル: <Member: price=8035, remain=3>, <Guest: price=8400, remain=3>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 喫煙エコノミーダブル: <Member: price=7398, remain=0>, <Guest: price=7763, remain=0>>
<Room 禁煙シングル: <Member: price=6935, remain=2>, <Guest: price=7300, remain=2>>
<Room 禁煙エコノミーダブル: <Member: price=6935, remain=0>, <Guest: price=7300, remain=0>>
<Room 【VISA1000+VOD】出張パック100★喫煙シングル: <Member: price=8498, remain=3>, <Guest: price=8863, remain=3>>
<Room 【VISAギフト券付】ビジネスパック300★喫煙シングル: <Member: price=10235, remain=3>, <Guest: price=10600, remain=3>>
<Room 【VISA2000+VOD】出張パック200★喫煙シングル: <Member: price=9598, remain=3>, <Guest: price=9963, remain=3>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 禁煙ダブル: <Member: price=8348, remain=0>, <Guest: price=8763, remain=0>>
<Room 【VISA2000+VOD】出張パック200★禁煙シングル: <Member: price=9598, remain=2>, <Guest: price=9963, remain=2>>
<Room 【VISAギフト券付】ビジネスパック200★禁煙シングル: <Member: price=9135, remain=2>, <Guest: price=9500, remain=2>>
<Room 禁煙ツイン: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
<Room 【VISAギフト券付】ビジネスパック200★喫煙シングル: <Member: price=9135, remain=3>, <Guest: price=9500, remain=3>>
<Room 【VISAギフト券付】ビジネスパック300★禁煙シングル: <Member: price=10235, remain=2>, <Guest: price=10600, remain=2>>
<Room 喫煙シングル: <Member: price=6935, remain=3>, <Guest: price=7300, remain=3>>
<Room 禁煙ハートフルツイン: <Member: price=8170, remain=0>, <Guest: price=8600, remain=0>>
<Room vod・映ガール集合★お得にビデオ見放題！ 喫煙シングル: <Member: price=7398, remain=3>, <Guest: price=7763, remain=3>>
<Room 【VOD】お部屋が映画館に！２００作品のビデオ見放題♪ 喫煙シングル: <Member: price=7398, remain=3>, <Guest: price=7763, remain=3>>
<Room 喫煙ツイン: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
<Room 【VISA1000+VOD】出張パック100★禁煙シングル: <Member: price=8498, remain=2>, <Guest: price=8863, remain=2>>
```
