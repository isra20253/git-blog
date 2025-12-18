import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re

URLS = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/post_detail/11/',
]
ITER = 10

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch(url, timeout=10):
    req = Request(url, headers=headers)
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as r:
            data = r.read()
            status = r.getcode()
    except HTTPError as e:
        return None, None, e.code
    except URLError as e:
        return None, None, None
    elapsed = time.perf_counter() - start
    return elapsed, len(data), status


def profile(url):
    print(f"Profiling {url} ({ITER} requests)")
    times = []
    sizes = []
    statuses = []
    first_html = None
    for i in range(ITER):
        t, size, status = fetch(url)
        if t is None:
            print(f"  Request {i+1}: failed (status={status})")
            continue
        print(f"  Request {i+1}: {t*1000:.1f} ms, {size} bytes, status {status}")
        times.append(t)
        sizes.append(size)
        statuses.append(status)
        if first_html is None:
            # store for scraping images
            req = Request(url, headers=headers)
            with urlopen(req, timeout=10) as r:
                first_html = r.read().decode('utf-8', errors='ignore')
    if not times:
        print('  All requests failed for', url)
        return
    import statistics
    print('  Summary:')
    print(f"    count: {len(times)}, min: {min(times)*1000:.1f} ms, avg: {statistics.mean(times)*1000:.1f} ms, max: {max(times)*1000:.1f} ms")
    print(f"    avg size: {statistics.mean(sizes):.1f} bytes")

    # find image URLs in first_html
    if first_html:
        img_srcs = re.findall(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', first_html, re.I)
        imgs = []
        for src in img_srcs:
            if src.startswith('/'):
                full = 'http://127.0.0.1:8000' + src
            elif src.startswith('http'):
                full = src
            else:
                full = 'http://127.0.0.1:8000/' + src
            if full not in imgs:
                imgs.append(full)
        print(f"    Found {len(imgs)} images on first fetch")
        if imgs:
            img_times = []
            for img in imgs:
                t, size, status = fetch(img)
                if t is None:
                    print(f"      Image: {img} -> failed (status={status})")
                    continue
                print(f"      Image: {img} -> {t*1000:.1f} ms, {size} bytes, status {status}")
                img_times.append(t)
            if img_times:
                print(f"      Images summary min/avg/max: {min(img_times)*1000:.1f} / {statistics.mean(img_times)*1000:.1f} / {max(img_times)*1000:.1f} ms")


if __name__ == '__main__':
    for u in URLS:
        profile(u)
        print('')
