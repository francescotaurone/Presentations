## Media

[Youtube](https://youtu.be/MGfgmy_0JM4) video with the resulting presentation.
[Paper](https://arxiv.org/abs/2303.04478) linked to the presentation.

## How to build

This presentation was meant to be a video.
To build the presentation, first create a virtual environment with 
<code>
python3 -m venv env
</code> 

or, for all the steps, follow [this guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

Once activated the environment with 
<code>
source env/bin/activate
</code>

install the required packages with
<code>
python3 -m pip install -r requirements.txt
</code>

Then, build the presentation using manim, with the command
<code>
manim -qh main.py FullPresentation
</code>

Manim will output the path to the produced video file.
Remember that you can choose the quality of the video with the arguments to the call (in this case, -h is "high").

Cheers!

