import asyncio

async def func1(x):
    
    while x >= 0:
        
        print(x)
        
        x-=1
        
async def func2(y):
    
    while y<=100:
    
        print(y)
        
        y*=1.5
        
async def run(x, y):
    
    vals = await asyncio.gather(func1(x), func2(y))
    
    print(vals)

asyncio.run(run(10, 2))
    