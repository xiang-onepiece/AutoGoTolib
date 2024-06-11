

import ddddocr;

# ocr = ddddocr.DdddOcr()

# with open('a.png', 'rb') as f:
#     img_bytes = f.read()
#
# res = ocr.classification(img_bytes)
# print("结果：")
# print(res)


# import time
#
# timestamp = int(time.time() * 1000)
# print(timestamp)


import random
# 从a-zA-Z0-9生成指定数量的随机字符：
ran_str = ''.join(random.sample('0123456789ABCDEFGHJKLMNOPQRSTUVWXYZI', 24))
print(ran_str)
