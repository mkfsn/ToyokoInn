# Toyoko Inn

Simple script to fetch reservable rooms.

# Usage

```python
hotel = ToyokoInn(u"大阪JR野田駅前")
rooms = hotel.room(date={'year': 2016, 'month': 12, 'day': 31},
                   member=False)
for r in rooms:
    print r

# vod★カップルプラン♪お得にビデオ見放題！ 喫煙エコノミーダブル 7398 5
# 喫煙ダブル 7885 5
# 禁煙エコノミーダブル 6935 1
# vod★カップルプラン♪お得にビデオ見放題！ 喫煙ダブル 8348 5
# vod★カップルプラン♪お得にビデオ見放題！ 禁煙ダブル 8348 2
# 喫煙ツイン 7885 2
# vod★カップルプラン♪お得にビデオ見放題！ 禁煙エコノミーダブル 7398 1
# 禁煙ダブル 7885 2
# 喫煙エコノミーダブル 6935 5
```
