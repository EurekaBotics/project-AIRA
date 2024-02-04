import python_weather
import asyncio
import os

async def getweather(city:str):
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    weather = await client.get(city)
    return str(weather.current)

if __name__ == '__main__':

  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
  print(asyncio.run(getweather("New York"))) # New York? -_-
  