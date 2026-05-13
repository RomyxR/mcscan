from mcstatus import JavaServer
import re
import asyncio
from tqdm.asyncio import tqdm
import json

async def server_cheсk(ip: str, port: int, semaphore: asyncio.Semaphore, pbar: tqdm):
    async with semaphore: 
        try:
            server = await JavaServer.async_lookup(f"{ip}:{port}")
            status = await server.async_status()
            server_overview = {
                'ip': ip,
                "port": port,
                "online": status.players.online,
                "version": status.version.name,
                "motd": re.sub(r'§.', '', status.description),
                "ping": status.latency,
                }
            
            pbar.write(str(server_overview))

            with open("servers.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(server_overview, ensure_ascii=False) + "\n")

        except (asyncio.TimeoutError, Exception):
            pass
        finally:
            pbar.update(1)

async def main():
    ips = [
        # playit.gg
        '147.185.221.211',
        '147.185.221.223',
        '147.185.221.31',
        '147.185.221.30',
        '147.185.221.29',
        # after-life.host
        '65.21.24.204',
        # gamely.pro
        '213.171.18.225',
        # hosting-minecraft.pro
        'free.joinserver.xyz',
        # rustix.me
        "f1.rustix.me",
        # rionix.cloud
        "d1.rionix.cloud",
        # cloudblaze.org
        "free.cloudblaze.org",

    ]
    ports = range(1024, 65535)
    
    semaphore = asyncio.Semaphore(1024)

    with open("servers.jsonl", "w", encoding="utf-8") as f:
        pass

    total_tasks = len(ips) * len(ports)

   
    with tqdm(total=total_tasks, unit="port") as pbar:
        tasks = []
        for ip in ips:
            for port in ports:
                tasks.append(server_cheсk(ip, port, semaphore, pbar))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nСканирование остановлено.")

