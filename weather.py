import aiohttp
import asyncio
import pandas as pd


async def function(Api_key, test_city):

    '''
    Преимущество асинхронного подхода: 
    1. Асинхронность: Ожидание ответа от API  не блокирует выполнение других задач.
    2. Программа в целом может обрабатывать несколько запросов одновременно.
    3. Производительность
    4. Асинхронный подход использует меньше потоков, чем таже многопоточность, снижая потребление оперативной памяти.
    5. Асинхронный код легче масштабируется в высоконагруженных системах  и тп.
    6.Гибкость
    '''
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={test_city}&appid={Api_key}&units=metric" 
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                r.raise_for_status()
                zxc = await r.json()

                Rank_data = {
                    "Город": zxc["name"],
                    "Температура (°C)": zxc["main"]["temp"],
                    "По ощущениям (°C)": zxc["main"]["feels_like"],
                    "Влажность (%)": zxc["main"]["humidity"],
                    "Описание Погоды": zxc["weather"][0]["description"],
                    "Скорость ветра (m/s)": zxc["wind"]["speed"]
                }

                qwe = pd.DataFrame([Rank_data])
                print("Данные Погоды:")
                print(qwe)
    except aiohttp.ClientError as e :
        print(f"HTTP Request failed:", {e})
    
async def main():
    Api_key = "9d961bd7afa2be78e31d239aafc53c14"
    test_city = "Ekaterinburg"

    await function(Api_key, test_city)




if __name__ == '__main__':
    asyncio.run(main())