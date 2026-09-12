"""Flip-to-start Pomodoro enclosure for Waveshare ESP32-S3 Touch AMOLED 1.8."""

from pathlib import Path

from build123d import *


# Finished device in the factory black enclosure.
DEVICE_W = 37.6
DEVICE_H = 45.2
DEVICE_MAX_D = 15.5
DEVICE_XY_CLEARANCE = 0.15
DEVICE_POCKET_W = DEVICE_W + 2 * DEVICE_XY_CLEARANCE
DEVICE_POCKET_H = DEVICE_H + 2 * DEVICE_XY_CLEARANCE
DEVICE_POCKET_RADIUS = 2.4

ACTIVE_W = 28.70
ACTIVE_H = 34.94
# Only the illuminated screen remains visible; the wider rim bears on the
# factory case and keeps the device from moving at the front.
WINDOW_CLEARANCE = 0.7
WINDOW_W = ACTIVE_W + 2 * WINDOW_CLEARANCE
WINDOW_H = ACTIVE_H + 2 * WINDOW_CLEARANCE
WINDOW_RADIUS = 3.2

CASE_SIZE = 52.0
CASE_DEPTH = 46.0
CORNER_RADIUS = 3.2
WALL = 1.8
LID_T = 2.0
# A deep plug guides the lid squarely and grips the factory case over 8 mm,
# which is what stops the assembly from rocking.
PLUG_DEPTH = 8.0
PLUG_CLEARANCE = 0.25
STOP_T = 1.4

DEVICE_FRONT = LID_T

# Four cantilever tongues, two per flexible side wall. Each carries a barb
# ramped on both faces: the rear ramp snaps in, the front ramp cams the tongue
# aside under a straight pull, so the lid holds firmly yet comes off by hand.
LATCH_W = 12.0
LATCH_X = 11.5
LATCH_HOOK = 0.70
LATCH_TIP = 0.15
LATCH_RELEASE = 0.70
LATCH_LAND = 0.50
LATCH_LEAD = 1.40
LATCH_H = LATCH_RELEASE + LATCH_LAND + LATCH_LEAD
LATCH_Z = LID_T + PLUG_DEPTH - LATCH_H - 0.8
TONGUE_ROOT_Z = LID_T + 1.4
SLIT_W = 0.8

# USB-C on the short factory-case edge (+X, the "10" face).
# Rectangular clearance for straight and bulky reversible cable overmolds,
# centered on the connector position in the official board STEP. The chamfered
# mouth reads as a finished port and guides the plug in. Its width leaves room
# for the two push-buttons that share this face.
USB_W = 14.0
USB_H = 10.0
USB_Z = 8.2
USB_CORNER = 0.8
USB_CHAMFER = 0.6

# The factory PWR and BOOT keys sit on the USB face, 10.5 mm either side of the
# connector (from the official board STEP). Printed push-buttons reach them
# through the wall, so the device can be switched off without opening the case.
# Each button is a stem in a bore with an inner flange that stops it falling
# out; the device key itself springs it back.
BUTTON_Y = 10.5
BUTTON_Z = 7.2
BUTTON_BORE_W = 4.4
BUTTON_BORE_H = 5.0
BUTTON_BORE_R = 1.0
BUTTON_STEM_W = 4.0
BUTTON_STEM_H = 4.6
BUTTON_STEM_R = 0.8
BUTTON_FLANGE_W = 6.6
BUTTON_FLANGE_H = 5.0
BUTTON_FLANGE_T = 1.0
BUTTON_SINK = 0.3
BUTTON_GAP = 0.5

# Matching scallops under the seam on the 5 and 30 faces. They expose the back
# edge of the lid so it can be pinched off with two fingernails.
GRIP_W = 16.0
GRIP_H = 2.2
GRIP_DEPTH = 1.0
GRIP_Z = LID_T + GRIP_H / 2

# Side texts, in order: +Y, +X (USB face), -Y, -X. Change these four strings
# to engrave whatever you want on a labeled variant. Empty strings skip a face.
LABELS = ("5", "10", "30", "60")
LABEL_DEPTH = 0.55
LABEL_SIZE = 22.0
LABEL_Z = 31.0

# Sparse honeycomb behind the device so the rear cavity prints without supports.
INFILL_PITCH = 11.0
INFILL_T = 0.8

OUTPUT_DIR = Path(__file__).parent

INNER = CASE_SIZE - 2 * WALL
PLUG_SIZE = INNER - 2 * PLUG_CLEARANCE
PLUG_RADIUS = max(CORNER_RADIUS - WALL - PLUG_CLEARANCE, 1.5)
FRAME_INNER_W = DEVICE_POCKET_W
FRAME_INNER_H = DEVICE_POCKET_H


def rounded_prism(width: float, height: float, depth: float, radius: float, z: float):
    with BuildPart() as part:
        with BuildSketch(Plane.XY.offset(z)):
            RectangleRounded(
                width, height, min(radius, width / 2 - 0.05, height / 2 - 0.05)
            )
        extrude(amount=depth)
    return part.part


def _cut_rounded_slot(
    plane: Plane,
    width: float,
    height: float,
    depth: float,
    radius: float | None = None,
):
    if radius is None:
        radius = min(width, height) / 2
    with BuildPart() as cutter:
        with BuildSketch(plane):
            RectangleRounded(
                width, height, min(radius, width / 2 - 0.05, height / 2 - 0.05)
            )
        extrude(amount=depth)
    return cutter.part


def _usb_port_cutter():
    """Straight rectangular bore plus a 45 degree chamfered mouth."""
    sleeve_x = (INNER - DEVICE_POCKET_W) / 2
    outer = Plane(
        origin=(CASE_SIZE / 2 + 0.2, 0, USB_Z), x_dir=(0, 1, 0), z_dir=(1, 0, 0)
    )
    lip = USB_CHAMFER + 0.2

    with BuildPart() as bore:
        with BuildSketch(outer):
            RectangleRounded(USB_W, USB_H, USB_CORNER)
        extrude(amount=-(WALL + sleeve_x + 1.4))

    with BuildPart() as flare:
        with BuildSketch(outer):
            RectangleRounded(USB_W + 2 * lip, USB_H + 2 * lip, USB_CORNER + lip)
        with BuildSketch(outer.offset(-lip)):
            RectangleRounded(USB_W, USB_H, USB_CORNER)
        loft(ruled=True)

    return bore.part + flare.part


def _latch_barb(x: float, y_sign: int):
    """Barb on one tongue, ramped on both faces so it snaps in and releases."""
    y0 = y_sign * PLUG_SIZE / 2
    align = (Align.CENTER, Align.MAX if y_sign < 0 else Align.MIN)
    profile = (
        (LATCH_Z, LATCH_TIP),
        (LATCH_Z + LATCH_RELEASE, LATCH_HOOK),
        (LATCH_Z + LATCH_RELEASE + LATCH_LAND, LATCH_HOOK),
        (LATCH_Z + LATCH_H, LATCH_TIP),
    )
    with BuildPart() as barb:
        for z, reach in profile:
            with BuildSketch(Plane.XY.offset(z)):
                with Locations((x, y0)):
                    Rectangle(LATCH_W, reach, align=align)
        loft(ruled=True)
    return barb.part


def make_cavity_infill():
    """Honeycomb behind the device pocket: light, printable walls, no supports."""
    sleeve_end = LID_T + DEVICE_MAX_D + STOP_T
    back_inner = CASE_DEPTH - WALL
    z = sleeve_end - 0.4
    depth = back_inner - sleeve_end + 0.8
    hole_apothem = INFILL_PITCH / 2 - INFILL_T / 2
    loc_apothem = INFILL_PITCH / 2
    with BuildPart() as infill:
        with BuildSketch(Plane.XY.offset(z)):
            RectangleRounded(
                INNER + 0.6,
                INNER + 0.6,
                max(CORNER_RADIUS - WALL, 1.0),
            )
            with HexLocations(loc_apothem, 7, 7, major_radius=False):
                RegularPolygon(
                    hole_apothem, 6, major_radius=False, mode=Mode.SUBTRACT
                )
        extrude(amount=depth)
    return infill.part


def _label_planes():
    return (
        Plane(origin=(0, CASE_SIZE / 2, LABEL_Z), x_dir=(-1, 0, 0), z_dir=(0, 1, 0)),
        Plane(origin=(CASE_SIZE / 2, 0, LABEL_Z), x_dir=(0, 1, 0), z_dir=(1, 0, 0)),
        Plane(origin=(0, -CASE_SIZE / 2, LABEL_Z), x_dir=(1, 0, 0), z_dir=(0, -1, 0)),
        Plane(origin=(-CASE_SIZE / 2, 0, LABEL_Z), x_dir=(0, -1, 0), z_dir=(-1, 0, 0)),
    )


def _add_labels(part, labels=LABELS):
    if len(labels) != 4:
        raise ValueError("LABELS must have exactly four strings: +Y, +X, -Y, -X")
    for label, plane in zip(labels, _label_planes()):
        if not str(label).strip():
            continue
        with BuildPart() as engraving:
            with BuildSketch(plane):
                Text(str(label), font_size=LABEL_SIZE, font_style=FontStyle.BOLD)
            extrude(amount=-LABEL_DEPTH)
        part -= engraving.part
    return part


def _lid_channel_width():
    return 2 * (BUTTON_Y + BUTTON_FLANGE_W / 2 + 0.4)


def make_body(with_buttons: bool = True, with_labels: bool = True, labels=LABELS):
    """Cube open at the front. The device drops in; the lid with the window closes it."""
    body = rounded_prism(
        CASE_SIZE, CASE_SIZE, CASE_DEPTH - LID_T, CORNER_RADIUS, LID_T
    )
    body -= rounded_prism(
        INNER,
        INNER,
        CASE_DEPTH - LID_T - WALL + 0.1,
        max(CORNER_RADIUS - WALL, 1.0),
        LID_T,
    )

    sleeve_z = LID_T + PLUG_DEPTH
    sleeve_depth = DEVICE_MAX_D - PLUG_DEPTH + STOP_T
    sleeve = rounded_prism(
        INNER + 0.6,
        INNER + 0.6,
        sleeve_depth,
        max(CORNER_RADIUS - WALL, 1.0),
        sleeve_z,
    )
    sleeve -= rounded_prism(
        DEVICE_POCKET_W,
        DEVICE_POCKET_H,
        DEVICE_MAX_D - PLUG_DEPTH + 0.1,
        DEVICE_POCKET_RADIUS,
        sleeve_z - 0.1,
    )
    body += sleeve
    body += make_cavity_infill()

    body -= _usb_port_cutter()

    if with_buttons:
        for y in (-BUTTON_Y, BUTTON_Y):
            bore_plane = Plane(
                origin=(CASE_SIZE / 2 + 0.2, y, BUTTON_Z),
                x_dir=(0, 1, 0),
                z_dir=(1, 0, 0),
            )
            body -= _cut_rounded_slot(
                bore_plane, BUTTON_BORE_W, BUTTON_BORE_H, -(WALL + 0.4), BUTTON_BORE_R
            )

    groove_d = LATCH_HOOK + 0.2
    groove_h = LATCH_H + 0.5
    for y in (-1, 1):
        for x in (-LATCH_X, LATCH_X):
            body -= Box(LATCH_W + 0.6, groove_d, groove_h).move(
                Location(
                    (
                        x,
                        y * (INNER / 2 + groove_d / 2),
                        LATCH_Z - 0.1 + groove_h / 2,
                    )
                )
            )

    for y in (-1, 1):
        grip_plane = Plane(
            origin=(0, y * (CASE_SIZE / 2 + 0.2), GRIP_Z),
            x_dir=(1, 0, 0),
            z_dir=(0, y, 0),
        )
        body -= _cut_rounded_slot(grip_plane, GRIP_W, GRIP_H, -(GRIP_DEPTH + 0.2))

    if with_labels:
        body = _add_labels(body, labels)
    return body


def make_lid():
    """Front lid with the screen opening. Hidden hooks click into the body."""
    lid = rounded_prism(CASE_SIZE, CASE_SIZE, LID_T, CORNER_RADIUS, 0)
    lid -= rounded_prism(WINDOW_W, WINDOW_H, LID_T + 0.2, WINDOW_RADIUS, -0.1)

    frame = rounded_prism(PLUG_SIZE, PLUG_SIZE, PLUG_DEPTH, PLUG_RADIUS, LID_T)
    frame -= rounded_prism(
        FRAME_INNER_W,
        FRAME_INNER_H,
        PLUG_DEPTH + 0.2,
        DEVICE_POCKET_RADIUS,
        LID_T - 0.1,
    )
    lid += frame

    # One open channel on the USB side, running the full depth of the frame.
    # The cable, both factory keys and the push-button flanges all pass through
    # it, so the device is loaded into the body first and the lid just drops on
    # without lining anything up. Two corner blocks keep centering the device.
    channel_w = _lid_channel_width()
    lid -= Box(
        PLUG_SIZE / 2 - FRAME_INNER_W / 2 + 1.0,
        channel_w,
        PLUG_DEPTH + 0.4,
    ).move(
        Location(
            (
                (PLUG_SIZE + FRAME_INNER_W) / 4,
                0,
                LID_T + (PLUG_DEPTH + 0.4) / 2,
            )
        )
    )

    # Slit the flexible side walls into free tongues, then add their barbs.
    slit_len = PLUG_DEPTH - 1.4 + 0.4
    slit_inner = FRAME_INNER_H / 2 - 0.5
    slit_outer = PLUG_SIZE / 2 + 1.0
    for y in (-1, 1):
        for x in (-LATCH_X, LATCH_X):
            for edge in (-1, 1):
                lid -= Box(
                    SLIT_W, slit_outer - slit_inner, slit_len
                ).move(
                    Location(
                        (
                            x + edge * (LATCH_W / 2 + 0.9),
                            y * (slit_inner + slit_outer) / 2,
                            TONGUE_ROOT_Z + slit_len / 2,
                        )
                    )
                )
            lid += _latch_barb(x, y)

    return lid


def button_nose_length():
    return INNER / 2 - BUTTON_FLANGE_T - (DEVICE_W / 2 + BUTTON_GAP)


def make_button():
    """Printed push-button, two needed, reaching a factory key through the wall.

    Loaded from inside the body before the device goes in. The flange stops it
    from falling out through the bore, the device key springs it back, and the
    cap stays below the face so the cube still sits flat on the USB side.
    """
    nose = button_nose_length()
    stem = WALL - BUTTON_SINK
    button = rounded_prism(BUTTON_STEM_W, BUTTON_STEM_H, nose, BUTTON_STEM_R, 0)
    button += rounded_prism(
        BUTTON_FLANGE_W, BUTTON_FLANGE_H, BUTTON_FLANGE_T, BUTTON_BORE_R, nose
    )
    button += rounded_prism(
        BUTTON_STEM_W, BUTTON_STEM_H, stem, BUTTON_STEM_R, nose + BUTTON_FLANGE_T
    )
    return button


def validate(body, lid, button=None, with_buttons: bool = True, with_labels: bool = True, labels=LABELS):
    assert len(body.solids()) == 1 and len(lid.solids()) == 1
    assert body.volume > 6_000 and lid.volume > 1_500
    assert abs(body.bounding_box().size.X - CASE_SIZE) < 0.01
    assert abs(lid.bounding_box().size.X - CASE_SIZE) < 0.05
    assert ACTIVE_W < WINDOW_W < DEVICE_W
    assert ACTIVE_H < WINDOW_H < DEVICE_H
    assert (DEVICE_W - WINDOW_W) / 2 > 3.0
    assert (DEVICE_H - WINDOW_H) / 2 > 3.0
    assert 0.4 <= LATCH_HOOK - PLUG_CLEARANCE <= 0.5
    assert LATCH_Z + LATCH_H < LID_T + PLUG_DEPTH
    assert 2 * LATCH_X + LATCH_W < PLUG_SIZE

    device = rounded_prism(DEVICE_W, DEVICE_H, DEVICE_MAX_D, 3.0, DEVICE_FRONT)
    assert body.intersect(device).volume < 0.01
    assert body.intersect(lid).volume < 5.0

    if with_labels:
        usb_label = str(labels[1]).strip()
        if usb_label:
            usb_top = USB_Z + USB_H / 2
            with BuildSketch() as label_sk:
                Text(usb_label, font_size=LABEL_SIZE, font_style=FontStyle.BOLD)
            label_h = label_sk.sketch.bounding_box().size.Y
            assert LABEL_Z - label_h / 2 > usb_top + 1.5

    if with_buttons:
        assert button is not None and len(button.solids()) == 1
        # The stem slides in the bore, the flange cannot follow it out.
        assert BUTTON_STEM_W < BUTTON_BORE_W and BUTTON_STEM_H < BUTTON_BORE_H
        assert BUTTON_FLANGE_W > BUTTON_BORE_W + 1.0
        # The bore clears the chamfered port mouth.
        port_half = USB_W / 2 + USB_CHAMFER + 0.2
        assert BUTTON_Y - BUTTON_BORE_W / 2 - port_half > 0.3
        # The flange stays clear of the pocket sleeve behind the lid frame.
        assert BUTTON_Z + BUTTON_FLANGE_H / 2 < LID_T + PLUG_DEPTH - 0.2
        # At rest the nose hovers off the device instead of holding a key down.
        assert button.bounding_box().size.Z == button_nose_length() + BUTTON_FLANGE_T + (
            WALL - BUTTON_SINK
        )
        assert BUTTON_GAP >= 0.4
        # The lid channel is wide enough for both flanges to travel in.
        assert _lid_channel_width() < PLUG_SIZE - 8.0


VARIANTS = (
    ("buttons/labeled", True, True),
    ("buttons/unlabeled", True, False),
    ("no_buttons/labeled", False, True),
    ("no_buttons/unlabeled", False, False),
)


def export_variant(folder: str, with_buttons: bool, with_labels: bool, labels=LABELS):
    output = OUTPUT_DIR / folder
    output.mkdir(parents=True, exist_ok=True)
    body = make_body(with_buttons=with_buttons, with_labels=with_labels, labels=labels)
    lid = make_lid()
    button = make_button() if with_buttons else None
    validate(
        body,
        lid,
        button,
        with_buttons=with_buttons,
        with_labels=with_labels,
        labels=labels,
    )
    export_step(body, output / "body.step")
    export_stl(body, output / "body.stl")
    export_step(lid, output / "lid.step")
    export_stl(lid, output / "lid.stl")
    if button is not None:
        export_step(button, output / "button.step")
        export_stl(button, output / "button.stl")
    print(f"Exported {folder}")


if __name__ == "__main__":
    for folder, with_buttons, with_labels in VARIANTS:
        export_variant(folder, with_buttons, with_labels, LABELS)
    print("Exported all Pomodoro enclosure variants")
