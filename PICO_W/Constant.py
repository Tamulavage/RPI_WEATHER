import collections
#MQ-135
gasses= collections.namedtuple('gasses',['name','para','parb'])
CO2 = gasses(name='CO2',para=116.60,parb=-2.769)
ALCOHOL = gasses(name='Alcohol',para=77.255,parb=-3.18)
AMMONIA = gasses(name='Ammonia',para=102.2,parb=-2.473)
Smoke = gasses(name='Smoke',para=38.83,parb=-3.19)
CO = gasses(name='CO',para=116.60,parb=-2.769) # WRONG PARA and PARB