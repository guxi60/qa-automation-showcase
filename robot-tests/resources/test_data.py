"""Python variable file for Robot Framework.

Reads shared test_data/*.yaml (same files used by Playwright & Selenium)
and exposes values as Robot Framework variables (uppercase = Robot variable).
"""

import os
from pathlib import Path

import yaml

from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# ── ChromeDriver ────────────────────────────────────────────────

def _get_chromedriver_path() -> str:
    """Return the path to a compatible ChromeDriver binary.

    Priority: 1) cached driver → 2) auto-detect (Linux CI) → 3) pinned v147
    Auto-detect first is essential on Linux where system Chrome ≠ v147.
    """
    _cached = list(
        (Path(os.environ.get("USERPROFILE", "")) / ".wdm" / "drivers" / "chromedriver" / "win64")
        .glob("147*/chromedriver-win64/chromedriver.exe"),
    )
    if _cached:
        return str(_cached[0])

    # Auto-detect: matches whatever Chrome is installed (critical on Linux CI)
    try:
        return ChromeDriverManager().install()
    except Exception:
        pass

    # Pinned v147: matches Playwright's bundled Chromium on Windows
    try:
        return ChromeDriverManager(
            driver_version="147.0.7727.15",
        ).install()
    except Exception:
        return ChromeDriverManager().install()

# ── shared test data ───────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_SHARED_DATA = _PROJECT_ROOT / "web-ui-tests" / "test_data"


def _load(filename: str) -> dict:
    path = _SHARED_DATA / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


_login = _load("login.yaml")
_inventory = _load("inventory.yaml")
_cart = _load("cart.yaml")
_checkout = _load("checkout.yaml")

# ── browser configuration ──────────────────────────────────────

_options = ChromeOptions()
_options.add_argument("--headless=new")
_options.add_argument("--no-sandbox")
_options.add_argument("--disable-dev-shm-usage")
_options.add_argument("--window-size=1280,720")

# Reuse Playwright's bundled Chromium
_playwright_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"
_chromiums = sorted(
    _playwright_dir.glob("chromium-*/chrome-win*/chrome.exe"), reverse=True
)
if _chromiums:
    _options.binary_location = str(_chromiums[0])

# ── exposed Robot variables ────────────────────────────────────

# URLs
BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
CART_URL = "https://www.saucedemo.com/cart.html"
CHECKOUT_STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
CHECKOUT_STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
CHECKOUT_COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

# Browser options object
CHROME_OPTIONS = _options
CHROMEDRIVER_PATH = _get_chromedriver_path()

# Login test cases: list of (id, username, password, expected_error_or_empty)
LOGIN_CASES = []
for tc in _login["login"]:
    LOGIN_CASES.append((
        tc["id"],
        tc["username"],
        tc["password"],
        tc.get("expected_error", ""),
        tc.get("severity", "NORMAL"),
        ",".join(tc.get("tags", [])),
    ))

# Inventory display cases
INVENTORY_DISPLAY_CASES = []
for tc in _inventory["display"]:
    INVENTORY_DISPLAY_CASES.append((
        tc["id"],
        tc["title"],
        tc.get("expected_count", ""),
        tc.get("severity", "NORMAL"),
        ",".join(tc.get("tags", [])),
    ))

# Sorting scenarios
SORT_SCENARIOS = _inventory["sorting"][0]["scenarios"]

# Cart badge test data
CART_BADGE_ITEMS = _inventory["cart_badge"][1]["add_items"]
CART_BADGE_ADD_REMOVE = _inventory["cart_badge"][2]["add_remove"]

# Cart test cases
CART_CASES = []
for tc in _cart["cart"]:
    CART_CASES.append((
        tc["id"],
        tc.get("add_items", []),
        tc.get("remove_item", ""),
        tc.get("add_item", ""),
        tc.get("severity", "NORMAL"),
        ",".join(tc.get("tags", [])),
    ))

# Checkout validation cases
CHECKOUT_VALIDATION_CASES = []
for tc in _checkout["validation"]:
    CHECKOUT_VALIDATION_CASES.append((
        tc["id"],
        tc["first_name"],
        tc["last_name"],
        tc["postal_code"],
        tc["expected_error"],
        tc.get("severity", "NORMAL"),
        ",".join(tc.get("tags", [])),
    ))

# E2E checkout data
CHECKOUT_E2E = _checkout["checkout"][0]
