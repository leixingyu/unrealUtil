import unreal


def get_track(u_section):
    """
    Get level u_seq track the section belongs

    :param u_section: unreal.MovieSceneSection.
    :return: unreal.MovieSceneTrack.
    """
    return u_section.get_outer()


def get_seq(u_section):
    """
    Get level u_seq the section belongs

    :param u_section: unreal.MovieSceneSection.
    :return: unreal.MovieSceneSequence.
    """
    return u_section.get_outermost()


def get_sub_seq(u_section):
    """
    Get level u_seq attached to the section

    :param u_section: unreal.MovieSceneSection.
    :return: unreal.MovieSceneSequence.
    """
    return u_section.get_editor_property('SubSequence')


def set_sub_seq(u_section, u_seq):
    """
    Attach a level sequence to the track

    :param u_section: unreal.MovieSceneSection.
    :param u_seq: unreal.MovieSceneSequence.
    """
    u_section.set_sequence(u_seq)


def set_range(u_section, start, end):
    """
    Set the level u_seq section active range

    :param u_section: unreal.MovieSceneSection.
    :param start: int. start frame
    :param end: int. end frame
    """
    if start >= end:
        raise ValueError('Start frame cannot be equal/greater than end frame')

    u_section.set_end_frame(end)
    u_section.set_start_frame(start)


def bind_camera(u_section, u_binding):
    """
    Attach a camera binding to the 'Camera Cut' track section

    :param u_section: unreal.MovieSceneSection. has to be a section in the
                      'Camera Cut' track
    :param u_binding: unreal.SequencerBindingProxy. the camera actor binding
                      to attach to the camera cut track section.
    """
    u_section.set_camera_binding_id(u_binding.get_binding_id())


def set_skm_anim(u_section, u_anim_seq):
    """
    Attach an animation sequence to the 'Skeletal Actor Binding' track's
    section

    :param u_section: unreal.MovieSceneSection. has to be a section in the
                      'Skeletal Actor Binding' track
    :param u_anim_seq: unreal.AnimSequence.
    """
    param = unreal.MovieSceneSkeletalAnimationParams()
    param.set_editor_property('animation', u_anim_seq)

    # section to house anim
    u_section.set_editor_property('params', param)
    u_section.set_completion_mode(unreal.MovieSceneCompletionMode.KEEP_STATE)
