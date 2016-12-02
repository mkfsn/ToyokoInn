# Toyoko Inn

Simple script to fetch reservable rooms.

# Usage

```python
>>> from ToyokoInn import ToyokoInn
>>> hotel = ToyokoInn(u"大阪JR野田駅前")
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
