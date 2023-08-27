import unreal


def get_shots(u_master):
    [shot_track] = u_master.find_master_tracks_by_type(
        unreal.MovieSceneCinematicShotTrack)
    shots = shot_track.get_sections()
    for shot in shots:
        name = shot.get_editor_property('SubSequence').get_name()
        start = shot.get_start_frame()
        end = shot.get_end_frame()-1
        print(name, start, end)


def create_seq(u_folder, name):
    """
    Create a level u_seq and attach it to a Sequence Helper instance

    :param u_folder: str. target directory to store the created unreal level
                          u_seq
    :param name: str. name of the created unreal level u_seq
    :return: unreal.MovieSceneSequence. u_seq asset
    """
    u_asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    u_sequence = u_asset_tools.create_asset(
        name,
        u_folder,
        unreal.LevelSequence,
        unreal.LevelSequenceFactoryNew()
    )
    return u_sequence


def get_framerate(u_seq):
    """
    Get level u_seq framerate

    :return: int.
    """
    u_framerate = u_seq.get_display_rate()
    return u_framerate.numerator / u_framerate.denominator


def get_range(u_seq):
    """
    Get level u_seq active range
    
    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    :return: (int, int): start and end frame
    """
    return u_seq.get_playback_start(), u_seq.get_playback_end()


def set_range(u_seq, start, end):
    """
    Set the level u_seq active range

    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    :param start: int. start frame
    :param end: int. end frame
    """
    if start >= end:
        raise ValueError('Start frame cannot be equal/greater than end frame')

    u_seq.set_playback_start(start)
    u_seq.set_playback_end(end)


def set_display_range(u_seq, start, end):
    """
    Set the level u_seq display range

    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    :param start: int. start frame
    :param end: int. end frame
    """
    if start >= end:
        raise ValueError('Start frame cannot be equal/greater than end frame')

    framerate = get_framerate(u_seq)
    u_seq.set_view_range_start(float(start) / framerate)
    u_seq.set_view_range_end(float(end) / framerate)

    # TRACKS


def add_track(u_seq, typ, name=None):
    """
    Add a track to level u_seq

    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    :param typ: unreal.MovieSceneTrack.Type. track type
                e.g.
                MovieSceneSubTrack: Subsequences (also the base class)

                MovieSceneAudioTrack: Audio
                MovieSceneCinematicShotTrack: Shots
                MovieSceneCameraCutTrack: Camera Cut
                MovieSceneSkeletalAnimationTrack, Actor To Sequencer

                MovieSceneFloatTrack,
                MovieScene3DTransformTrack
                MovieSceneMediaTrack
    :param name: str. track name
    :return: unreal.MovieSceneTrack
    """
    u_track = u_seq.add_master_track(typ)
    if name:
        u_track.set_editor_property('display_name', name)
    return u_track


def clear_tracks(u_seq):
    """
    Remove all tracks (not bindings) of the level u_seq

    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    """
    for u_track in u_seq.get_master_tracks():
        u_seq.remove_master_track(u_track)


def bind_actor(u_seq, u_actor):
    """
    Add a binding to an actor in the level

    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    :param u_actor: unreal.Actor
    :return: unreal.SequencerBindingProxy. the binding object
    """
    return u_seq.add_possessable(object_to_possess=u_actor)


def get_bounds(u_seq):
    """
    Get all bindings of the level u_seq in the world

    :param u_seq: unreal.MovieSceneSequence. u_seq asset
    :return: [unreal.SequencerBindingProxy]
    """
    u_world = unreal.EditorLevelLibrary.get_editor_world()
    u_seq_bounds = unreal.SequencerTools().get_bound_objects(
        u_world,
        u_seq,
        u_seq.get_bindings(),
        u_seq.get_playback_range()
    )
    return [u_seq_bound.binding_proxy for u_seq_bound in u_seq_bounds]


def remove_binding(u_seq):
    # https://forums.unrealengine.com/t/python-remove-binding-correctly-in-sequence/482501/3
    bound_objects = get_bounds(u_seq)

    for bound_object in bound_objects:
        if bound_object.binding_proxy.get_display_name() == 'binding_name':
            tracks = bound_object.binding_proxy.get_tracks()
            for track in tracks:
                bound_object.binding_proxy.remove_track(track)
            bound_object.binding_proxy.remove()
            unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
