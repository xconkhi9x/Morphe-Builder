import os, sys, requests, glob

webhook = os.environ.get("DISCORD_WEBHOOK")
if not webhook:
    print("No DISCORD_WEBHOOK found.")
    sys.exit(0)

repo = os.environ.get("GITHUB_REPOSITORY", "xconkhi9x/Morphe-Builder")
tag = os.environ.get("RELEASE_TAG", "")
run_id = os.environ.get("GITHUB_RUN_ID", "")

# Tim cac file output
files = glob.glob("./output/**/*.apk", recursive=True) + glob.glob("./output/**/*.zip", recursive=True)
if not files and not tag:
    print("No artifacts found to report.")
    sys.exit(0)

fields = []
for f in sorted(files):
    name = os.path.basename(f)
    size_mb = round(os.path.getsize(f) / (1024 * 1024), 1)
    
    if tag:
        dl_url = f"https://github.com/{repo}/releases/download/{tag}/{name}"
        link_text = f"⬇️ [Tải trực tiếp ({size_mb} MB)]({dl_url})"
    else:
        link_text = f"📦 {size_mb} MB"
        
    fields.append({
        "name": f"📱 {name}",
        "value": link_text,
        "inline": False
    })

title = f"🎉 Morphe Build Mới: {tag}" if tag else "🎉 Morphe Build Hoàn Tất!"
release_page = f"https://github.com/{repo}/releases/tag/{tag}" if tag else f"https://github.com/{repo}/releases"

embed = {
    "title": title,
    "url": release_page,
    "description": "Các bản dựng APK/Module đã hoàn tất! Cậu Chủ có thể bấm trực tiếp vào link dưới đây để tải về máy:",
    "color": 3447003,
    "fields": fields[:25],
    "footer": {
        "text": f"Morphe Multi-App Builder • Tự động ngày 1 hàng tháng"
    }
}

payload = {"embeds": [embed]}
r = requests.post(webhook, json=payload)
print(f"Discord notification sent: {r.status_code}")
