# I Am Groot

Groot has been working on his computer skills and sent what he claims is an important message but so far we haven't really been able to interpret it. Maybe you can make some sense of it?

## Solution

Examining groot.txt, there are a ton of lines of simply "I Am Groot.". However, depending on the text editor you are using you may also see a lot of random looking characters as well. These are unicode zero-width joiner characters which are not normally visible in text (as they have zero width) but can be used to encode information. Each line has a set of characters to denote the start and end of a block and then eight other characters which denote binary 1 and 0. Decoding these reveals a ZIP file encoded into the text whic contains flag.txt

```python

import re

X = open("groot.txt","rb").read()

matches = re.findall(b"\xef\xbb\xbf(.{24})\xef\xbb\xbf",X)

for m in matches:
    m = m.replace(b"\xe2\x80\x8b",b"0")
    m = m.replace(b"\xe2\x80\x8c",b"1")
    print(hex(int(m,2))[2:].zfill(2),end="")
    
```
