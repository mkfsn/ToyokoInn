# Toyoko Inn

Simple script to fetch reservable rooms.

# Dependency

* python-pip

# Installation

Install required packages.

```
$ pip -r requirement.txt
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
<Hotel: 東横INN大阪JR野田駅前 dataid='218', state='27', substateid='8'>
```

### Candidates

```python
>>> hotel = ToyokoInn("大阪")
Candidates are:
0.444444%: 東横INN大阪船場, id = 47
0.428571%: 東横INN大阪船場2, id = 292
0.400000%: 東横INN大阪船場東, id = 39
0.400000%: 東横INN大阪梅田東, id = 138
0.363636%: 東横INN大阪伊丹空港, id = 261
0.363636%: 東横INN大阪鶴橋駅前, id = 257
0.363636%: 東横INN大阪通天閣前, id = 279
0.363636%: 東横INN大阪心斎橋西, id = 23
0.363636%: 東横INN新大阪駅東口, id = 260
0.342857%: 東横INN大阪JR野田駅前, id = 218
0.333333%: 東横INN大阪谷四交差点, id = 164
0.307692%: 東横INN大阪なんば日本橋, id = 281
0.307692%: 東横INN新大阪中央口新館, id = 96
0.307692%: 東横INN新大阪中央口本館, id = 16
0.296296%: 東横INN大分駅前, id = 151
0.296296%: 東横INN大和駅前, id = 136

Choose:
東横INN大阪船場, id = 47
```

### By id

```python
>>> hotel = ToyokoInn(id=218)
>>> print hotel
<Hotel: 東横INN大阪JR野田駅前 dataid='218', state='27', substateid='8'>
```

## Query rooms by date

```python
>>> rooms = hotel.rooms(year=2016, month=12, day=31, member=False)
>>> for r in rooms:
...     print r

<Room vod★カップルプラン♪お得にビデオ見放題！ 喫煙エコノミーダブル: <Member: price=8348, remain=0>, <Guest: price=8763, remain=0>>
<Room 喫煙ダブル: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room 禁煙ハートフルツイン: <Member: price=9120, remain=0>, <Guest: price=9600, remain=0>>
<Room 禁煙エコノミーダブル: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 喫煙ダブル: <Member: price=9298, remain=0>, <Guest: price=9763, remain=0>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 禁煙ダブル: <Member: price=9298, remain=0>, <Guest: price=9763, remain=0>>
<Room 喫煙ツイン: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room vod★カップルプラン♪お得にビデオ見放題！ 禁煙エコノミーダブル: <Member: price=8348, remain=0>, <Guest: price=8763, remain=0>>
<Room 禁煙ツイン: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room 禁煙ダブル: <Member: price=8835, remain=0>, <Guest: price=9300, remain=0>>
<Room 喫煙エコノミーダブル: <Member: price=7885, remain=0>, <Guest: price=8300, remain=0>>
```
