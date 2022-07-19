def get_seq(u_track):
    """
    Level u_seq the track belongs

    :param u_track: unreal.MovieSceneTrack.
    :return: unreal.MovieSceneSequence.
    """
    return u_track.get_outer()


def get_sections(u_track):
    """
    Level u_seq sections within the track

    :param u_track: unreal.MovieSceneTrack.
    :return: [unreal.MovieSceneSection].
    """
    return u_track.get_sections()


def add_section(u_track):
    """
    Add a section to the level u_seq track

    :param u_track: unreal.MovieSceneTrack.
    :return: unreal.MovieSceneSection.
    """
    return u_track.add_section()


def clear_sections(u_track):
    """
    Remove all sections of the level u_seq track

    :param u_track: unreal.MovieSceneTrack.
    """
    for u_section in u_track.get_sections():
        u_track.remove_section(u_section)
