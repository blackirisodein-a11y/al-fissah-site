"""Inventaire de la chaîne YouTube de l'école (exécuté par l'action GitHub « Inventaire YouTube »).
Part d'une vidéo connue, retrouve la chaîne, ses playlists et les vidéos de chaque playlist,
puis imprime un JSON. Aucune clé d'API : lecture des pages publiques."""
import json, re, sys, urllib.request

VIDEO = sys.argv[1] if len(sys.argv) > 1 else "MNiWkEPoGNw"
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
     "Accept-Language": "fr-FR,fr;q=0.9,ar;q=0.8,en;q=0.7", "Cookie": "CONSENT=YES+cb; SOCS=CAI"}

def page(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40).read().decode("utf-8", "replace")

def initial_data(html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    return json.loads(m.group(1)) if m else {}

def walk(node, key):
    """Tous les sous-objets qui possèdent la clé `key`."""
    if isinstance(node, dict):
        if key in node:
            yield node
        for v in node.values():
            yield from walk(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v, key)

def text(t):
    if not isinstance(t, dict): return ""
    if "simpleText" in t: return t["simpleText"]
    return "".join(r.get("text", "") for r in t.get("runs", []))

# Chaîne : par oEmbed (author_url), puis identifiant UC… lu sur la page de la chaîne
oe = json.loads(page(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={VIDEO}&format=json"))
cname, curl = oe.get("author_name", ""), oe.get("author_url", "")
chtml = page(curl + "/playlists")
m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]+)"', chtml)
if not m:
    print("=====DEBUG=====", curl, len(chtml), re.sub(r"\s+", " ", chtml[:1500]))
    sys.exit(1)
cid = m.group(1)
out = {"channel": {"id": cid, "name": cname, "url": curl}, "playlists": [], "latest": []}

# Playlists de la chaîne
d = initial_data(chtml)
if not d:
    print("=====DEBUG===== pas de ytInitialData", re.sub(r"\s+", " ", chtml[:1500]))
seen = set()
for r in list(walk(d, "playlistId")):
    pid = r.get("playlistId")
    if not pid or pid in seen or not pid.startswith("PL"): continue
    title = text(r.get("title")) if isinstance(r.get("title"), dict) else r.get("title", "")
    if not title:
        continue
    seen.add(pid)
    out["playlists"].append({"id": pid, "title": title, "count": text(r.get("videoCountText")) or text(r.get("videoCountShortText")), "videos": []})

for r in walk(d, "lockupViewModel"):
    lv = r["lockupViewModel"]; pid = lv.get("contentId", "")
    if not pid.startswith("PL") or pid in seen: continue
    seen.add(pid)
    title = lv.get("metadata", {}).get("lockupMetadataViewModel", {}).get("title", {}).get("content", "")
    out["playlists"].append({"id": pid, "title": title, "count": "", "videos": []})
out["debug_playlist_keys"] = sorted({k for k in ("gridPlaylistRenderer", "lockupViewModel", "playlistRenderer") if next(walk(d, k), None)})

# Toutes les vidéos de la chaîne (page /videos + continuations)
def innertube(token):
    body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": "2.20240701.00.00", "hl": "fr"}}, "continuation": token}).encode()
    req = urllib.request.Request("https://www.youtube.com/youtubei/v1/browse?prettyPrint=false", data=body, headers={**H, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode("utf-8"))
def collect(node, acc, seen_ids):
    for r in walk(node, "videoRenderer"):
        v = r["videoRenderer"]; vid = v.get("videoId")
        if vid and vid not in seen_ids:
            seen_ids.add(vid); acc.append({"id": vid, "title": text(v.get("title")), "len": text(v.get("lengthText")), "when": text(v.get("publishedTimeText"))})
    for r in walk(node, "lockupViewModel"):
        lv = r["lockupViewModel"]; vid = lv.get("contentId", "")
        if lv.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO" and vid and vid not in seen_ids:
            seen_ids.add(vid); acc.append({"id": vid, "title": lv.get("metadata", {}).get("lockupMetadataViewModel", {}).get("title", {}).get("content", ""), "len": "", "when": ""})
    toks = [r["continuationCommand"]["token"] for r in walk(node, "continuationCommand") if r["continuationCommand"].get("token")]
    return toks[0] if toks else None
try:
    dv = initial_data(page(curl + "/videos")); allv = []; sid = set()
    tok = collect(dv, allv, sid); n = 0
    while tok and n < 40:
        n += 1
        try: tok = collect(innertube(tok), allv, sid)
        except Exception as e: out["videos_error"] = str(e); break
    out["videos"] = allv
except Exception as e:
    out["videos_error"] = str(e)

# Vidéos de chaque playlist (jusqu'à 100 par page)
for pl in out["playlists"]:
    try:
        dp = initial_data(page(f"https://www.youtube.com/playlist?list={pl['id']}"))
    except Exception as e:
        pl["error"] = str(e); continue
    vs = []
    for r in walk(dp, "playlistVideoRenderer"):
        v = r["playlistVideoRenderer"]
        vs.append({"id": v.get("videoId"), "title": text(v.get("title")), "len": text(v.get("lengthText"))})
    pl["videos"] = vs
    hdr = next(walk(dp, "playlistHeaderRenderer"), None)
    if hdr:
        pl["desc"] = text(hdr["playlistHeaderRenderer"].get("descriptionText"))

# Dernières vidéos de la chaîne (flux RSS, 15 max)
try:
    rss = page(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
    for m in re.finditer(r"<entry>.*?<yt:videoId>([^<]+)</yt:videoId>.*?<title>([^<]*)</title>.*?<published>([^<]+)</published>", rss, re.S):
        out["latest"].append({"id": m.group(1), "title": m.group(2), "published": m.group(3)[:10]})
except Exception as e:
    out["latest_error"] = str(e)

print("=====JSON=====")
print(json.dumps(out, ensure_ascii=False))
print("=====FIN=====")
