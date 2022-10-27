"""
https://github.com/ue4plugins/tk-unreal/blob/master/hooks/tk-multi-publish2/basic/publish_movie.py
"""

import unreal

ERROR_CALLBACK = unreal.OnMoviePipelineExecutorErrored()
FINISH_CALLBACK = unreal.OnMoviePipelineExecutorFinished()


def render_errored(executor, pipeline, is_fatal, error_msg):
    unreal.log_warning(
        "Render Error: \n"
        "Executor: {}\n"
        "Pipeline: {} \n"
        "Fatal? {} \n"
        "{}".format(executor, pipeline, is_fatal, error_msg)
    )


def render_finished(executor, is_success):
    unreal.log_warning(
        'Render Success? {} \n'
        'Executor: {}'.format(is_success, executor)
    )


ERROR_CALLBACK.add_callable(render_errored)
FINISH_CALLBACK.add_callable(render_finished)


def get_render_presets(folder):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    asset_datas = asset_registry.get_assets_by_path(folder)

    return [assetData.get_asset()
            for assetData in asset_datas
            if isinstance(assetData.get_asset(),
                          unreal.MoviePipelineMasterConfig)]


class Renderer(object):
    subsystem = None
    queue = None
    executor = None

    def __init__(self):
        # get movie queue subsystem for editor
        self.subsystem = unreal.get_editor_subsystem(
            unreal.MoviePipelineQueueSubsystem)
        self.queue = self.subsystem.get_queue()
        self.executor = unreal.MoviePipelinePIEExecutor()

        self.register_callback()
        self.clear_jobs()

    @property
    def jobs(self):
        return self.queue.get_jobs()

    def render(self):
        self.subsystem.render_queue_with_executor_instance(self.executor)

    def clear_jobs(self):
        self.queue.delete_all_jobs()

    def remove_job(self, name):
        for job in self.jobs:
            if job.job_name == name:
                self.queue.delete_job(job)

    def add_job(self, name, map_path, sequence_path, preset):
        # Create new movie pipeline job
        job = self.queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
        job.job_name = name
        job.map = unreal.SoftObjectPath(map_path)
        job.sequence = unreal.SoftObjectPath(sequence_path)
        job.set_configuration(preset)

    def register_callback(self):
        global ERROR_CALLBACK
        global FINISH_CALLBACK

        self.executor.on_executor_errored_delegate = ERROR_CALLBACK
        self.executor.on_executor_finished_delegate = FINISH_CALLBACK
