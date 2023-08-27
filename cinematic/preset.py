import unreal


@unreal.uclass()
class MyPreset(unreal.MoviePipelineMasterConfig):

    def __init__(self, preset):
        super(MyPreset, self).__init__(preset)
        self.copy_from(preset)

        self.set_file_name()
        self.set_flush_disk()

    @unreal.ufunction(ret=None, params=[])
    def set_flush_disk(self):
        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        u_setting.flush_disk_writes_per_shot = True

    @unreal.ufunction(ret=None, params=[])
    def set_file_name(self):
        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        u_setting.set_editor_property('zero_pad_frame_numbers', 5)
        u_setting.set_editor_property('file_name_format', r'{frame_number}')

    @classmethod
    def get_base_preset(cls):
        u_preset = unreal.MoviePipelineMasterConfig()
        u_setting = u_preset.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )

        # A job should have a render pass and a file output.
        u_setting.output_resolution = unreal.IntPoint(1280, 720)

        render_pass = u_preset.find_or_add_setting_by_class(
            unreal.MoviePipelineDeferredPassBase
        )
        render_pass.disable_multisample_effects = True

        u_preset.find_or_add_setting_by_class(
            unreal.MoviePipelineImageSequenceOutput_PNG
        )
        u_preset.initialize_transient_settings()
        return cls(u_preset)

    @property
    def output_path(self):
        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        return u_setting.get_editor_property('output_directory')

    @unreal.ufunction(ret=None, params=[str])
    def set_output_path(self, path):
        """
        Set output directory of image sequences

        @param path: str. absolute Windows path to render outputs
        """
        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        u_setting.set_editor_property(
            'output_directory',
            unreal.DirectoryPath(path)
        )

    @unreal.ufunction(ret=None, params=[int])
    def set_frame_rate(self, frame_rate):
        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        u_setting.set_editor_property(
            'output_frame_rate',
            unreal.FrameRate(frame_rate, 1)
        )

    @unreal.ufunction(ret=None, params=[int, int])
    def set_resolution(self, width, height):
        if not width and not height:
            return

        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        u_setting.set_editor_property(
            'output_resolution',
            unreal.IntPoint(width, height)
        )

    @unreal.ufunction(ret=None, params=[int, int])
    def set_frame_range(self, start, end):
        if not start and not end:
            return

        u_setting = self.find_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        u_setting.set_editor_property('use_custom_playback_range', True)
        u_setting.set_editor_property('custom_start_frame', start)
        u_setting.set_editor_property('custom_end_frame', end+1)
