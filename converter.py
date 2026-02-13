from __future__ import annotations

import json
import pathlib
import urllib.request
import uuid
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List


@dataclass
class Node:
    kind: str
    text: str | None = None
    src: str | None = None
    href: str | None = None


class LandingExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.nodes: List[Node] = []
        self._current_tag: str | None = None
        self._buffer: List[str] = []
        self._a_href: str | None = None

    def handle_starttag(self, tag: str, attrs):
        attrs_dict = dict(attrs)
        if tag in {"h1", "h2", "p", "a"}:
            self._current_tag = tag
            self._buffer = []
            self._a_href = attrs_dict.get("href") if tag == "a" else None
        elif tag == "img":
            src = attrs_dict.get("src")
            if src:
                self.nodes.append(Node(kind="image", src=src))

    def handle_data(self, data: str):
        if self._current_tag:
            self._buffer.append(data)

    def handle_endtag(self, tag: str):
        if self._current_tag == tag:
            text = " ".join("".join(self._buffer).split()).strip()
            if text:
                if tag in {"h1", "h2"}:
                    self.nodes.append(Node(kind="heading", text=text))
                elif tag == "p":
                    self.nodes.append(Node(kind="text", text=text))
                elif tag == "a":
                    self.nodes.append(Node(kind="button", text=text, href=self._a_href))
            self._current_tag = None
            self._buffer = []
            self._a_href = None


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


def _widget_from_node(node: Node) -> dict:
    if node.kind == "heading":
        return {
            "id": _short_id(),
            "elType": "widget",
            "widgetType": "heading",
            "settings": {"title": node.text, "size": "xl"},
            "elements": [],
        }
    if node.kind == "text":
        return {
            "id": _short_id(),
            "elType": "widget",
            "widgetType": "text-editor",
            "settings": {"editor": f"<p>{node.text}</p>"},
            "elements": [],
        }
    if node.kind == "image":
        return {
            "id": _short_id(),
            "elType": "widget",
            "widgetType": "image",
            "settings": {"image": {"url": node.src}},
            "elements": [],
        }
    if node.kind == "button":
        return {
            "id": _short_id(),
            "elType": "widget",
            "widgetType": "button",
            "settings": {"text": node.text, "link": {"url": node.href or "#"}},
            "elements": [],
        }
    raise ValueError(f"Tipo de nó não suportado: {node.kind}")


def extract_nodes(html: str) -> List[Node]:
    parser = LandingExtractor()
    parser.feed(html)
    return parser.nodes


def build_elementor_template(nodes: List[Node], source_label: str = "imported") -> dict:
    widgets = [_widget_from_node(node) for node in nodes]

    return {
        "title": f"Imported from {source_label}",
        "type": "page",
        "version": "0.4",
        "page_settings": {},
        "content": [
            {
                "id": _short_id(),
                "elType": "section",
                "settings": {},
                "elements": [
                    {
                        "id": _short_id(),
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": widgets,
                    }
                ],
                "isInner": False,
            }
        ],
    }


def load_source(source: str) -> str:
    if source.startswith("http://") or source.startswith("https://"):
        with urllib.request.urlopen(source, timeout=20) as response:
            return response.read().decode("utf-8", errors="ignore")

    path = pathlib.Path(source)
    return path.read_text(encoding="utf-8")


def convert_source_to_template(source: str) -> dict:
    html = load_source(source)
    nodes = extract_nodes(html)
    return build_elementor_template(nodes, source)


def convert_to_json(source: str, output: str) -> None:
    template = convert_source_to_template(source)
    pathlib.Path(output).write_text(
        json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8"
    )
