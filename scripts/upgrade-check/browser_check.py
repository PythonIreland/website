"""Drive the Wagtail admin and public site in a headless browser.

Usage: python browser_check.py <screenshots-dir>

Environment:
  UPGRADE_CHECK_SERVER_PORT     port of the running server (default 18000)
  UPGRADE_CHECK_ADMIN_PASSWORD  admin password set by seed.py
  CHROMIUM_PATH                 optional Chromium binary; Playwright's bundled
                                browser is used when unset

Exits with status 1 when a step fails.
"""

import os
import re
import sys
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE = f"http://127.0.0.1:{os.environ.get('UPGRADE_CHECK_SERVER_PORT', '18000')}"
PASSWORD = os.environ.get("UPGRADE_CHECK_ADMIN_PASSWORD", "upgrade-check")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# Draftail syncs its hidden form input asynchronously: wait before saving,
# like a human would, or the typed text is not submitted.
DRAFTAIL_SYNC_MS = 800

results = []
console_errors = []
bad_responses = []
steps = []


def step(name):
    def decorator(fn):
        def run(page):
            try:
                fn(page)
                results.append(("PASS", name, ""))
            except Exception as exc:  # noqa: BLE001 - report every failure
                results.append(("FAIL", name, str(exc).splitlines()[0][:300]))
            finally:
                slug = re.sub(r"\W+", "-", name.lower()).strip("-")
                page.screenshot(
                    path=OUT / f"{len(results):02d}-{slug}.png", full_page=True
                )

        steps.append(run)
        return run

    return decorator


def page_id(page, title):
    """Return the id of the page with this title, using the admin search."""
    page.goto(f"{BASE}/admin/pages/search/?q={title}")
    link = page.locator("main").get_by_role("link", name=title, exact=True).first
    return re.search(r"/pages/(\d+)/", link.get_attribute("href")).group(1)


def open_editor(page, title):
    page.goto(f"{BASE}/admin/pages/{page_id(page, title)}/edit/")
    page.wait_for_load_state("networkidle")


def publish(page):
    page.wait_for_timeout(DRAFTAIL_SYNC_MS)
    page.locator("[data-w-dropdown-target='toggle']").last.click()
    page.get_by_role("button", name="Publish").click()
    expect(page.locator(".messages")).to_contain_text("published", timeout=15000)


@step("Admin login")
def login(page):
    page.goto(f"{BASE}/admin/login/")
    page.fill("#id_username", "admin")
    page.fill("#id_password", PASSWORD)
    page.click("button[type=submit]")
    page.wait_for_url(f"{BASE}/admin/")
    expect(page.locator("main")).to_contain_text("Pages")


@step("Page explorer (sidebar)")
def explorer(page):
    page.goto(f"{BASE}/admin/")
    page.wait_for_load_state("networkidle")
    panel = page.locator("#wagtail-sidebar")
    panel.get_by_text("Pages", exact=True).click()
    expect(panel).to_contain_text("Python Ireland", timeout=10000)
    panel.locator("a, button").filter(
        has_text=re.compile("Python Ireland")
    ).last.click()
    expect(panel).to_contain_text("About", timeout=10000)
    expect(panel).to_contain_text("Meetups")


@step("Page listing and search")
def listing(page):
    page.goto(f"{BASE}/admin/pages/{page_id(page, 'Python Ireland')}/")
    expect(page.locator("main")).to_contain_text("About")
    expect(page.locator("main")).to_contain_text("Draft page")
    page.goto(f"{BASE}/admin/pages/search/?q=Conduct")
    expect(page.locator("main")).to_contain_text("Code of Conduct")


@step("Edit rich text and publish an existing page")
def edit_publish(page):
    open_editor(page, "About")
    editor = page.locator(".Draftail-Editor .public-DraftEditor-content").first
    editor.click()
    page.keyboard.press("Control+End")
    page.keyboard.type(" Edited by the upgrade check.", delay=30)
    page.keyboard.press("Enter")
    page.keyboard.press("Control+b")
    page.keyboard.type("Bold line", delay=30)
    expect(editor).to_contain_text("Edited by the upgrade check.")
    publish(page)
    page.goto(f"{BASE}/about/")
    expect(page.locator("body")).to_contain_text("Edited by the upgrade check.")
    bold = page.locator("b, strong").filter(has_text="Bold line")
    assert bold.count() == 1, "bold text missing on the public page"


@step("Create a new page with rich text and publish")
def create_page(page):
    home_id = page_id(page, "Python Ireland")
    page.goto(f"{BASE}/admin/pages/add/core/simplepage/{home_id}/")
    page.wait_for_load_state("networkidle")
    page.fill("#id_title", "Upgrade check page")
    page.get_by_role("button", name=re.compile("Insert a block")).first.click()
    page.get_by_role("option", name=re.compile("Paragraph")).click()
    editor = page.locator(".Draftail-Editor .public-DraftEditor-content").first
    editor.click()
    page.keyboard.type("Created by the upgrade check", delay=30)
    expect(editor).to_contain_text("Created by the upgrade check")
    publish(page)
    page.goto(f"{BASE}/upgrade-check-page/")
    expect(page.locator("body")).to_contain_text("Created by the upgrade check")


@step("Preview and revision history")
def preview_history(page):
    about_id = page_id(page, "About")
    response = page.request.get(f"{BASE}/admin/pages/{about_id}/edit/preview/?mode=")
    assert response.status in (200, 400), f"preview status {response.status}"
    page.goto(f"{BASE}/admin/pages/{about_id}/history/")
    expect(page.locator("main")).to_contain_text("Published")


@step("Draft page (unpublished) opens in editor")
def draft_page(page):
    open_editor(page, "Draft page")
    expect(page.locator("#id_title")).to_have_value("Draft page")


@step("Snippets: PageSegment and Meetup")
def snippets(page):
    page.goto(f"{BASE}/admin/snippets/")
    expect(page.locator("main")).to_contain_text("Page segments")
    expect(page.locator("main")).to_contain_text("Meetups")
    page.goto(f"{BASE}/admin/snippets/core/pagesegment/")
    page.locator("main").get_by_role("link", name=re.compile("Sidebar")).first.click()
    expect(page.locator("#id_title")).to_have_value("Sidebar")
    page.get_by_role("button", name="Save").click()
    expect(page.locator(".messages")).to_contain_text("updated", timeout=15000)
    page.goto(f"{BASE}/admin/snippets/meetups/meetup/")
    page.locator("main").get_by_role("link", name="November Meetup").first.click()
    expect(page.locator("#id_name")).to_have_value("November Meetup")
    page.get_by_role("button", name="Save").click()
    expect(page.locator(".messages")).to_contain_text("updated", timeout=15000)


@step("Images and documents")
def images_documents(page):
    page.goto(f"{BASE}/admin/images/")
    expect(page.locator("main")).to_contain_text("banner-webp")
    page.locator("main").get_by_role(
        "link", name=re.compile("banner-webp")
    ).first.click()
    expect(page.locator("#id_title")).to_have_value("banner-webp")
    page.goto(f"{BASE}/admin/documents/")
    expect(page.locator("main")).to_contain_text("CoC")


@step("Settings: sites, users, redirects")
def settings_pages(page):
    for path, text in [
        ("/admin/sites/", "127.0.0.1"),
        ("/admin/users/", "admin"),
        ("/admin/redirects/", "/old-about"),
    ]:
        page.goto(BASE + path)
        expect(page.locator("main")).to_contain_text(text)


@step("Django admin: sponsors")
def django_admin(page):
    page.goto(f"{BASE}/django-admin/")
    expect(page.locator("body")).to_contain_text("Sponsors")
    page.goto(f"{BASE}/django-admin/sponsors/sponsor/")
    expect(page.locator("body")).to_contain_text("Acme")


@step("Public pages render (home, nested, redirect, 404)")
def public_pages(page):
    for path, text in [
        ("/", "Python Ireland"),
        ("/meetups/", "Meetups"),
        ("/meetups/coc/", "Code of Conduct"),
    ]:
        response = page.goto(BASE + path)
        assert response.status == 200, f"{path} -> {response.status}"
        expect(page.locator("body")).to_contain_text(text)
        assert page.locator("img").count() >= 2, f"{path}: images missing"
    page.goto(f"{BASE}/old-about")
    assert page.url.endswith("/about/"), f"redirect landed on {page.url}"
    response = page.goto(f"{BASE}/nope/")
    assert response.status == 404


def main():
    with sync_playwright() as playwright:
        launch_options = {}
        if os.environ.get("CHROMIUM_PATH"):
            launch_options["executable_path"] = os.environ["CHROMIUM_PATH"]
        browser = playwright.chromium.launch(**launch_options)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.on(
            "console",
            lambda m: (
                m.type == "error" and console_errors.append(f"{page.url} :: {m.text}")
            ),
        )
        page.on(
            "pageerror",
            lambda e: console_errors.append(f"{page.url} :: PAGEERROR {e}"),
        )
        page.on(
            "response",
            lambda r: (
                r.status >= 400
                and not r.url.endswith(("/nope/", "/favicon.ico"))
                and bad_responses.append(f"{r.status} {r.request.method} {r.url}")
            ),
        )
        for run in steps:
            run(page)
        browser.close()

    for status, name, error in results:
        print(f"  {status}  {name}")
        if error:
            print(f"        -> {error}")
    print(f"\n  JS console errors: {len(console_errors)}")
    for error in dict.fromkeys(console_errors):
        print(f"    {error[:300]}")
    print(f"  HTTP >= 400 responses: {len(bad_responses)}")
    for response in dict.fromkeys(bad_responses):
        print(f"    {response[:300]}")
    print(f"\n  Screenshots: {OUT}")

    failed = [r for r in results if r[0] == "FAIL"]
    return 1 if failed or bad_responses else 0


if __name__ == "__main__":
    sys.exit(main())
