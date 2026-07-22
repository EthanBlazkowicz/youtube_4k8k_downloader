from pytubefix import YouTube
from pytubefix.cli import on_progress

from rich.console import Console
from rich.table import Table

import os
import sys
import time
import subprocess
import ffmpeg
import datetime

console = Console()


def PrintOK(text):
    console.log(f"[green]{text}")


def PrintInfo(text):
    console.log(f"[blue]{text}")


def PrintWarning(text):
    console.log(text, style="#EE9427")


def PrintRule(text):
    console.rule(f"[bold blue]{text}")


# console.print(
#     "[blue]Github URL: [green]https://github.com/12343954/youtube_4k8k_downloader")

print('')
console.print(
    "[bold blue]YOUTUBE [green]4K/8K [#EE9427]Downloader")
print('')

# https://www.youtube.com/watch?v=tUjIwYeVlQc
url_4k = input('Enter a youtube url (prefer 4K or 8K): ')
if url_4k is None:
    url_4k = 'https://www.youtube.com/watch?v=R3GfuzLMPkA'

url_8k = 'https://www.youtube.com/watch?v=6I5nor_880M'

proxies = {
    # 'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

keys = [
    # "_monostate",
    "itag",
    "mime_type",
    "resolution",
    "fps",
    # "codecs",
    # "type",
    # "subtype",
    "video_codec",
    # "audio_codec",
    # "is_otf",
    "bitrate",
    # "_filesize",
    # "_filesize_kb",
    "_filesize_mb",
    # "_filesize_gb",
    # "is_dash",
    # "abr",
    # "_width",
    # "_height",
    # "is_3d",
    # "is_hdr",
    # "is_live",
    # "includes_multiple_audio_tracks",
    # "is_default_audio_track",
    # "audio_track_name",
    "url",
]

# Payload: {
#     serviceIntegrityDimensions: {
#         poToken: "MnQenNfHb5GLBh6kUYK8yaq-UhMBtrpjdlG668nFHu8CpDhsV2aAaU32sIbval9e4KUcX1nsQBbrKasXu0lYmIdhvz6E1ZOnQKGdK6TILzDZ2aqC9UDBx4wMDzIbxSlVpRqaKWa6dnIdxEFeeTHXkBRLhSP77Q=="
#     }
#     context: {
#         client: {
#             visitorData: "CgtpVXNqTE5LZDZONCjknK-6BjIKCgJISxIEGgAgGg%3D%3D"
#         }
#     }
# }

yt = YouTube(url_4k, on_progress_callback=on_progress)
# yt = YouTube(url_8k, proxies=proxies, on_progress_callback=on_progress,
#             use_po_token=True)

# Info(f'\n\nTitle= {yt.title}\n')
# title = yt.title

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Title", style="magenta")
table.add_row(yt.title)
console.print(table)
time.sleep(1)

# for key in yt.streams[0].__dict__.keys():print(key)
# time.sleep(1)

RESOLUTIONS = [{"id": 0, "label": "8K", "resv": "4320p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}},
               {"id": 1, "label": "4K", "resv": "2160p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}},
               {"id": 2, "label": "2.5K", "resv": "1440p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}},
               {"id": 3, "label": "2K", "resv": "1080p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}},
               {"id": 4, "label": "1K", "resv": "720p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}},
               {"id": 5, "label": "DV", "resv": "480p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}},
               {"id": 6, "label": "CD", "resv": "320p", "size": "0", "exist": "❌", "codecs": [], "raw_codecs": [], "codec_sizes": {}}]

CODEC_NAMES = {"av01": "AV1", "avc1": "H.264", "vp9": "VP9", "vp09": "VP9", "hvc1": "H.265"}

def short_codec(raw):
    """Map raw codec string like 'av01.0.12M.08' to a readable name like 'AV1'."""
    for prefix, name in CODEC_NAMES.items():
        if raw.startswith(prefix):
            return name
    return raw

for i, k in enumerate(RESOLUTIONS):
    streams = yt.streams.filter(res=k["resv"], only_video=True)
    if not streams:
        continue
    ordered = streams.order_by("bitrate").desc()
    raw_codecs = list(dict.fromkeys(s.video_codec for s in ordered if s.video_codec))
    codec_sizes = {}
    for s in ordered:
        if s.video_codec and s.video_codec not in codec_sizes:
            codec_sizes[s.video_codec] = str(getattr(s, "_filesize_mb"))
    RESOLUTIONS[i]["size"] = list(codec_sizes.values())[0]
    RESOLUTIONS[i]["exist"] = "✅"
    RESOLUTIONS[i]["codecs"] = [short_codec(c) for c in raw_codecs]
    RESOLUTIONS[i]["raw_codecs"] = raw_codecs
    RESOLUTIONS[i]["codec_sizes"] = codec_sizes

table = Table(show_header=True, header_style="bold magenta")
# table.add_column(["8K", "4K", "2.5K", "2K"])
# table.add_row(*Resolutions)
# table.add_row(*['✅' if VDO_8K else '❌',
#                 '✅' if VDO_4K else '❌',
#                 '✅' if VDO_1440P else '❌',
#                 '✅' if VDO_1080P else '❌',])

for col in list(map(lambda x: f'{x["label"]}/{x["resv"]}', RESOLUTIONS)):
    table.add_column(col)

# table.add_row(*list(map(lambda x: x["resv"], RESOLUTIONS)))
table.add_row(
    *list(map(lambda x: "❌" if x["size"] == "0" else f'✅ {x["size"]} MB [{", ".join(x["codecs"])}]', RESOLUTIONS)))
console.print(table)
time.sleep(1)

list2 = list(filter(lambda x: x["size"] != "0", RESOLUTIONS))
# print("Select a item to download:\n", '\n'.join([f'\t{str(i+1)}. {x["label"]}/{x["resv"]}  {x["size"]}MB' for i, x in enumerate(list2)]))
PrintWarning("Select a item to download(default is first item):")

# PrintOK('\n'.join(
#     [f'\t{str(i+1)}. {x["label"]}/{x["resv"]}  {x["size"]} MB' for i, x in enumerate(list2)]))

for i, x in enumerate(list2):
    codec_parts = ", ".join(
        f"{short_codec(c)}/{x['codec_sizes'][c]}MB" for c in x['raw_codecs'])
    codecs_str = f" [{codec_parts}]" if x['raw_codecs'] else ""
    console.print(
        f"\t[blue]{str(i+1)}.  [green]{str(x['label']).rjust(4)}/{str(x['resv']).ljust(6)}  {codecs_str}")

index = input('Your chose: ')
if (index is None):
    index = 1
    PrintWarning("You input nothing, the first item will be downloaded!")
elif index not in [str(i + 1) for i, x in enumerate(list2)]:
    index = 1
    PrintWarning(
        "You entered the wrong option, the first item will be downloaded!")

select_item = list2[int(index) - 1]

available_codecs = select_item["codecs"]
raw_codecs = select_item["raw_codecs"]
codec_sizes = select_item["codec_sizes"]
chosen_raw = raw_codecs[0] if raw_codecs else None
if len(available_codecs) > 1:
    PrintWarning("Select codec:")
    for ci, c in enumerate(available_codecs):
        raw = raw_codecs[ci]
        console.print(f"\t[blue]{str(ci+1)}.  [green]{c}[/green] ({codec_sizes.get(raw, '?')} MB)")
    codec_index = input('Codec choice: ')
    if codec_index in [str(n + 1) for n in range(len(available_codecs))]:
        chosen_raw = raw_codecs[int(codec_index) - 1]

chosen_size = codec_sizes.get(chosen_raw, select_item["size"])

PrintRule(
    f'✅ {index}. {select_item["label"]}/{select_item["resv"]} {short_codec(chosen_raw)} {chosen_size} MB will be downloaded ... ✅')

captions_list = list(yt.captions)
selected_caption = None
if captions_list:
    download_subs = input('Download subtitles? (y/N): ').strip().lower()
    if download_subs in ('y', 'yes'):
        print('')
        PrintWarning('Available subtitles:')
        for ci, c in enumerate(captions_list):
            console.print(f"\t[blue]{str(ci+1)}.  [green]{c.name}")
        sub_index = input('Subtitle choice: ')
        if sub_index and sub_index in [str(n + 1) for n in range(len(captions_list))]:
            selected_caption = captions_list[int(sub_index) - 1]

time.sleep(1)

default_output = os.path.join(os.path.expanduser('~'), 'Downloads')
output_dir = input(f'Output directory (default: {default_output}): ').strip()
if not output_dir:
    output_dir = default_output
output_dir = os.path.expanduser(output_dir)
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.datetime.now().timestamp()
temp_audio = f'temp_{timestamp}.mp3'
temp_video = f'temp_{timestamp}.mp4'
output_ext = '.mp4' if chosen_raw and chosen_raw.startswith('avc1') else '.mkv'
merge_file = f'_merge_{timestamp}{output_ext}'

opener = "open" if sys.platform == "darwin" else "xdg-open" if sys.platform == 'linux' else 'start'
# subprocess.call([opener, output_dir])

if os.path.exists(os.path.join(output_dir, f'{yt.title}{output_ext}')):
    os.remove(os.path.join(output_dir, f'{yt.title}{output_ext}'))
if os.path.exists(os.path.join(output_dir, temp_audio)):
    os.remove(os.path.join(output_dir, temp_audio))
if os.path.exists(os.path.join(output_dir, temp_video)):
    os.remove(os.path.join(output_dir, temp_video))


audioes = yt.streams.filter(
    only_audio=True, mime_type="audio/mp4").order_by("abr").desc()
audio = audioes.first()

PrintInfo(
    f'Step 1/3. Downloading audio file, size = {str(getattr(audio, "_filesize_mb"))} MB ...')
t = time.time()
audio.download(output_path=output_dir, filename=temp_audio, max_retries=3)
PrintOK(f'Step 1/3. Done, ETA= {time.time() - t:.8f}s')

# region //download the heightest resv
# if VDO_8K:
#     PrintInfo('8K Video downloading ...')
#     video = yt.streams.filter(res='4320p').first()
# elif not VDO_8K and VDO_4K:
#     PrintInfo('4K Video downloading ...')
#     video = yt.streams.filter(res='2160p').first()
# elif not VDO_8K and not VDO_4K and VDO_1440P:
#     PrintInfo('1440P Video downloading ...')
#     video = yt.streams.filter(res='1440p').first()
# elif not VDO_8K and not VDO_4K and not VDO_1440P and VDO_1080P:
#     PrintInfo('1080P Video downloading ...')
#     video = yt.streams.filter(res='1080p').first()
# elif not VDO_8K and not VDO_4K and not VDO_1440P and not VDO_1080P and VDO_720P:
#     PrintInfo('720P Video downloading ...')
#     video = yt.streams.filter(res='720p').first()
# elif not VDO_8K and not VDO_4K and not VDO_1440P and not VDO_1080P and not VDO_720P and VDO_480P:
#     PrintInfo('480P Video downloading ...')
#     video = yt.streams.filter(res='480p').first()
# elif not VDO_8K and not VDO_4K and not VDO_1440P and not VDO_1080P and not VDO_720P and not VDO_480P and VDO_320P:
#     PrintInfo('320P Video downloading ...')
#     video = yt.streams.filter(res='320p').first()
# else:
#     PrintWarning('❌ NO HD Video download!')
# endregion

PrintInfo(
    f'Step 2/3. Downloading {select_item["resv"]} ({short_codec(chosen_raw)}) video file, size = {chosen_size} MB ...')
video = yt.streams.filter(res=select_item["resv"], video_codec=chosen_raw).first()

t = time.time()
video.download(output_path=output_dir, filename=temp_video, max_retries=3)
PrintOK(f'Step 2/3. Done, ETA= {time.time() - t:.8f}s')

probe = ffmpeg.probe(os.path.join(output_dir, temp_video))
info = probe['streams'][0]

fps = str(info['r_frame_rate']).split('/')[0]
# or
# fps = str(getattr(video, "fps"))

table = Table(show_header=True, header_style="bold magenta",
              title="Media Information")
table.add_column("FPS", style="magenta")
table.add_column("Encoder", style="magenta")
table.add_column("Resolution", style="magenta")
table.add_column("Ratio", style="magenta")
table.add_row(fps, info['codec_long_name'],
              f'{info['width']} x {info['height']}', info['display_aspect_ratio'])
console.print(table)
time.sleep(1)
# OK('video info:')
# Info(f'{'fps': >10} = {fps}')
# Info(f'{'encoder': >10} = {info['codec_long_name']}')
# Info(f'{'resolution': >10} = {info['width']} x {info['height']}')
# Info(f'{'ratio': >10} = {info['display_aspect_ratio']}')

# info
# ffmpeg -i temp1.mp4 -i temp1.mp3 -y -r 30 1.mp4
# ffmpeg -i temp1.mp4 -i temp1.mp3 -r 30 -vf yadif,format=yuv420p -force_key_frames "expr:gte(t,n_forced/2)" -c:v libx264 -crf 18 -bf 2 -c:a aac -q:a 1 -ac 2 -ar 48000 -use_editlist 0 -movflags +faststart out.mp4

# cmd = 'ffmpeg -i temp_vid.mp4 -i temp_voice.wav -c:v copy -c:a aac -strict experimental -strftime 1 ' + dt_file_name

PrintInfo('Step 3/3. Mergeing ...')
cmd = (' ').join(['ffmpeg',
                  '-i', os.path.join(output_dir, temp_video),
                  '-i', os.path.join(output_dir, temp_audio),
                  '-c:v', 'copy',
                  '-c:a', 'copy',
                  '-y',
                  os.path.join(output_dir, merge_file)
                  ])

t = time.time()
p = subprocess.Popen(cmd.split(),
                     stdin=subprocess.PIPE,
                     # creationflags=subprocess.CREATE_NO_WINDOW
                     )

p.wait()

os.rename(os.path.join(output_dir, merge_file),
          os.path.join(output_dir, f'{yt.title}{output_ext}'))

if os.path.exists(os.path.join(output_dir, temp_audio)):
    os.remove(os.path.join(output_dir, temp_audio))
if os.path.exists(os.path.join(output_dir, temp_video)):
    os.remove(os.path.join(output_dir, temp_video))

PrintOK('Step 3/3. Done')

if selected_caption:
    subtitle_path = os.path.join(output_dir, f'{yt.title}.srt')
    try:
        srt_content = selected_caption.generate_srt_captions()
        with open(subtitle_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        PrintOK(f'Subtitles saved: {subtitle_path}')
    except Exception:
        PrintWarning('Failed to save subtitles')

PrintOK('All Done !!!')
