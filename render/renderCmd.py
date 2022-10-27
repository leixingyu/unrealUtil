"""
https://docs.unrealengine.com/4.26/en-US/AnimatingObjects/Sequencer/Workflow/RenderAndExport/RenderingCmdLine/
https://forums.unrealengine.com/t/ue5-rendering-from-command-line-not-working-anymore/538400
"""

import subprocess

UNREAL_EXE = ''
U_PROJECT = ''


def render(u_level_file, u_level_seq_file, u_preset_file):
    """
    Render through commandline using the movie render queue with preset

    :param u_level_file: str. Unreal path to level asset
    :param u_level_seq_file: str. Unreal path to level sequence asset
    :param u_preset_file: str. Unreal path to movie render queue preset asset
    :return:
    """
    command = [
        UNREAL_EXE,
        U_PROJECT,
        u_level_file,

        # required
        "-LevelSequence=%s" % u_level_seq_file,  # The sequence to render
        "-MoviePipelineConfig=\"%s\"" % u_preset_file,
        "-game",

        # options
        "-NoLoadingScreen",
        "-log",
        "-NoTextureStreaming",  # for final render
        "-NoScreenMessages",  # no screen debug message

        # window size
        "-Windowed",
        "-ResX=800",
        "-ResY=600",
    ]
    print(command)
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return proc.communicate()


def render_legacy(u_level_file, u_level_seq_file, output_folder):
    """
    Render through commandline using the legacy movie scene capture

    :param u_level_file: str. Unreal path to level asset
    :param u_level_seq_file: str. Unreal path to level sequence asset
    :param output_folder: str. system folder to export out
    :return:
    """
    command = [
        UNREAL_EXE,
        U_PROJECT,
        u_level_file,

        # required
        "-LevelSequence=%s" % u_level_seq_file,  # The sequence to render
        "-MovieSceneCaptureType=/Script/MovieSceneCapture.AutomatedLevelSequenceCapture",
        "-NoLoadingScreen",
        "-game",
        "-log",
        "-MovieCinematicMode=yes",

        # general property
        "-MovieFolder=%s" % output_folder,

        # if doing .avi
        "-MovieFormat=Video",  # JPG, BMP, PNG or Video
        "-MovieFrameRate=24",
        "-MovieQuality=100",  # compression quality in percentage
        "-Windowed",
        "-ResX=1920",
        "-ResY=1080",

        # other
        "-NoTextureStreaming",  # for final render
        "-NoScreenMessages",  # no screen debug message
    ]
    print(command)
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return proc.communicate()
