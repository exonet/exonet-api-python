"""Fail when an installed package has a license outside the allowlist."""

import importlib.metadata
import re
import sys

ALLOWED = re.compile(
    r"MIT|MPL|HPND|PSF|BSD|Apache|ISC|LGPL|Expat"
    r"|Python Software Foundation License|Unlicense",
)
PROJECT = "exonetapi"


def licenses(dist: importlib.metadata.Distribution) -> list[str]:
    # A package declares its license in any of three fields, so read them all.
    meta = dist.metadata
    # Every part of an AND expression applies, so each part has to be allowed.
    found = re.split(r"\s+AND\s+", meta.get("License-Expression") or "")
    found.append((meta.get("License") or "").strip().split("\n")[0])
    found += [
        classifier.rsplit(" :: ", 1)[-1]
        for classifier in meta.get_all("Classifier") or []
        if classifier.startswith("License :: ")
        and classifier != "License :: OSI Approved"
    ]
    return [license_ for license_ in found if license_.strip()]


def main() -> int:
    failed = False
    for dist in importlib.metadata.distributions():
        name = dist.metadata["Name"]
        if name == PROJECT:
            continue
        found = licenses(dist)
        if not found:
            print(f"{name}: no license metadata")
            failed = True
        for license_ in found:
            if not ALLOWED.search(license_):
                print(f"{name}: {license_}")
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
