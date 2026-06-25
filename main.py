#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🕉️   HINDU PANCHANG AI VIDEO GENERATOR   🕉️                   ║
║                                                                  ║
║   Sirf yahi ek file chalao — sab apne aap hoga!                 ║
║                                                                  ║
║   NORMAL:     python main.py                                     ║
║   SIRF VIDEO: python main.py --video-only                        ║
║   DATE:       python main.py --date 2026-07-15                   ║
║   SCHEDULER:  python main.py --scheduler                         ║
║   CHECK:      python main.py --check                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys, os, subprocess, importlib
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# ── Auto install ──────────────────────────────────────────────────
def _ensure_libs():
    for module, pkg in {"requests": "requests", "gtts": "gtts"}.items():
        try:
            importlib.import_module(module)
        except ImportError:
            print(f"\n📦 Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install",
                                   "--break-system-packages", "-q", pkg])
            print("✅ Done!\n")
_ensure_libs()

import argparse, datetime, time
from zoneinfo import ZoneInfo

import config.settings as cfg
from core import panchang, script_generator, video_prompts, saver, logger
from core import video_maker


# ═══════════════════════════════════════════════════════════════════
# CORE PIPELINE
# ═══════════════════════════════════════════════════════════════════

def run_pipeline(date_str=None, video_only=False):
    logger.info("━"*50)
    logger.info("PANCHANG VIDEO GENERATOR — START")
    logger.info("━"*50)

    # 1. Panchang
    logger.info("Panchang calculate ho raha hai...")
    p = panchang.calculate(date_str=date_str, timezone=cfg.TIMEZONE)
    p["city"]    = cfg.CITY
    p["channel"] = cfg.CHANNEL_NAME

    logger.ok(f"Date      : {p['date']}")
    logger.ok(f"Var       : {p['var_name']} ({p['var_en']})")
    logger.ok(f"Tithi     : {p['tithi']} | {p['paksha']}")
    logger.ok(f"Nakshatra : {p['nakshatra']}")
    logger.ok(f"Shubh     : {p['shubh_muhurt']}")
    logger.ok(f"Rahu Kaal : {p['rahu_kaal']}")

    # 2. Script
    logger.info("Video script generate ho rahi hai...")
    script = script_generator.generate(
        panchang=p, api_key=cfg.ANTHROPIC_API_KEY, channel_name=cfg.CHANNEL_NAME)
    logger.ok("Script ready!")

    # 3. Video Prompts
    prompts = video_prompts.generate_all(panchang=p, script=script)

    # 4. Save HTML, JSON, txt
    saved = {}
    if not video_only:
        logger.info("HTML/JSON/TXT files save ho rahi hain...")
        saved = saver.save_all(panchang=p, script=script, prompts=prompts, cfg=cfg)
        logger.ok("Support files saved!")

    # 5. ★ ACTUAL VIDEO BANANA ★
    output_dir = ROOT / "output"
    logger.info("★ Actual MP4 video ban rahi hai ★")
    print()
    print("  ┌──────────────────────────────────────────┐")
    print("  │  🎬  VIDEO CREATION IN PROGRESS...        │")
    print("  └──────────────────────────────────────────┘")

    video_path = video_maker.make_video(
        panchang=p,
        script=script,
        output_dir=output_dir
    )

    saved["video"] = video_path

    # ── Final Summary ─────────────────────────────────────────────
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║           ✅  SABKUCH COMPLETE!              ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    if video_path and video_path.exists():
        size_mb = video_path.stat().st_size / (1024*1024)
        print(f"  🎬 VIDEO READY!")
        print(f"     📁 {video_path}")
        print(f"     📦 Size: {size_mb:.1f} MB")
        print()
        print("  ▶️  Yeh video seedha YouTube / Instagram / Reels")
        print("     par upload kar sakte hain!")
    else:
        print("  ⚠️  Automatic video nahi bana (internet ya library issue)")
        print("     → HTML prompts use karein (output/ folder mein)")
        print()
        _print_fallback_sites(p)

    if saved.get("html"):
        print(f"\n  🌐 HTML Preview : output/{saved['html'].name}")
    print()
    print("  🙏 Jai Shri Ram! Aaj ka din shubh ho! 🙏")
    print()
    return saved


def _print_fallback_sites(p):
    print("  ┌─────────────────────────────────────────────┐")
    print("  │  🎬 FALLBACK: Free AI Video Sites           │")
    print("  └─────────────────────────────────────────────┘")
    for name, url, tip in [
        ("InVideo",  "https://invideo.io",       "Hindi videos ke liye best"),
        ("Fliki",    "https://app.fliki.ai",     "Text to video + Hindi voice"),
        ("Canva",    "https://canva.com/video",  "Beautiful templates"),
        ("D-ID",     "https://d-id.com",         "AI Avatar pandit"),
        ("Pictory",  "https://pictory.ai",       "Script to video"),
    ]:
        print(f"  🔗 {name:<10} {url}")
        print(f"               ({tip})")
    print()
    print("  💡 output/video_prompts_*.txt mein ready prompts hain")
    print("     Copy karein aur kisi bhi site pe paste karein!")


# ═══════════════════════════════════════════════════════════════════
# SCHEDULER
# ═══════════════════════════════════════════════════════════════════

def run_scheduler():
    print("\n" + "═"*52)
    print("  ⏰  DAILY AUTO-SCHEDULER")
    print("═"*52)
    print(f"  Roz {cfg.DAILY_RUN_TIME} baje subah apne aap chalega")
    print("  Band karne ke liye: Ctrl+C dabao")
    print("═"*52 + "\n")

    print("▶️  Pehle abhi ek baar chal raha hai...\n")
    run_pipeline()

    print(f"\n⏰ Waiting... roz {cfg.DAILY_RUN_TIME} baje chalega.\n")
    logger.info(f"Scheduler active: {cfg.DAILY_RUN_TIME} daily")

    run_h, run_m = map(int, cfg.DAILY_RUN_TIME.split(":"))
    tz = ZoneInfo(cfg.TIMEZONE)
    last = None

    while True:
        now = datetime.datetime.now(tz)
        if now.hour == run_h and now.minute == run_m and last != now.date():
            print(f"\n🔔 [{now.strftime('%H:%M')}] Scheduled run...")
            run_pipeline()
            last = now.date()
        time.sleep(30)


# ═══════════════════════════════════════════════════════════════════
# CHECK
# ═══════════════════════════════════════════════════════════════════

def run_check():
    import shutil
    print("\n" + "═"*52)
    print("  🔍 SETUP CHECK")
    print("═"*52)
    print(f"  {'✅'} Python          : {sys.version_info.major}.{sys.version_info.minor}")
    print(f"  {'✅'} City            : {cfg.CITY}, {cfg.STATE}")
    print(f"  {'✅'} Timezone        : {cfg.TIMEZONE}")
    print(f"  {'✅'} Daily run       : {cfg.DAILY_RUN_TIME}")
    api = bool(cfg.ANTHROPIC_API_KEY)
    print(f"  {'✅' if api else '⚠️ '} Anthropic API   : {'Set ✅' if api else 'Not set (local mode)'}")

    for pkg in ["PIL", "numpy", "cv2", "imageio"]:
        try:
            importlib.import_module(pkg if pkg != 'PIL' else 'PIL.Image')
            print(f"  ✅ {pkg:<15} : installed")
        except:
            print(f"  ❌ {pkg:<15} : MISSING")

    ffmpeg = shutil.which("ffmpeg")
    print(f"  {'✅' if ffmpeg else '❌'} ffmpeg          : {'found' if ffmpeg else 'NOT FOUND — install karein'}")

    print()
    print("  Settings: config/settings.py")
    print("  Run     : python main.py")
    print("═"*52 + "\n")


# ═══════════════════════════════════════════════════════════════════
# ENTRY
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Hindu Panchang AI Video Generator")
    parser.add_argument("--date",       help="YYYY-MM-DD format")
    parser.add_argument("--scheduler",  action="store_true")
    parser.add_argument("--check",      action="store_true")
    parser.add_argument("--video-only", action="store_true", dest="video_only",
                        help="Sirf video banao, baaki files skip")
    args = parser.parse_args()

    print()
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║  🕉️   Hindu Panchang AI Video Generator  🕉️   ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print()

    if args.check:
        run_check()
    elif args.scheduler:
        run_scheduler()
    else:
        run_pipeline(date_str=args.date, video_only=args.video_only)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Band hua. Jai Shri Ram! 🙏\n")
    except Exception as e:
        logger.err(f"Error: {e}")
        raise
