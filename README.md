# Toyoko Inn

Simple script to fetch reservable rooms.

# Usage

```python
hotel = ToyokoInn(u"大阪JR野田駅前")
rooms = hotel.room(date={'year': 2016, 'month': 12, 'day': 31},
                   member=False)
```
