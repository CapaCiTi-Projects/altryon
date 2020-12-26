import random
import pprint

names = [
    "Adrin Strydom", "Jesse Boise", "Nadeem Dante", "Ntombizodwa Thwala",
    "Philip Harteveld", "Scott Dennis", "Zaakirah", "Zaid Zama"
]

d = {n: [] for n in names}
nums = list(range(30))
num_len = len(nums)
while nums:
    name = names[random.randint(0, len(names)-1)]
    num = nums[random.randint(0, len(nums)-1)]
    print((num_len / ((num_len // len(names)) * len(names))))
    if (len(d[name]) > 3) and ((num_len / ((num_len // len(names)) * len(names))) <= 1.25):
        continue
    print(d)
    nums.remove(num)
    d[name].append(num+1)
# print(d)
pprint.pprint(d)
