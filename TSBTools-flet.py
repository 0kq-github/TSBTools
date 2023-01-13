import flet as ft
from tsb.client import tsbAPI

tsb = tsbAPI()
tsb_md = ""
tsb.fetch_release()
for v in tsb.releases.values():
    tsb_md += f"# {v['name']}\n{v['body']}\n"

def main(page: ft.Page):
    page.scroll = "auto"
    page.add(
        ft.Markdown(
            tsb_md,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: page.launch_url(e.data),
        )
    )

ft.app(target=main)