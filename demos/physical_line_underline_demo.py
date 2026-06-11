"""Privacy-safe physical-line underline demo.

This script demonstrates the core CV idea used in the research notes:

1. Load a handwriting/essay image.
2. Build a foreground mask with adaptive thresholding.
3. Remove long horizontal/vertical ruling lines.
4. Detect physical text lines by y-axis projection.
5. Estimate each line's left/right bounds and local slope.
6. Draw a simple underline below each detected line.

It intentionally avoids internal services, OCR calls, tokens, Nacos config, and private APIs.

Usage:
    python demos/physical_line_underline_demo.py \
        --input sample_images/example.jpg \
        --output outputs/example_underlined.jpg
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass
class TextLine:
    x1: int
    y1: int
    x2: int
    y2: int
    slope: float

    @property
    def height(self) -> int:
        return max(1, self.y2 - self.y1 + 1)

    @property
    def x_center(self) -> float:
        return (self.x1 + self.x2) / 2

    @property
    def y_center(self) -> float:
        return (self.y1 + self.y2) / 2


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {path}")
    return image


def build_foreground_mask(image: np.ndarray) -> np.ndarray:
    """Return a 0/1 handwriting-like foreground mask."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Black foreground becomes 255 after THRESH_BINARY_INV.
    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        35,
        15,
    )

    height, width = binary.shape

    # Remove long paper ruling lines. Kernel sizes are proportional so the
    # script can work on both small demo images and high-resolution photos.
    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (max(20, width // 25), 1)
    )
    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, max(20, height // 25))
    )

    horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)
    vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)
    ruling = cv2.dilate(cv2.bitwise_or(horizontal, vertical), np.ones((3, 3), np.uint8))

    foreground = cv2.bitwise_and(binary, cv2.bitwise_not(ruling))
    return (foreground > 0).astype(np.uint8)


def smooth_projection(values: np.ndarray, radius: int = 3) -> np.ndarray:
    kernel = np.ones(radius * 2 + 1, dtype=np.float32) / (radius * 2 + 1)
    return np.convolve(values.astype(np.float32), kernel, mode="same")


def connected_ranges(mask: np.ndarray) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(mask):
        if value and start is None:
            start = index
        elif not value and start is not None:
            ranges.append((start, index - 1))
            start = None
    if start is not None:
        ranges.append((start, len(mask) - 1))
    return ranges


def merge_close_ranges(
    ranges: list[tuple[int, int]], merge_gap: int
) -> list[tuple[int, int]]:
    if not ranges:
        return []
    merged = [ranges[0]]
    for y1, y2 in ranges[1:]:
        prev_y1, prev_y2 = merged[-1]
        if y1 - prev_y2 <= merge_gap:
            merged[-1] = (prev_y1, max(prev_y2, y2))
        else:
            merged.append((y1, y2))
    return merged


def estimate_slope(points: np.ndarray, max_abs_slope: float = 0.12) -> float:
    """Fit y = kx + b on foreground points in one physical line."""
    if len(points) < 20:
        return 0.0

    xs = points[:, 1].astype(np.float32)
    ys = points[:, 0].astype(np.float32)
    x_mean = float(xs.mean())
    y_mean = float(ys.mean())

    denom = float(((xs - x_mean) ** 2).sum())
    if denom <= 1e-6:
        return 0.0

    slope = float(((xs - x_mean) * (ys - y_mean)).sum() / denom)
    if abs(slope) > max_abs_slope:
        return 0.0
    return slope


def detect_text_lines(mask: np.ndarray) -> list[TextLine]:
    height, width = mask.shape
    row_projection = mask.sum(axis=1)
    smoothed = smooth_projection(row_projection, radius=max(2, height // 500))

    threshold = max(8, np.percentile(smoothed[smoothed > 0], 35) if np.any(smoothed > 0) else 8)
    raw_ranges = connected_ranges(smoothed > threshold)
    y_ranges = merge_close_ranges(raw_ranges, merge_gap=max(3, height // 180))

    lines: list[TextLine] = []
    min_height = max(6, height // 120)
    min_width = max(30, width // 20)
    min_ink = max(30, width // 80)

    for y1, y2 in y_ranges:
        if y2 - y1 + 1 < min_height:
            continue

        line_mask = mask[y1 : y2 + 1, :]
        if int(line_mask.sum()) < min_ink:
            continue

        col_projection = line_mask.sum(axis=0)
        xs = np.where(col_projection > 0)[0]
        if len(xs) == 0:
            continue

        x1 = max(0, int(xs.min()) - 5)
        x2 = min(width - 1, int(xs.max()) + 5)
        if x2 - x1 + 1 < min_width:
            continue

        points = np.argwhere(line_mask[:, x1 : x2 + 1] > 0)
        if len(points):
            points[:, 0] += y1
            points[:, 1] += x1
        slope = estimate_slope(points)

        lines.append(TextLine(x1=x1, y1=y1, x2=x2, y2=y2, slope=slope))

    return lines


def underline_points(line: TextLine, image_shape: tuple[int, int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    image_height, image_width = image_shape[:2]
    offset = max(4, int(line.height * 0.25))

    def y_at(x: int) -> int:
        y_mid = line.y_center + line.slope * (x - line.x_center)
        y = y_mid + line.height / 2 + offset
        return int(np.clip(round(y), 0, image_height - 1))

    x1 = int(np.clip(line.x1, 0, image_width - 1))
    x2 = int(np.clip(line.x2, 0, image_width - 1))
    return (x1, y_at(x1)), (x2, y_at(x2))


def draw_underlines(image: np.ndarray, lines: list[TextLine]) -> np.ndarray:
    output = image.copy()
    for line in lines:
        start, end = underline_points(line, output.shape)
        cv2.line(output, start, end, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Input essay/handwriting image")
    parser.add_argument("--output", required=True, type=Path, help="Output image path")
    args = parser.parse_args()

    image = load_image(args.input)
    mask = build_foreground_mask(image)
    lines = detect_text_lines(mask)
    output = draw_underlines(image, lines)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.output), output)
    print(f"Detected {len(lines)} physical lines. Saved: {args.output}")


if __name__ == "__main__":
    main()
