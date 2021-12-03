import os
import random
import sys
from dataclasses import dataclass

import streamlit as st
from PIL import Image

sys.path.append("../")


@dataclass
class NameOpt:
    name: str
    is_female: bool


name1_options = [NameOpt("תוכנה", True), NameOpt("חשמל", False), NameOpt("ביולוגיה", True)]

name2_options = [
    NameOpt("ימית", True),
    NameOpt("ימי", False),
    NameOpt("ביולוגית", True),
    NameOpt("ביולוגי", False),
    NameOpt("תת-מימית", True),
    NameOpt("תת-מימי", False),
    NameOpt("כימית", True),
    NameOpt("כימי", False),
    NameOpt("חישובית", True),
    NameOpt("חישובי", False),
    NameOpt("חישובית", True),
    NameOpt("חישובי", False),
]

university_options = ["בטכניון", "בבן גוריון", "בתל אביב", "בעברית", "בייל", "באוניברסיטת מוסקבה", "בפריפריה"]


def generate_program_name() -> str:
    """Generate a new psagot program at will."""
    name1 = random.choice(name1_options)
    if random.random() < 0.85:
        name2 = random.choice([n2 for n2 in name2_options if n2.is_female == name1.is_female])
    else:
        name2 = NameOpt("", False)
    prog_name = f"פסגות {name1.name} {name2.name}"

    degree = random.random()
    if degree < 0.15:
        prog_name += " לתואר שני"
    elif degree < 0.2:
        prog_name += " לתואר שלישי"
    elif degree < 0.25:
        prog_name += " לתואר רביעי"
    elif degree < 0.28:
        prog_name += " לתואר חמישי"

    if random.random() < 0.1:
        prog_name += " בתנאי פנימיה"

    prog_name += f" {random.choice(university_options)}"
    return prog_name


def main() -> None:
    """Psagot Program Generator."""
    image = Image.open(os.path.join(os.path.dirname(__file__), "Psagot.jpg"))
    c1, c2 = st.columns([1, 6])
    c1.image(image, width=100)
    c2.title("Psagot Program Generator")
    t = st.empty()

    small = st.empty()

    data = generate_program_name()
    t.markdown(f"<h1 style='text-align: center; color: red;'>{data}</h1>", unsafe_allow_html=True)
    if random.random() < 0.5:
        small.markdown(
            "<div style='text-align: right; color: gray; direction: rtl'>פסגות ט\"ו הכי prestigious</div>",
            unsafe_allow_html=True,
        )
    else:
        small.text(" ")

    _, bot2, _ = st.columns(3)

    bot2.button("Generate!")


if __name__ == "__main__":
    main()  # pragma: no cover
